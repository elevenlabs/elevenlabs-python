import typing

from ._wire import WireDict
from .graph import WorkflowGraph
from .validate import depths_from

COLUMN_WIDTH = 300
ROW_HEIGHT = 200


def layout(graph: WorkflowGraph) -> typing.Dict[str, WireDict]:
    """
    Positions for the workflow editor. Nodes that already have a position keep it. The rest go in
    column = breadth-first depth from the start node, row = order of discovery within that column, skipping rows
    where a positioned node already sits. Unreachable nodes go in the column after the deepest one.
    """
    depths = depths_from(graph)
    last_column = max([0, *depths.values()]) + 1
    order = [*depths, *(id for id in graph.nodes if id not in depths)]
    rows: typing.Dict[int, int] = {}
    positions: typing.Dict[str, WireDict] = {}
    occupied = {
        (model["position"].get("x"), model["position"].get("y"))
        for model in graph.nodes.values()
        if model.get("position") is not None
    }

    for id in order:
        existing = graph.nodes[id].get("position")
        if existing is not None:
            positions[id] = existing
            continue
        column = depths.get(id, last_column)
        row = rows.get(column, 0)
        while (column * COLUMN_WIDTH, row * ROW_HEIGHT) in occupied:
            row += 1
        rows[column] = row + 1
        occupied.add((column * COLUMN_WIDTH, row * ROW_HEIGHT))
        positions[id] = {"x": column * COLUMN_WIDTH, "y": row * ROW_HEIGHT}
    return positions
