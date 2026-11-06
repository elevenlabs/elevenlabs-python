from __future__ import annotations

import dataclasses
import typing

from ..types.conversational_config_api_model_workflow_override_input import (
    ConversationalConfigApiModelWorkflowOverrideInput,
)
from ..types.entry_behavior import EntryBehavior
from ..types.knowledge_base_locator import KnowledgeBaseLocator
from ..types.position_input import PositionInput
from ..types.transfer_type_enum import TransferTypeEnum
from ..types.uui_transfer_config import UuiTransferConfig
from ..types.workflow_phone_number_node_model_input_custom_sip_headers_item import (
    WorkflowPhoneNumberNodeModelInputCustomSipHeadersItem,
)
from ..types.workflow_phone_number_node_model_input_post_dial_digits import (
    WorkflowPhoneNumberNodeModelInputPostDialDigits,
)
from ..types.workflow_tool_locator_schema_overrides_value import WorkflowToolLocatorSchemaOverridesValue
from ._wire import WireDict
from .condition import Condition, ConditionInput, to_condition
from .destination import Destination
from .graph import GraphEdge, WorkflowGraph

# Generated models or the equivalent wire-format dicts are accepted for every nested option.
Position = typing.Union[PositionInput, typing.Mapping[str, float]]
SchemaOverrides = typing.Mapping[
    str, typing.Mapping[str, typing.Union[WorkflowToolLocatorSchemaOverridesValue, typing.Mapping[str, typing.Any]]]
]
"""Parameter overrides per tool id, keyed by dotted parameter path (for example `path_params.order_id`)."""


@dataclasses.dataclass(frozen=True)
class EdgeOrigin:
    """Where the next edge starts and which conditions it carries."""

    source: str
    forward_condition: WireDict
    backward_condition: typing.Optional[WireDict] = None


