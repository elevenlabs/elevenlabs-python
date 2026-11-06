from __future__ import annotations

import json
import typing

from ..core.unchecked_base_model import construct_type
from ..types.agent_workflow_request_model import AgentWorkflowRequestModel
from ..types.agent_workflow_response_model import AgentWorkflowResponseModel
from ..types.get_agent_response_model import GetAgentResponseModel
from ._wire import WireDict, canonical, deep_copy, to_wire
from .condition import Condition, ConditionInput
from .errors import WorkflowIssue, WorkflowValidationError
from .graph import GraphEdge, WorkflowGraph
from .layout import layout
from .node import EdgeOrigin, WorkflowBranch, WorkflowChain, WorkflowNode, branch
from .validate import reverse_edge_merges, validate


class Workflow(WorkflowChain):
    """
    An agent workflow, written as code. The workflow itself is the start node: calling a verb on it branches
    from the start.

    Examples
    --------
    from elevenlabs.agent_workflows import Destination, Workflow

    wf = Workflow()
    triage = wf.converse("triage", "Find out what the caller needs")
    lookup = triage.when("Caller gave an order number").tool("lookup_order", ["tool_123"])
    lookup.on_result(
        success=lambda ok: ok.converse("resolve", "Explain the order status").end(),
        failure=lambda failed: failed.transfer("human", Destination.phone("+15551234567")),
    )

    client.conversational_ai.agents.update(agent_id, workflow=wf.build())
    """

    def __init__(self, *, prevent_subagent_loops: typing.Optional[bool] = None) -> None:
        """`prevent_subagent_loops` stops the conversation from re-entering a subagent it already visited."""
        super().__init__(WorkflowGraph())
        self._graph.add_node(self._graph.start_id, {"type": "start"})
        self._graph.prevent_subagent_loops = prevent_subagent_loops

    @staticmethod
    def from_agent(
        agent: typing.Union[GetAgentResponseModel, AgentWorkflowResponseModel, AgentWorkflowRequestModel],
    ) -> Workflow:
        """
        Loads the workflow of an existing agent so it can be edited. Accepts the result of `agents.get()` or its
        `workflow` field. Node ids, editor positions and edge order are kept.
        """
        workflow = agent if hasattr(agent, "nodes") else getattr(agent, "workflow", None)
        wf = Workflow()
        if workflow is not None:
            wf._graph.load(to_wire(workflow))
        return wf

    @staticmethod
    def from_json(data: typing.Union[str, bytes, typing.Mapping[str, typing.Any]]) -> Workflow:
        """
        Loads a workflow stored as API-format JSON (snake_case), for example from `to_json_string()` or a CLI
        `agent_configs/*.json` file. Accepts a JSON string or a parsed dict, holding either the workflow itself or
        a whole agent config with a `workflow` key.
        """
        parsed = json.loads(data) if isinstance(data, (str, bytes)) else data
        raw = parsed["workflow"] if isinstance(parsed, typing.Mapping) and "workflow" in parsed else parsed
        wf = Workflow()
        wf._graph.load(raw or {})
        return wf

    @property
    def start_id(self) -> str:
        """The id of the start node: `"start_node"`, the id the API requires, or whatever a loaded workflow uses."""
        return self._graph.start_id

    @property
    def node_ids(self) -> typing.List[str]:
        """Ids of every node, in the order they were added."""
        return list(self._graph.nodes)

    def when(self, condition: ConditionInput, *, back: typing.Optional[ConditionInput] = None) -> WorkflowBranch:
        """Opens a branch from the start node that is followed when `condition` holds. A string is an LLM condition."""
        return branch(self._graph, self._graph.start_id, condition, back)

    def node(self, id: str) -> WorkflowNode:
        """A handle to an existing node, for editing it or going to it."""
        if id not in self._graph.nodes:
            self._graph.issue("unknown_node", f'There is no node "{id}"', id)
        return WorkflowNode(self._graph, id)

    def remove(self, id: str) -> Workflow:
        """Removes a node and every edge to or from it."""
        graph = self._graph
        if id == graph.start_id:
            graph.issue("cannot_remove_start", "The start node can't be removed", id)
            return self
        graph.nodes.pop(id, None)
        graph.edges = [edge for edge in graph.edges if edge.source != id and edge.target != id]
        return self

    def insert_between(
        self,
        source_id: str,
        target_id: str,
        insert: typing.Callable[[WorkflowBranch], typing.Optional[WorkflowNode]],
    ) -> typing.Optional[WorkflowNode]:
        """
        Splices new nodes into the edge from `source_id` to `target_id`. `insert` receives a branch carrying that
        edge's conditions and returns the last new node, which is then connected to `target_id`. Returns that
        node, or `None` if there is no such edge (`insert` isn't called) or `insert` returned nothing; `build()`
        reports both.

        Examples
        --------
        verify = wf.insert_between("identify", "lookup_order", lambda start: start.converse("verify", "Verify the caller"))
        if verify is not None:
            verify.when("Caller can't verify").end(id="unverified")
        """
        graph = self._graph
        index = next(
            (i for i, edge in enumerate(graph.edges) if edge.source == source_id and edge.target == target_id), None
        )
        if index is None:
            graph.issue(
                "unknown_edge", f'There is no edge from "{source_id}" to "{target_id}" to insert into', source_id
            )
            return None
        original = graph.edges.pop(index)
        before = len(graph.edges)
        last = insert(
            WorkflowBranch(
                graph,
                EdgeOrigin(
                    source=source_id,
                    forward_condition=original.forward_condition or Condition.always().to_wire(),
                    backward_condition=original.backward_condition,
                ),
            )
        )

        # Put the first new edge back where the original was, so the source's edge order is unchanged.
        first_hop = next(
            (i for i in range(before, len(graph.edges)) if graph.edges[i].source == source_id),
            None,
        )
        if first_hop is not None:
            edge = graph.edges.pop(first_hop)
            graph.edges.insert(index, edge)
            loaded = graph.loaded_order.get(source_id)
            if loaded is not None:
                for slot, loaded_edge in enumerate(loaded):
                    if loaded_edge is original:
                        loaded[slot] = edge
                        break

        if not isinstance(last, WorkflowNode):
            graph.issue(
                "missing_insert_result",
                f'insert_between("{source_id}", "{target_id}") must return the last inserted node',
                source_id,
            )
            return None
        if last.type == "tool":
            last.on_success().go_to(target_id)
        else:
            last.go_to(target_id)
        return last

    def build(
        self, *, on_warning: typing.Optional[typing.Callable[[WorkflowIssue], typing.Any]] = None
    ) -> AgentWorkflowRequestModel:
        """
        Validates the workflow and returns it as the model `agents.create()` and `agents.update()` accept.
        `on_warning` is called for each non-fatal problem, such as a node that can't be reached from the start.

        Raises
        ------
        WorkflowValidationError
            Listing every problem, if the workflow is invalid.
        """
        return typing.cast(
            AgentWorkflowRequestModel,
            construct_type(type_=AgentWorkflowRequestModel, object_=self._to_wire(on_warning)),
        )

    def to_json(self) -> WireDict:
        """
        The workflow in API format (snake_case keys, sorted at every level), for storing as config. Validates like
        `build()`.
        """
        return typing.cast(WireDict, canonical(self._to_wire(None)))

    def to_json_string(self) -> str:
        """`to_json()` as a string with 2-space indentation and a trailing newline: the canonical file format."""
        return json.dumps(self.to_json(), indent=2, ensure_ascii=False) + "\n"

    def _origin(self) -> EdgeOrigin:
        return EdgeOrigin(source=self._graph.start_id, forward_condition=Condition.always().to_wire())

    def _to_wire(self, on_warning: typing.Optional[typing.Callable[[WorkflowIssue], typing.Any]]) -> WireDict:
        graph = self._graph
        issues = validate(graph)
        errors = [issue for issue in issues if issue.severity == "error"]
        if errors:
            raise WorkflowValidationError(errors)
        if on_warning is not None:
            for warning in issues:
                if warning.severity == "warning":
                    on_warning(warning)

        # An edge that goes back the way another one came is sent as that edge's backward condition.
        merges = reverse_edge_merges(graph)
        kept = [edge for i, edge in enumerate(graph.edges) if i not in merges]
        id_of = {edge: edge_id for edge, edge_id in zip(kept, _assign_edge_ids(kept))}
        positions = layout(graph)
        outgoing: typing.Dict[str, typing.List[GraphEdge]] = {}
        edges: WireDict = {}
        for i, edge in enumerate(graph.edges):
            into = merges.get(i)
            if into is not None:
                reverse = graph.edges[into]
                outgoing.setdefault(edge.source, []).append(reverse)
                edges[id_of[reverse]]["backward_condition"] = edge.forward_condition
                continue
            outgoing.setdefault(edge.source, []).append(edge)
            # The API lists an edge with a backward condition among its target's outgoing edges as well.
            if edge.backward_condition is not None:
                outgoing.setdefault(edge.target, []).append(edge)
            wire: WireDict = {**edge.extra, "source": edge.source, "target": edge.target}
            if edge.forward_condition is not None:
                wire["forward_condition"] = edge.forward_condition
            if edge.backward_condition is not None:
                wire["backward_condition"] = edge.backward_condition
            edges[id_of[edge]] = wire

        nodes = {
            node_id: {
                **model,
                "position": positions[node_id],
                "edge_order": [
                    id_of[edge] for edge in _edge_order(graph.loaded_order.get(node_id, []), outgoing.get(node_id, []))
                ],
            }
            for node_id, model in graph.nodes.items()
        }
        workflow: WireDict = {"nodes": nodes, "edges": edges}
        if graph.prevent_subagent_loops is not None:
            workflow["prevent_subagent_loops"] = graph.prevent_subagent_loops
        return typing.cast(WireDict, deep_copy(workflow))


def _edge_order(loaded: typing.List[GraphEdge], current: typing.List[GraphEdge]) -> typing.List[GraphEdge]:
    """A loaded node's order for the edges it still has, then any others in edge-list order."""
    kept = [edge for edge in loaded if edge in current]
    return [*kept, *(edge for edge in current if edge not in kept)]


def _assign_edge_ids(edges: typing.List[GraphEdge]) -> typing.List[str]:
    """Loaded edges keep their ids. New ones get `source__target`, with `__2`, `__3`... on collision."""
    taken = {edge.id for edge in edges if edge.id is not None}
    ids = []
    for edge in edges:
        if edge.id is not None:
            ids.append(edge.id)
            continue
        base = f"{edge.source}__{edge.target}"
        edge_id = base
        n = 2
        while edge_id in taken:
            edge_id = f"{base}__{n}"
            n += 1
        taken.add(edge_id)
        ids.append(edge_id)
    return ids
