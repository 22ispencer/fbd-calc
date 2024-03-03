#!/usr/bin/env python
"""The cli application for fbd-solve"""
import cmd2
from fbd_calc.data import Member, Node, Support


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
        self.poutput(f"Node created with id: {len(self.nodes) - 1}\n")

    new_member_parser = cmd2.Cmd2ArgumentParser()
    new_member_parser.add_argument("node_1", type=int,
                                   help="the first node id")
    new_member_parser.add_argument("node_2", type=int,
                                   help="the second node id")

    @cmd2.with_argparser(new_member_parser)
    def do_new_member(self, args):
        """For adding a member to the problem"""
        self.poutput(f"node_1: {args.node_1}, node_2: {args.node_2}")

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
        self.poutput(f"{args.node_id=}, {args.x=}, {args.y=}")

    def do_print(self):
        print(self.nodes, self.members)

    def do_q(self, args):
        """Exit the application"""
        return True


def run():
    import sys
    c = App()
    sys.exit(c.cmdloop())


if __name__ == "__main__":
    run()