class WorkflowChain:
    """
    The verbs that add a node and connect it to the current point in the workflow. Each returns the new node, so
    linear flows chain: `wf.converse(...).when("...").tool(...)`.
    """

    def __init__(self, graph: WorkflowGraph) -> None:
        self._graph = graph

    def _origin(self) -> EdgeOrigin:
        raise NotImplementedError

    def converse(
        self,
        id: str,
        prompt: str,
        *,
        position: typing.Optional[Position] = None,
        label: typing.Optional[str] = None,
        tool_ids: typing.Optional[typing.Sequence[str]] = None,
        knowledge_base: typing.Optional[typing.Sequence[KnowledgeBaseLocator]] = None,
        conversation_config: typing.Optional[ConversationalConfigApiModelWorkflowOverrideInput] = None,
        entry_behavior: typing.Optional[EntryBehavior] = None,
    ) -> WorkflowNode:
        """
        The agent holds a conversation with `prompt` added to its instructions, until an outgoing condition holds.
        A subagent node in the API and the UI. `label` defaults to `id`; `tool_ids` and `knowledge_base` are added
        to the agent's own, and `conversation_config` overrides the agent's config while this node is active.
        """
        model = self._graph.apply_options(
            id,
            {"type": "override_agent", "label": id, "additional_prompt": prompt},
            {
                "position": position,
                "label": label,
                "tool_ids": tool_ids,
                "knowledge_base": knowledge_base,
                "conversation_config": conversation_config,
                "entry_behavior": entry_behavior,
            },
        )
        self._graph.add_node(id, model)
        return self._connect(id)

    def tool(
        self,
        id: str,
        tool_ids: typing.Sequence[str],
        *,
        position: typing.Optional[Position] = None,
        schema_overrides: typing.Optional[SchemaOverrides] = None,
    ) -> WorkflowNode:
        """Runs the tools in parallel. Branch on the result with `on_result()`, or `on_success()` and `on_failure()`."""
        model = self._graph.apply_options(
            id,
            {"type": "tool"},
            {"position": position, "schema_overrides": schema_overrides, "tool_ids": list(tool_ids)},
        )
        self._graph.add_node(id, model)
        return self._connect(id)

    def transfer(
        self,
        id: str,
        destination: Destination,
        *,
        position: typing.Optional[Position] = None,
        transfer_type: typing.Optional[TransferTypeEnum] = None,
        custom_sip_headers: typing.Optional[
            typing.Sequence[WorkflowPhoneNumberNodeModelInputCustomSipHeadersItem]
        ] = None,
        sip_refer_play_dialtone: typing.Optional[bool] = None,
        uui: typing.Optional[UuiTransferConfig] = None,
        post_dial_digits: typing.Optional[WorkflowPhoneNumberNodeModelInputPostDialDigits] = None,
        delay_ms: typing.Optional[int] = None,
        transfer_message: typing.Optional[str] = None,
        enable_transferred_agent_first_message: typing.Optional[bool] = None,
        preserve_client_tts_overrides: typing.Optional[bool] = None,
        preserve_voice_settings: typing.Optional[bool] = None,
    ) -> WorkflowNode:
        """
        Transfers the conversation to a phone number, SIP URI or another agent. `transfer_type`,
        `custom_sip_headers`, `sip_refer_play_dialtone`, `uui` and `post_dial_digits` apply to phone and SIP
        transfers; the other options apply to agent transfers.
        """
        model = self._graph.apply_options(
            id,
            destination.to_wire(),
            {
                "position": position,
                "transfer_type": transfer_type,
                "custom_sip_headers": custom_sip_headers,
                "sip_refer_play_dialtone": sip_refer_play_dialtone,
                "uui": uui,
                "post_dial_digits": post_dial_digits,
                "delay_ms": delay_ms,
                "transfer_message": transfer_message,
                "enable_transferred_agent_first_message": enable_transferred_agent_first_message,
                "preserve_client_tts_overrides": preserve_client_tts_overrides,
                "preserve_voice_settings": preserve_voice_settings,
            },
        )
        self._graph.add_node(id, model)
        return self._connect(id)

    def end(self, *, id: str = "end", position: typing.Optional[Position] = None) -> WorkflowNode:
        """Ends the conversation. Every `end()` without an id shares one end node, `"end"`."""
        self._graph.add_node(id, self._graph.apply_options(id, {"type": "end"}, {"position": position}))
        return self._connect(id)

    def go_to(
        self, target: typing.Union[WorkflowNode, str], *, back: typing.Optional[ConditionInput] = None
    ) -> WorkflowNode:
        """
        Moves the conversation to a node that already exists (or will by the time you call `build()`), for merges
        and loops. `back` is the condition for coming back along this edge, from the target to here.
        """
        return self._connect(target if isinstance(target, str) else target.id, back)

    def _connect(self, target: str, back: typing.Optional[ConditionInput] = None) -> WorkflowNode:
        origin = self._origin()
        self._graph.edges.append(
            GraphEdge(
                source=origin.source,
                target=target,
                forward_condition=origin.forward_condition,
                backward_condition=origin.backward_condition if back is None else to_condition(back).to_wire(),
            )
        )
        return WorkflowNode(self._graph, target, origin.source)


class WorkflowBranch(WorkflowChain):
    """A pending edge out of a node, opened by `when()`, `on_success()` or `on_failure()`."""

    def __init__(self, graph: WorkflowGraph, origin: EdgeOrigin) -> None:
        super().__init__(graph)
        self._from = origin

    def _origin(self) -> EdgeOrigin:
        return self._from


