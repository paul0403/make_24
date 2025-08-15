"""
The design is as follows:

The state of the game is completely determined by the list of current numbers.

Initially we start with 4 numbers,
i.e. init state of the game is a list of 4 `NumberNode`s.

A state can evolve into another state by consuming 2 nodes to produce a new `OpNode`.
This one evolution is a single downward edge on the game tree.

When the game state is one single `OpNode` with value 24, the game is won.

Note: usually "node" will refer to a single number, aka `NumberNode` or `OpNode`.
Nodes of the game tree will bee called `GameTreeNode`.
"""

import copy
from itertools import combinations

from make_24.graph import NumberNode, OpNode, Node, simple_spawn_from_pair


class GameState:
    """
    A single game state.
    Each game state must be frozen once created, hence the tuple.
    """

    def __init__(self, nodes):
        self.nodes = tuple(nodes)

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, index):
        return self.nodes[index]

    def getNode(self, i):
        return self.nodes[i]

    def hasWon(self, goal=24):
        return len(self.nodes) == 1 and self.nodes[0].getValue() == goal


class GameTreeNode:
    """
    A single node of the game tree.
    """

    def __init__(self, state: GameState):
        self.state = state
        self.children = []

    def addChild(self, treenode):
        self.children.append(treenode)

    def evolve(self):
        """
        Populate the children list with all possible chidlren.
        Each children consumes two numbers and produces a new number.

        This is breadth first, but let's optimize later.
        With 4 numbers the entire search tree isn't that big, so the simple soln is actually ok.
        """

        for comb in combinations(range(len(self.state)), 2):
            i, j = comb

            # Consume the two input numbers
            new_nodes = []
            for p in range(len(self.state)):
                if p != i and p != j:
                    new_nodes.append(self.state[p])
            new_nodes_save = tuple(
                new_nodes
            )  # lock for immutability across the next loop

            # Fill with the result number from those two numbers
            all_new_results = simple_spawn_from_pair(self.state[i], self.state[j])
            for res in all_new_results:
                new_nodes = list(new_nodes_save)
                new_nodes.append(res)
                new_state = GameState(tuple(new_nodes))
                new_tree_node = GameTreeNode(new_state)
                self.addChild(new_tree_node)


class GameDriver:
    """
    Main driver for the game.
    """

    def __init__(self, *numbers):
        nodes = [NumberNode(n) for n in numbers]
        self.root = GameTreeNode(GameState(nodes))
        self.cur_node = self.root
        self.hasWon = False

    def run(self):
        if self.cur_node.state.hasWon():
            self.cur_node.state[0].printAllHistory()
            self.hasWon = True
            return True
        else:
            self.cur_node.evolve()
            for child in self.cur_node.children:
                self.cur_node = child
                found = self.run()
                if found:
                    return True
        return False
