import functools
import typing

import typing_extensions
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from ..types.agent_workflow_request_model_nodes_value import AgentWorkflowRequestModelNodesValue


@functools.lru_cache(maxsize=None)
def _known_node_types() -> typing.FrozenSet[str]:
    # The request model is `Annotated[Union[...], UnionMetadata(discriminant="type")]`; each member's `type`
    # field defaults to its discriminant value.
    union = typing_extensions.get_args(AgentWorkflowRequestModelNodesValue)[0]
    known = set()
    for member in typing_extensions.get_args(union):
        fields = member.model_fields if IS_PYDANTIC_V2 else member.__fields__
        known.add(fields["type"].default)
    return frozenset(known)


def model_knows_node_type(node_type: typing.Any) -> bool:
    """
    Whether this SDK version's generated request model has a member for a node type. Read from the generated
    union rather than listed here, so a regeneration that adds a node type is picked up without a change to the
    builder.
    """
    return node_type in _known_node_types()