class WorkflowNode(WorkflowChain):
    """A handle to one node in a workflow. Handles are cheap: all state lives in the `Workflow`."""

    def __init__(self, graph: WorkflowGraph, id: str, parent_id: typing.Optional[str] = None) -> None:
        super().__init__(graph)
        self.id = id
        self._parent_id = parent_id

    @property
    def type(self) -> typing.Optional[str]:
        """The API node type, for example `"override_agent"` or `"tool"`."""
        model = self._graph.nodes.get(self.id)
        return None if model is None else model.get("type")

    def when(self, condition: ConditionInput, *, back: typing.Optional[ConditionInput] = None) -> WorkflowBranch:
        """
        Opens a branch that is followed when `condition` holds. A string is an LLM condition. `back` is the
        condition for coming back along the edge, from the new node to this one.
        """
        return branch(self._graph, self.id, condition, back)

    def up(self) -> WorkflowNode:
        """
        Returns the node this handle was chained from, so a whole workflow can be written as one chain. For a
        handle from `wf.node(id)`, that is the source of the first edge into the node. The start node, and a node
        nothing leads to, go up to the start node. Adds nothing to the workflow.
        """
        parent = self._parent_id
        if parent is None:
            parent = next(
                (edge.source for edge in self._graph.edges if edge.target == self.id and edge.source != self.id),
                self._graph.start_id,
            )
        return WorkflowNode(self._graph, parent)

    def on_success(self, *, label: typing.Optional[str] = None) -> WorkflowBranch:
        """Opens the branch followed when every tool in this tool node succeeded."""
        return branch(self._graph, self.id, Condition.success(label=label))

    def on_failure(self, *, label: typing.Optional[str] = None) -> WorkflowBranch:
        """Opens the branch followed when any tool in this tool node failed."""
        return branch(self._graph, self.id, Condition.failure(label=label))

    def on_result(
        self,
        *,
        success: typing.Optional[typing.Callable[[WorkflowBranch], typing.Any]] = None,
        failure: typing.Optional[typing.Callable[[WorkflowBranch], typing.Any]] = None,
    ) -> WorkflowNode:
        """
        Routes both outcomes of this tool node in one place. Same as calling `on_success()` and then
        `on_failure()`, so the success edge always comes first. Either may be omitted. Returns this node.
        """
        if success is not None:
            success(self.on_success())
        if failure is not None:
            failure(self.on_failure())
        return self

    def update(
        self,
        *,
        prompt: typing.Optional[str] = None,
        tool_ids: typing.Optional[typing.Sequence[str]] = None,
        destination: typing.Optional[Destination] = None,
        position: typing.Optional[Position] = None,
        label: typing.Optional[str] = None,
        knowledge_base: typing.Optional[typing.Sequence[KnowledgeBaseLocator]] = None,
        conversation_config: typing.Optional[ConversationalConfigApiModelWorkflowOverrideInput] = None,
        entry_behavior: typing.Optional[EntryBehavior] = None,
        schema_overrides: typing.Optional[SchemaOverrides] = None,
        transfer_type: typing.Optional[TransferTypeEnum] = None,
        custom_sip_headers: typing.Optional[
            typing.Sequence[WorkflowPhoneNumberNodeModelInputCustomSipHeadersItem]
        ] = None,
        sip_refer_play_dialtone: typing.Optional[bool] = None,
        uui: typing.Optional[UuiTransferConfig] = None,
        post_dial_digits: typing.Optional[WorkflowPhoneNumberNodeModelInputPostDialDigits] = None,
        delay_ms: typing.Optional[int] = None,
        transfer_message: typing.Optional[str] = None,
        enable_transferred_agent_first_message: typing.Optional[bool] = None,
        preserve_client_tts_overrides: typing.Optional[bool] = None,
        preserve_voice_settings: typing.Optional[bool] = None,
    ) -> WorkflowNode:
        """
        Changes this node's options. Only options that apply to the node's kind may be set; `build()` reports the
        rest. `prompt` applies to subagents, `tool_ids` to subagents and tool nodes, and `destination` to
        transfers. A destination of the other transfer kind changes the node's type and keeps only its position.
        """
        model = self._graph.nodes.get(self.id)
        if model is None:
            self._graph.issue("unknown_node", f'Can\'t update unknown node "{self.id}"', self.id)
        else:
            options = {
                "prompt": prompt,
                "tool_ids": tool_ids,
                "destination": destination,
                "position": position,
                "label": label,
                "knowledge_base": knowledge_base,
                "conversation_config": conversation_config,
                "entry_behavior": entry_behavior,
                "schema_overrides": schema_overrides,
                "transfer_type": transfer_type,
                "custom_sip_headers": custom_sip_headers,
                "sip_refer_play_dialtone": sip_refer_play_dialtone,
                "uui": uui,
                "post_dial_digits": post_dial_digits,
                "delay_ms": delay_ms,
                "transfer_message": transfer_message,
                "enable_transferred_agent_first_message": enable_transferred_agent_first_message,
                "preserve_client_tts_overrides": preserve_client_tts_overrides,
                "preserve_voice_settings": preserve_voice_settings,
            }
            self._graph.nodes[self.id] = self._graph.apply_options(self.id, model, options)
        return self

    def _origin(self) -> EdgeOrigin:
        return EdgeOrigin(source=self.id, forward_condition=Condition.always().to_wire())

    def __repr__(self) -> str:
        return f"WorkflowNode(id={self.id!r}, type={self.type!r})"


def branch(
    graph: WorkflowGraph, source: str, condition: ConditionInput, back: typing.Optional[ConditionInput] = None
) -> WorkflowBranch:
    return WorkflowBranch(
        graph,
        EdgeOrigin(
            source=source,
            forward_condition=to_condition(condition).to_wire(),
            backward_condition=None if back is None else to_condition(back).to_wire(),
        ),
    )
