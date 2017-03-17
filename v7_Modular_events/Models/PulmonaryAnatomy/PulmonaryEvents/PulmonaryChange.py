__author__ = "Michael J. Pitcher"

from ...Base.Events.Change import *


class ChangeByOxygen(Change):

    def __init__(self, type_change_from, type_change_to, probability, oxygen_high=True):
        self.oxygen_high = oxygen_high
        Change.__init__(self, type_change_from, type_change_to, probability)

    def increment_from_node(self, node, network):
        if self.oxygen_high:
            return node.subpopulations[self.class_from] * node.oxygen_tension
        else:
            return node.subpopulations[self.class_from] * (1/node.oxygen_tension)
