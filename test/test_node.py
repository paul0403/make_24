import pytest

from make_24 import NumberNode, OpNode, simple_spawn_from_pair


#
# Basic Nodes
#


def test_number_node():
    x = NumberNode(37)
    assert x.getValue() == 37
    assert x.getParents() == []


@pytest.mark.parametrize("op, expected", [("+", 24), ("-", 12), ("*", 108), ("/", 3)])
def test_op_node(op, expected):
    x = NumberNode(6)
    y = NumberNode(18)
    res = OpNode(op, [x, y])
    assert res.getValue() == expected

    parents = res.getParents()
    assert parents[0] is x
    assert parents[1] is y


def test_chained_op_nodes():
    x = NumberNode(6)
    y = NumberNode(18)
    three = OpNode("/", [x, y])
    twelve = OpNode("-", [x, y])

    res = OpNode("/", [three, twelve])
    assert res.getValue() == 4


def test_print_all_history(capfd):
    x = NumberNode(6)
    y = NumberNode(18)
    three = OpNode("/", [x, y])
    twelve = OpNode("-", [x, y])
    res = OpNode("/", [three, twelve])

    res.printAllHistory()
    out, _ = capfd.readouterr()
    assert "18 / 6 -> 3" in out
    assert "18 - 6 -> 12" in out
    assert "12 / 3 -> 4" in out


#
# simple_spawn_from_pair
#


def test_simple_spawn_from_pair_with_division():
    a, b = NumberNode(1), NumberNode(2)
    results = simple_spawn_from_pair(a, b)
    assert len(results) == 4

    expected = [3, 1, 2, 2]
    for i, res in enumerate(results):
        assert res.getValue() == expected[i]


def test_simple_spawn_from_pair_without_division():
    a, b = NumberNode(6), NumberNode(5)
    results = simple_spawn_from_pair(a, b)
    assert len(results) == 3

    expected = [11, 1, 30]
    for i, res in enumerate(results):
        assert res.getValue() == expected[i]


if __name__ == "__main__":
    pytest.main(["-x", __file__])
