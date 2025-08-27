import pytest

from make_24 import NumberNode, OpNode, GameState, GameDriver, GameTreeNode, api

#
# GameState
#


def test_gamestate():
    x = GameState([NumberNode(1), NumberNode(2)])
    assert x.getNode(0).getValue() == 1
    assert x.getNode(1).getValue() == 2


def test_game_won():
    x = GameState([NumberNode(24)])
    assert x.hasWon()


@pytest.mark.parametrize("numbers", [[1], [2, 3]])
def test_game_not_won(numbers):
    x = GameState([NumberNode(n) for n in numbers])
    assert not x.hasWon()

def test_print_no_solution_msg(capfd):
    api.make_24(1, 1, 1, 1)
    out, _ = capfd.readouterr()
    assert "No solution was found." in out


#
# GameTreeNode
#
def test_GameTreeNode():
    _ = GameState([NumberNode(1), NumberNode(2)])
    root = GameTreeNode(_)

    assert root.children == []
    assert len(root.state) == 2
    assert root.state[0].getValue() == 1
    assert root.state[1].getValue() == 2


def test_GameTreeNode_two_numbers_evolve():
    _ = GameState([NumberNode(1), NumberNode(2)])
    root = GameTreeNode(_)
    root.evolve()

    # Check that evolving does not change the state of the tree node itself
    assert len(root.state) == 2
    assert root.state[0].getValue() == 1
    assert root.state[1].getValue() == 2

    # Check the children
    assert len(root.children) == 4

    # e.g. Addition child consumes the numbers 1 and 2 from parent, produces a 3
    expected = [3, 1, 2, 2]  # +-*/
    for i, e in enumerate(expected):
        assert len(root.children[i].state) == 1
        assert root.children[i].state[0].getValue() == e


def test_GameTreeNode_three_numbers_evolve():
    _ = GameState([NumberNode(1), NumberNode(2), NumberNode(4)])
    root = GameTreeNode(_)
    root.evolve()

    # Check that evolving does not change the state of the tree node itself
    assert len(root.state) == 3
    assert root.state[0].getValue() == 1
    assert root.state[1].getValue() == 2
    assert root.state[2].getValue() == 4

    # Check the children
    assert len(root.children) == 4 * 3

    expected = [
        # 1. Consumes 1 and 2, leaves 4
        (4, 3),
        (4, 1),
        (4, 2),
        (4, 2),
        # 2. Consumes 1 and 4, leaves 2
        (2, 5),
        (2, 3),
        (2, 4),
        (2, 4),
        # 3. Consumes 2 and 4, leaves 1
        (1, 6),
        (1, 2),
        (1, 8),
        (1, 2),
    ]
    for i, e in enumerate(expected):
        assert len(root.children[i].state) == 2
        assert root.children[i].state[0].getValue() == e[0]
        assert root.children[i].state[1].getValue() == e[1]


#
# GameDriver
#
def test_game_driver(capfd):
    game = GameDriver(1, 2, 3, 4)
    game.run()

    out, _ = capfd.readouterr()
    assert "2 + 1 -> 3" in out
    assert "3 + 3 -> 6" in out
    assert "6 * 4 -> 24" in out


def test_arbitrary_goal(capfd):
    game = GameDriver(4, 7, 2, 1, goal=20)
    game.run()

    out, _ = capfd.readouterr()
    assert "7 + 4 -> 11" in out
    assert "11 - 1 -> 10" in out
    assert "10 * 2 -> 20" in out


if __name__ == "__main__":
    pytest.main(["-x", __file__])
