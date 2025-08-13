"""
Contains the definition of the two kinds of nodes.

Each node will hold a number. A number can be one of two things:
1. One of the 4 starting numbers. This is the `NumberNode`.
2. The result of a binary operation from two other nodes. This is the `OpNode`.
"""


class Node:
    def __init__(self, parents: tuple):
        """
        A node carries a integer value and a list of parent nodes.
        Parent node list is either empty (case 1), or there're 2 parents (case 2).
        """
        self.value = None
        self.parents = parents

    def getValue(self):
        """
        Getter for the int value on the node.
        """
        assert self.value is not None
        return self.value

    def getParents(self):
        """
        Return the reference to the parent nodes of the current node.
        Note that this getter is both readable and writable.
        """
        assert len(self.parents) in (0, 2)
        return self.parents

    def printAllHistory(self):
        for parent in self.getParents():
            parent.printAllHistory()
        print(self)


class NumberNode(Node):
    def __init__(self, value: int):
        super().__init__(parents=[])
        self.value = value
        assert self.getParents() == []

    def __repr__(self):
        return str(self.getValue())


class OpNode(Node):
    def __init__(self, op, parents):
        assert op in ("+", "-", "*", "/")
        self.op = op

        assert len(parents) == 2
        super().__init__(parents=parents)

        self._parent_numbers = [parent.getValue() for parent in self.getParents()]
        self._parent_numbers.sort()  # .sort() is ascending
        self.parent_num_small, self.parent_num_big = self._parent_numbers
        self.eval()

    def eval(self):
        if self.op == "+":
            self.value = self.parent_num_small + self.parent_num_big
        elif self.op == "-":
            self.value = self.parent_num_big - self.parent_num_small
        elif self.op == "*":
            self.value = self.parent_num_small * self.parent_num_big
        elif self.op == "/":
            assert (
                self.parent_num_big % self.parent_num_small == 0
            ), "division nodes must take in two divisible numbers"
            self.value = self.parent_num_big // self.parent_num_small

    def __repr__(self):
        return (
            f"{self.parent_num_big} {self.op} {self.parent_num_small} -> {self.value}"
        )
