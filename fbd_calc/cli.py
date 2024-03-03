#!/usr/bin/env python
"""The cli application for fbd-solve"""
import cmd2
from fbd_calc.data import Force, Member, Node, Support


class App(cmd2.Cmd):
    """The cli application for fbd-solve"""

    intro = "Welcome to FBD-Solve, the open source free body diagram solver."
    prompt = "> "

    nodes: list[Node] = []
    members: list[Member] = []

    def __init__(self):
        super().__init__()

    new_node_parser = cmd2.Cmd2ArgumentParser()
    new_node_parser.add_argument("x", type=float,
                                 help="the x position of the node")
    new_node_parser.add_argument("y", type=float,
                                 help="the y position of the node")
    new_node_parser.add_argument("-s", "--support",
                                 choices=["x", "y", "xy", "tfm", "none"],
                                 default="none",
                                 help="the type of support for the node")

    @cmd2.with_argparser(new_node_parser)
    def do_new_node(self, args):
        """For adding a node to the problem"""
        match args.support:
            case "x":
                support = Support.X
            case "y":
                support = Support.Y
            case "xy":
                support = Support.XY
            case "tfm":
                support = Support.TFM
            case _:
                support = Support.NONE

        self.nodes.append(Node(args.x, args.y, support, None))
        self.poutput(f"Node created with id: {len(self.nodes) - 1}")

    new_member_parser = cmd2.Cmd2ArgumentParser()
    new_member_parser.add_argument("node_1", type=int,
                                   help="the first node id")
    new_member_parser.add_argument("node_2", type=int,
                                   help="the second node id")

    @cmd2.with_argparser(new_member_parser)
    def do_new_member(self, args):
        """For adding a member to the problem"""
        if not (0 <= args.node_1 <= len(self.nodes) - 1):
            self.poutput(f"invalid node: {args.node_1}")
            return
        if not (0 <= args.node_2 <= len(self.nodes) - 1):
            self.poutput(f"invalid node: {args.node_2}")
            return
        new_member = Member(args.node_1, args.node_2)
        self.members.append(new_member)
        self.poutput(f"new member created with id: {len(self.members) - 1}")

    new_force_parser = cmd2.Cmd2ArgumentParser()
    new_force_parser.add_argument("node_id", type=int,
                                  help="the node to add the force to")
    new_force_parser.add_argument("x", type=float,
                                  help="the x component of the force")
    new_force_parser.add_argument("y", type=float,
                                  help="the y component of the force")

    @cmd2.with_argparser(new_force_parser)
    def do_new_force(self, args):
        """For adding a force to a node"""
        if not (0 <= args.node_id <= len(self.nodes) - 1):
            self.poutput(f"invalid node: {args.node_id}")
            return
        new_force = Force(args.x, args.y)
        (self.nodes[args.node_id]).forces.append(new_force)
        self.poutput(f"Force added to node: {args.node_id}")

    def do_print(self, args):
        """Print the nodes"""
        if len(self.nodes) == 0:
            print("No data to print")
        self.poutput("---------- Nodes ----------")
        for i, node in enumerate(self.nodes):
            self.poutput(f"\n       --- Node #{i} ---\n"
                         f"pos:     ( {node.X:6.5} , {node.Y:6.5})")
            for j, force in enumerate(node.forces):
                self.poutput(f"force {j}:  {force.X:6.5}i + {force.Y:6.5}j")
            node = None
        if len(self.members) == 0:
            return
        self.poutput("--------- Members ---------\n")
        for i, member in enumerate(self.members):
            self.poutput(f"node_1: {member.NODE_1}, node_2: {member.NODE_2}")

    def do_q(self, args):
        """Exit the application"""
        return True


def run():
    import sys
    c = App()
    sys.exit(c.cmdloop())


if __name__ == "__main__":
    run()
