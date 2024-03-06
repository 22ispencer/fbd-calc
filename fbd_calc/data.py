from enum import Enum
from pydantic import BaseModel


class SupportEnum(str, Enum):
    none = "none"
    x = "x"
    y = "y"
    xy = "xy"
    tfm = "tfm"


class Force(BaseModel):
    X: float
    Y: float


class Node(BaseModel):
    X: float
    Y: float
    support: SupportEnum = SupportEnum.none
    forces: list[Force] = []

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y


class Member(BaseModel):
    NODE_1: int
    NODE_2: int

    def __eq__(self, other):
        return {self.NODE_1, self.NODE_2} == {other.NODE_1, other.NODE_2}


class AppData(BaseModel):
    nodes: list[Node] = []
    members: list[Member] = []
