import collections
import typing

from .errors import WorkflowIssue
from .graph import WorkflowGraph
from .node_types import model_knows_node_type


def validate(graph: WorkflowGraph) -> typing.List[WorkflowIssue]:
    """Checks that need the finished graph. Problems found while chaining are already in `graph.issues`."""
    issues = list(graph.issues)
    ends_with_edges: typing.Set[str] = set()

    def error(code: typing.Any, message: str, node_id: str) -> None:
        issues.append(WorkflowIssue(code=code, severity="error", message=message, node_id=node_id))

    for edge in graph.edges:
        name = f'"{edge.source}" → "{edge.target}"'
        for id in (edge.source, edge.target):
            if id not in graph.nodes:
                error("unknown_node", f'Edge {name} refers to unknown node "{id}"', id)
        if edge.target == graph.start_id:
            error(
                "edge_into_start",
                f"Edge {name} points into the start node; go to the first node after it instead",
                edge.source,
            )

        source_type = graph.nodes.get(edge.source, {}).get("type")
        condition_type = (edge.forward_condition or {}).get("type")
        if source_type == "end" and edge.source not in ends_with_edges:
            ends_with_edges.add(edge.source)
            error("end_has_outgoing_edges", f'End node "{edge.source}" can\'t have outgoing edges', edge.source)
        if source_type == "tool" and condition_type != "result":
            error(
                "tool_edge_needs_result",
                f"Edge {name} leaves a tool node, so it must use on_success() or on_failure()",
                edge.source,
            )
        if source_type is not None and source_type != "tool" and condition_type == "result":
            error(
                "result_edge_needs_tool",
                f"Edge {name} uses on_success()/on_failure(), which only applies to tool nodes",
                edge.source,
            )

    for id, model in graph.nodes.items():
        if not model_knows_node_type(model.get("type")):
            issues.append(
                WorkflowIssue(
                    code="unknown_node_type",
                    severity="warning",
                    message=(
                        f'Node "{id}" has type "{model.get("type")}", which this SDK version doesn\'t model. '
                        "build() keeps it as given but can't type it, and Pydantic warns when agents.create() or "
                        "agents.update() serializes it. Upgrade the SDK, or send to_json() instead: "
                        'request_options={"additional_body_parameters": {"workflow": wf.to_json()}}'
                    ),
                    node_id=id,
                )
            )

    reachable = depths_from(graph)
    for id in graph.nodes:
        if id not in reachable:
            issues.append(
                WorkflowIssue(
                    code="unreachable_node",
                    severity="warning",
                    message=f'Node "{id}" can\'t be reached from the start node',
                    node_id=id,
                )
            )
    return issues


def depths_from(graph: WorkflowGraph) -> typing.Dict[str, int]:
    """Breadth-first depth of every node reachable from the start node, in visiting order."""
    depths = {graph.start_id: 0}
    queue = collections.deque([graph.start_id])
    while queue:
        id = queue.popleft()
        for edge in graph.edges:
            # A backward condition lets the conversation travel the edge from target to source.
            if edge.source == id:
                next_id: typing.Optional[str] = edge.target
            elif edge.target == id and edge.backward_condition is not None:
                next_id = edge.source
            else:
                next_id = None
            if next_id is not None and next_id not in depths and next_id in graph.nodes:
                depths[next_id] = depths[id] + 1
                queue.append(next_id)
    return depths
