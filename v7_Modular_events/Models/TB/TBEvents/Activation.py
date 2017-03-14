__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ..TBClasses import *


class Activate(Event):

    def __init__(self, macrophage_state, probability):
        self.macrophage_state = macrophage_state
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        # Spontaneous activation
        return node.subpopulations[self.macrophage_state]

    def update_network(self, chosen_node, network):
        # If infected, destroys any bacteria inside
        if self.macrophage_state in CLASSES_WITH_INTRACELLULAR:
            bacteria_to_destroy = int(round(chosen_node.subpopulations[BACTERIA_INTRACELLULAR] /
                                            chosen_node.subpopulations[self.macrophage_state]))
            chosen_node.update(BACTERIA_INTRACELLULAR, -1 * bacteria_to_destroy)
        chosen_node.update(self.macrophage_state, -1)
        chosen_node.update(MACROPHAGE_ACTIVATED, 1)


class ActivateByTCell(Activate):

    def __init__(self, macrophage_state, probability):
        Activate.__init__(self, macrophage_state, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_state] * node.subpopulations[T_CELL]
