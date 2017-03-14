__author__ = "Michael J. Pitcher"

from ...Base.Event import *
from ..TBClasses import *


class Ingest(Event):

    def __init__(self, macrophage_state, bacteria_metabolism, infect, destroy, probability):
        assert not (infect and destroy), "Cannot destroy the bacterium and infect the macrophage"
        self.macrophage_state = macrophage_state
        self.bacteria_metabolism = bacteria_metabolism
        self.macrophage_is_infected = infect
        self.bacteria_is_destroyed = destroy
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_state] * node.subpopulations[self.bacteria_metabolism]

    def update_network(self, chosen_node, network):
        chosen_node.update(self.bacteria_metabolism, -1)
        if self.macrophage_is_infected:
            chosen_node.update(self.macrophage_state, -1)
            chosen_node.update(MACROPHAGE_INFECTED, 1)
            if not self.bacteria_is_destroyed:
                chosen_node.update(BACTERIA_INTRACELLULAR, 1)
