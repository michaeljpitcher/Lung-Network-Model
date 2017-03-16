__author__ = "Michael J. Pitcher"

from Event import *


class Change(Event):

    def __init__(self, class_from, class_to, probability):
        self.class_from = class_from
        self.class_to = class_to
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_from]

    def update_network(self, chosen_node, network):
        chosen_node.update(self.class_from, -1)
        chosen_node.update(self.class_to, 1)


class ChangeThroughOtherClass(Change):

    def __init__(self, class_from, class_to, influencing_class, probability):
        self.influencing_class = influencing_class
        Change.__init__(self, class_from, class_to, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_from] * node.subpopulations[self.influencing_class]
