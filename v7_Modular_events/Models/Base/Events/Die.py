__author__ = "Michael J. Pitcher"

from Event import *


class Die(Event):

    def __init__(self, class_to_die, probability):
        self.class_to_die = class_to_die
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_to_die]

    def update_network(self, chosen_node, network):
        chosen_node.update(self.class_to_die, -1)


class DieByOtherClass(Die):

    def __init__(self, class_to_die, class_which_kills, probability):
        self.class_which_kills = class_which_kills
        Die.__init__(self, class_to_die, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_to_die] * node.subpopulations[self.class_which_kills]
