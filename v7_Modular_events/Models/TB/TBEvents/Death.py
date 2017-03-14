__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ..TBClasses import *


class Die(Event):

    def __init__(self, class_type, probability, kill_load=True):
        self.class_type = class_type
        self.kill_load = kill_load
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_type]

    def update_network(self, chosen_node, network):
        if self.class_type in CLASSES_WITH_INTRACELLULAR and not self.kill_load:
            bacteria_to_redistribute = int(round(chosen_node.subpopulations[BACTERIA_INTRACELLULAR] /
                                                 chosen_node.subpopulations[self.class_type]))
            chosen_node.update(BACTERIA_SLOW, bacteria_to_redistribute)
        chosen_node.update(self.class_type, -1)


class DieIntracellularLoad(Die):

    def __init__(self, class_type, probability):
        Die.__init__(self, class_type, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_type] * node.subpopulations[BACTERIA_INTRACELLULAR]


class DieTCell(Die):

    def __init__(self, class_type, probability):
        Die.__init__(self, class_type, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.class_type] * node.subpopulations[T_CELL]
