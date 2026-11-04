import dataclasses
import typing

from ._wire import WireDict, deep_copy, to_wire
from .destination import Destination
from .errors import WorkflowIssue


# Compared by identity: two edges with the same fields are still two edges.
@dataclasses.dataclass(eq=False)
class GraphEdge:
    source: str
    target: str
    forward_condition: typing.Optional[WireDict] = None
    backward_condition: typing.Optional[WireDict] = None
    # Set for edges loaded from an existing workflow; generated at build time otherwise.
    id: typing.Optional[str] = None
    # Other fields of a loaded edge, such as `reroutes` (editor bend points), written back as they were.
    extra: WireDict = dataclasses.field(default_factory=dict)


# Canonical option name -> API field, per node type.
FIELDS: typing.Dict[str, typing.Dict[str, str]] = {
    "start": {"position": "position"},
    "end": {"position": "position"},
    "override_agent": {
        "position": "position",
        "prompt": "additional_prompt",
        "label": "label",
        "tool_ids": "additional_tool_ids",
        "knowledge_base": "additional_knowledge_base",
        "conversation_config": "conversation_config",
        "entry_behavior": "entry_behavior",
    },
    "tool": {"position": "position"},
    "phone_number": {
        "position": "position",
        "transfer_type": "transfer_type",
        "custom_sip_headers": "custom_sip_headers",
        "sip_refer_play_dialtone": "sip_refer_play_dialtone",
        "uui": "uui",
        "post_dial_digits": "post_dial_digits",
    },
    "standalone_agent": {
        "position": "position",
        "delay_ms": "delay_ms",
        "transfer_message": "transfer_message",
        "enable_transferred_agent_first_message": "enable_transferred_agent_first_message",
        "preserve_client_tts_overrides": "preserve_client_tts_overrides",
        "preserve_voice_settings": "preserve_voice_settings",
    },
}

NODE_KIND: typing.Dict[str, str] = {
    "start": "start",
    "end": "end",
    "override_agent": "subagent",
    "tool": "tool",
    "phone_number": "phone/SIP transfer",
    "standalone_agent": "agent transfer",
}

_TRANSFER_TYPES = ("phone_number", "standalone_agent")


