from enum import Enum


class Support(Enum):
    NONE = "none"
    X = "x"
    Y = "y"
    XY = "xy"
    TFM = "tfm"


class Force:
    X: float
    Y: float

    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y


class Node:
    X: float
    Y: float
    support: Support
    forces: list[Force] = []

    def __init__(self, x: float, y: float, support: Support,
                 forces: list[Force]):
        self.X = x
        self.Y = y
        self.support = support
        if forces is not None:
            self.forces = forces

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y


class Member:
    NODE_1: int
    NODE_2: int

    def __init__(self, node_1: int, node_2: int):
        self.NODE_1: node_1
        self.NODE_2: node_2

    def __eq__(self, other):
        return (self.NODE_1, self.NODE_2) == (other.NODE_1, other.NODE_2)
