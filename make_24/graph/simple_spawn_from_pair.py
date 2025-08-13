from .node import OpNode, Node


def simple_spawn_from_pair(node1: Node, node2: Node):
    """
    Spawn all 4 (or 3) child states from exactly two parenet `Node`s.
    Note that these are number nodes, not game tree nodes.
    """
    result_nodes = []
    for op in ["+", "-", "*"]:
        result_nodes.append(OpNode(op, [node1, node2]))

    # Do not spawn division node if not a multiple
    a = node1.getValue()
    b = node2.getValue()
    if min(a, b) != 0 and max(a, b) % min(a, b) == 0:
        result_nodes.append(OpNode("/", [node1, node2]))

    return result_nodes
