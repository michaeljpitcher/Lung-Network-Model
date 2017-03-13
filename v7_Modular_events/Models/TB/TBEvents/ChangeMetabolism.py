__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ..TBClasses import *


class ChangeMetabolism(Event):

    def __init__(self, bacteria_metabolism_from, bacteria_metabolism_to, probability):
        self.metabolism_from = bacteria_metabolism_from
        self.metabolism_to = bacteria_metabolism_to
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        # TODO - may be better to import BPS and do isinstance
        if node in network.node_list_bps:
            if self.metabolism_from == BACTERIA_SLOW:
                return node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension
            else:
                return node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
        else:
            return 0

    def update_network(self, chosen_node, network):
        chosen_node.update(self.metabolism_from, -1)
        chosen_node.update(self.metabolism_to, 1)