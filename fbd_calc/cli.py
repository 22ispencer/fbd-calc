#!/usr/bin/env python
"""The cli application for fbd-solve"""
import cmd2
from fbd_calc.data import AppData, Force, Member, Node, SupportEnum


class App(cmd2.Cmd):
    """The cli application for fbd-solve"""

    intro = "Welcome to FBD-Solve, the open source free body diagram solver."
    prompt = "> "

    app_data = AppData()

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

        self.app_data.nodes.append(Node(X=args.x,
                                        Y=args.y,
                                        support=args.support))
        self.poutput(f"Node created with id: {len(self.app_data.nodes) - 1}")

    new_member_parser = cmd2.Cmd2ArgumentParser()
    new_member_parser.add_argument("node_1", type=int,
                                   help="the first node id")
    new_member_parser.add_argument("node_2", type=int,
                                   help="the second node id")

    @cmd2.with_argparser(new_member_parser)
    def do_new_member(self, args):
        """For adding a member to the problem"""
        if not (0 <= args.node_1 <= len(self.app_data.nodes) - 1):
            self.poutput(f"invalid node: {args.node_1}")
            return
        if not (0 <= args.node_2 <= len(self.app_data.nodes) - 1):
            self.poutput(f"invalid node: {args.node_2}")
            return
        self.app_data.members.append(Member(NODE_1=args.node_1,
                                            NODE_2=args.node_2))
        self.poutput("new member created with id: "
                     f"{len(self.app_data.members) - 1}")

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
        if not (0 <= args.node_id <= len(self.app_data.nodes) - 1):
            self.poutput(f"invalid node: {args.node_id}")
            return
        self.app_data.nodes[args.node_id].forces.append(Force(X=args.x,
                                                              Y=args.y))
        self.poutput(f"Force added to node: {args.node_id}")

    def do_print(self, args):
        """Print the nodes"""
        if len(self.app_data.nodes) == 0:
            print("No data to print")
        self.poutput("---------- Nodes ----------")
        for i, node in enumerate(self.app_data.nodes):

            self.poutput(f"\n       --- Node #{i} ---\n"
                         f"pos:     ({node.X:6.5}  , {node.Y:6.5})")
            if len(node.forces) <= 0:
                continue
            for j, force in enumerate(node.forces):
                self.poutput(f"force {j}:  {force.X:6.5}i + {force.Y:6.5}j")
        if len(self.app_data.members) == 0:
            return
        self.poutput("\n--------- Members ---------\n")
        for member in self.app_data.members:
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
