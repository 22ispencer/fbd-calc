from fbd_calc.data import Force, Node, Member, SupportEnum
import json


def write(nodes: list[Node],
          members: list[Member],
          filename: str = "fbd-data.json"):
    """
    For writing to a file

    Args:
        nodes (list[Node]): The nodes to add
        members (list[Member]): The members to add
        filename (str): The name/path of the file to write to
    """

    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=2)


def read(filename: str) -> tuple[list[Node], list[Member]] | bool:
    """
    For reading from a given file

    Args:
        filename (str): The name of the input file

    Returns:
        tuple[list[Node], list[Member]] | bool: A tuple containing the list of
            nodes and the list of members, or False if the given file is an
            invalid format
    """
    with open(filename, "r") as file:
        data: dict = json.load(file)

        if "nodes" not in data.keys():
            return False

        node_data = data["nodes"]
        nodes: list[Node] = []
        for n in node_data:
            match n["support"]:
                case "x":
                    SupportEnum.X
                case "y":
                    SupportEnum.Y
                case "xy":
                    SupportEnum.XY
                case "tfm":
                    SupportEnum.tfm
                case _:
                    SupportEnum.NONE

            forces: list[Force] = []
            for f in n["forces"]:
                forces.append(Force(f["X"], f["Y"]))
            nodes.append(Node(n["x"], n["y"], ))
