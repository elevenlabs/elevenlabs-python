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

    merged = reverse_edge_merges(graph)
    connected: typing.Set[typing.FrozenSet[str]] = set()
    for i, edge in enumerate(graph.edges):
        if i in merged:
            continue
        # The API allows one edge per pair of nodes, in either direction.
        pair = frozenset((edge.source, edge.target))
        if pair in connected:
            error(
                "duplicate_edge",
                f'Edge "{edge.source}" → "{edge.target}" connects two nodes that already have an edge between them, '
                "and the API allows only one. Give the existing edge a different condition, or remove one",
                edge.source,
            )
        connected.add(pair)

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


def reverse_edge_merges(graph: WorkflowGraph) -> typing.Dict[int, int]:
    """
    Edges the API stores as the backward condition of another edge: index of the later edge -> index of the
    earlier one. The later edge goes the opposite way between the same two nodes, and neither has a backward
    condition of its own.
    """
    merges: typing.Dict[int, int] = {}
    taken: typing.Set[int] = set()
    for j, later in enumerate(graph.edges):
        if later.backward_condition is not None or later.forward_condition is None:
            continue
        i = next(
            (
                k
                for k, earlier in enumerate(graph.edges[:j])
                if k not in taken
                and k not in merges
                and earlier.source == later.target
                and earlier.target == later.source
                and earlier.backward_condition is None
            ),
            None,
        )
        if i is not None:
            merges[j] = i
            taken.add(i)
    return merges


def depths_from(graph: WorkflowGraph) -> typing.Dict[str, int]:
    """
    Breadth-first depth of every node reachable from the start node, in visiting order. Edges are followed
    forward first. Only when that runs out does a backward condition lead on, from an edge's target to a source
    not yet visited, so a back edge to an ancestor never pulls its source into a shallower column.
    """
    depths: typing.Dict[str, int] = {}

    def visit(id: str, depth: int) -> None:
        depths[id] = depth
        queue = collections.deque([id])
        while queue:
            current = queue.popleft()
            for edge in graph.edges:
                if edge.source == current and edge.target not in depths and edge.target in graph.nodes:
                    depths[edge.target] = depths[current] + 1
                    queue.append(edge.target)

    visit(graph.start_id, 0)
    while True:
        back = next(
            (
                edge
                for edge in graph.edges
                if edge.backward_condition is not None
                and edge.target in depths
                and edge.source not in depths
                and edge.source in graph.nodes
            ),
            None,
        )
        if back is None:
            return depths
        visit(back.source, depths[back.target] + 1)