class WorkflowGraph:
    """Mutable state shared by a `Workflow` and every node handle created from it. Nodes are kept in wire format."""

    def __init__(self) -> None:
        self.nodes: typing.Dict[str, WireDict] = {}
        self.edges: typing.List[GraphEdge] = []
        self.issues: typing.List[WorkflowIssue] = []
        self.start_id = "start_node"
        # Each loaded node's edge_order, as edges. build() keeps this order and appends edges added since.
        self.loaded_order: typing.Dict[str, typing.List[GraphEdge]] = {}
        self.prevent_subagent_loops: typing.Optional[bool] = None

    def add_node(self, id: str, model: WireDict) -> None:
        existing = self.nodes.get(id)
        if existing is None:
            self.nodes[id] = model
        elif not (existing.get("type") == "end" and model.get("type") == "end"):
            self.issue("duplicate_node_id", f'Node id "{id}" is used by more than one node', id)

    def issue(self, code: typing.Any, message: str, node_id: typing.Optional[str]) -> None:
        self.issues.append(WorkflowIssue(code=code, severity="error", message=message, node_id=node_id))

    def apply_options(self, id: str, model: WireDict, options: typing.Mapping[str, typing.Any]) -> WireDict:
        """Applies canonical options to a node model. Options set to `None` are ignored."""
        rest = {key: value for key, value in options.items() if value is not None}
        destination: typing.Optional[Destination] = rest.pop("destination", None)
        tool_ids: typing.Optional[typing.Sequence[str]] = rest.pop("tool_ids", None)
        schema_overrides: typing.Optional[typing.Mapping[str, typing.Any]] = rest.pop("schema_overrides", None)
        node = dict(model)

        if destination is not None:
            if node.get("type") in _TRANSFER_TYPES:
                dest = destination.to_wire()
                if dest["type"] != node["type"]:
                    position = node.get("position")
                    node = dest
                    if position is not None:
                        node["position"] = position
                else:
                    if node["type"] == "standalone_agent":
                        # A new agent destination starts at that agent's default entry point, not the old one's
                        # node or branch.
                        for key in ("agent_id", "node_id", "branch_id"):
                            node.pop(key, None)
                    node.update(dest)
            else:
                self._invalid_option(id, "destination", node.get("type"))

        if node.get("type") == "tool":
            existing: typing.List[WireDict] = node.get("tools") or []
            ids = list(tool_ids) if tool_ids is not None else [tool["tool_id"] for tool in existing]
            for tool_id in schema_overrides or {}:
                if tool_id not in ids:
                    self.issue(
                        "invalid_option",
                        f'Node "{id}" has schema overrides for tool "{tool_id}", which it doesn\'t run',
                        id,
                    )
            tools = []
            for tool_id in ids:
                overrides = (schema_overrides or {}).get(tool_id)
                if overrides is not None:
                    overrides = to_wire(overrides)
                else:
                    overrides = next(
                        (tool.get("schema_overrides") for tool in existing if tool.get("tool_id") == tool_id), None
                    )
                tools.append(
                    {"tool_id": tool_id} if overrides is None else {"tool_id": tool_id, "schema_overrides": overrides}
                )
            node["tools"] = tools
        else:
            if schema_overrides is not None:
                self._invalid_option(id, "schema_overrides", node.get("type"))
            if tool_ids is not None:
                rest["tool_ids"] = list(tool_ids)

        fields = FIELDS.get(node.get("type"), {})  # type: ignore[arg-type]
        for key, value in rest.items():
            field = fields.get(key)
            if field is None:
                self._invalid_option(id, key, node.get("type"))
            else:
                node[field] = to_wire(value)
        return node

    def load(self, workflow: typing.Mapping[str, typing.Any]) -> None:
        """Replaces the graph's contents with an existing wire-format workflow, keeping ids, positions and edge order."""
        self.nodes.clear()
        self.edges = []
        self.issues.clear()
        self.loaded_order.clear()
        self.prevent_subagent_loops = workflow.get("prevent_subagent_loops")

        nodes: typing.Mapping[str, WireDict] = workflow.get("nodes") or {}
        edges: typing.Mapping[str, WireDict] = workflow.get("edges") or {}
        for id, node in nodes.items():
            self.nodes[id] = {key: deep_copy(value) for key, value in node.items() if key != "edge_order"}
        self.start_id = next((id for id, node in nodes.items() if node.get("type") == "start"), "start_node")
        if self.start_id not in self.nodes:
            self.nodes[self.start_id] = {"type": "start"}

        # Rebuild the edge list in each node's edge_order, so that build() reproduces it.
        placed: typing.Dict[str, GraphEdge] = {}

        def add_edge(edge_id: str) -> None:
            edge = edges.get(edge_id)
            if edge is None or edge_id in placed:
                return
            rest = {key: deep_copy(value) for key, value in edge.items()}
            graph_edge = GraphEdge(
                id=edge_id,
                source=rest.pop("source", None),
                target=rest.pop("target", None),
                forward_condition=rest.pop("forward_condition", None),
                backward_condition=rest.pop("backward_condition", None),
                extra=rest,
            )
            placed[edge_id] = graph_edge
            self.edges.append(graph_edge)

        for id, node in nodes.items():
            order = node.get("edge_order") or []
            for edge_id in order:
                add_edge(edge_id)
            self.loaded_order[id] = [placed[edge_id] for edge_id in order if edge_id in placed]
        for edge_id in edges:
            add_edge(edge_id)

    def _invalid_option(self, id: str, option: str, node_type: typing.Any) -> None:
        kind = NODE_KIND.get(node_type, f'"{node_type}"')
        self.issue("invalid_option", f'Option "{option}" doesn\'t apply to {kind} node "{id}"', id)
