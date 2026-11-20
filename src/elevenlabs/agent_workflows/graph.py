from __future__ import annotations

import dataclasses
import re
import typing

from ._wire import WireDict, deep_copy, to_wire
from .destination import Destination
from .errors import WorkflowIssue

if typing.TYPE_CHECKING:
    from ..agent_tools.tool import Tool

ToolRef = typing.Union[str, "Tool"]
"""A tool by id, or a `Tool` object whose id is filled in when the workflow is built with `tool_ids`."""

_PLACEHOLDER = re.compile(r"^<tool:(.*)>$")


def tool_placeholder(name: str) -> str:
    """The placeholder a `Tool` object stands under in the graph until `build()` swaps in its id."""
    return f"<tool:{name}>"


def display_tool(id: str) -> str:
    """A tool id as shown in messages: the name, for a `Tool` object's placeholder."""
    match = _PLACEHOLDER.match(id)
    return id if match is None else match.group(1)


def node_tool_ids(model: typing.Mapping[str, typing.Any]) -> typing.List[str]:
    """The tool ids (or placeholders) a node uses: a tool node's tools, or a subagent's extra tools."""
    tools = model.get("tools") or []
    extra = model.get("additional_tool_ids") or []
    return [
        *(tool["tool_id"] for tool in tools if isinstance(tool, dict) and isinstance(tool.get("tool_id"), str)),
        *(id for id in extra if isinstance(id, str)),
    ]


def map_node_tool_ids(model: WireDict, fn: typing.Callable[[str], str]) -> WireDict:
    """A copy of a tool node or subagent with each tool id passed through `fn`. Other nodes are returned as they are."""
    if model.get("type") == "tool" and isinstance(model.get("tools"), list):
        return {
            **model,
            "tools": [
                {**tool, "tool_id": fn(tool["tool_id"])}
                if isinstance(tool, dict) and isinstance(tool.get("tool_id"), str)
                else tool
                for tool in model["tools"]
            ],
        }
    if model.get("type") == "override_agent" and isinstance(model.get("additional_tool_ids"), list):
        return {
            **model,
            "additional_tool_ids": [fn(id) if isinstance(id, str) else id for id in model["additional_tool_ids"]],
        }
    return model


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
        # `Tool` objects referenced by nodes, by placeholder.
        self.tool_refs: typing.Dict[str, Tool] = {}

    def ref_tools(self, node_id: str, refs: typing.Sequence[ToolRef]) -> typing.List[str]:
        """Swaps `Tool` objects for placeholders, remembering each one."""
        ids = []
        in_this_node: typing.Dict[str, Tool] = {}
        for ref in refs:
            if isinstance(ref, str):
                ids.append(ref)
                continue
            key = tool_placeholder(ref.name)
            known = self.tool_refs.get(key)
            # A different tool of the same name conflicts if this node or another node still uses it; one left behind
            # by a removed or edited node doesn't.
            clash = in_this_node.get(key)
            if clash is None and known is not None and self._uses_placeholder(key, node_id):
                clash = known
            in_this_node[key] = ref
            if clash is not None and clash is not ref:
                self.issue(
                    "duplicate_tool_name", f'Node "{node_id}" uses a different tool also named "{ref.name}"', node_id
                )
            self.tool_refs[key] = ref
            ids.append(key)
        return ids

    def _uses_placeholder(self, key: str, except_node_id: str) -> bool:
        return any(key in node_tool_ids(model) for id, model in self.nodes.items() if id != except_node_id)

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
        refs: typing.Optional[typing.Sequence[ToolRef]] = rest.pop("tool_ids", None)
        tool_ids = None if refs is None else self.ref_tools(id, refs)
        overrides_by_ref: typing.Optional[typing.Mapping[str, typing.Any]] = rest.pop("schema_overrides", None)
        # Overrides for a `Tool` object may be keyed by the tool's name.
        schema_overrides = (
            None
            if overrides_by_ref is None
            else {
                (tool_placeholder(key) if tool_placeholder(key) in self.tool_refs else key): value
                for key, value in overrides_by_ref.items()
            }
        )
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
                        f'Node "{id}" has schema overrides for tool "{display_tool(tool_id)}", which it doesn\'t run',
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

        # Node kinds without a dedicated field map (e.g. generated say/update_state) still accept
        # position, which is common to every node kind.
        fields = FIELDS.get(node.get("type"), {"position": "position"})  # type: ignore[arg-type]
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
