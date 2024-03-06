from fbd_calc.data import Node, Member
import json


def write(nodes: list[Node],
          members: list[Member],
          filename: str = "fbd-data.json"):
    data = {
        "nodes": nodes,
        "members": members
    }

    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=2)


def read(filename: str):
    with open(filename, "r") as file:
        data: dict = json.load(file)

        if "nodes" not in data.keys():
            return False
