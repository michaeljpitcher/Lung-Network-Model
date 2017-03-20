__author__ = "Michael J. Pitcher"

from ...Base.Events.Die import *
from ..TBClasses import *


class MacrophageIngestBacterium(DieByOtherClass):
    def __init__(self, bacterium_type, macrophage_type, probability, destroy_load=False):
        self.destroy_load = destroy_load
        DieByOtherClass.__init__(self, bacterium_type, macrophage_type, probability)

    def update_network(self, chosen_node, network):
        if not self.destroy_load:
            chosen_node.update(BACTERIA_INTRACELLULAR, 1)
            if self.class_which_kills == MACROPHAGE_REGULAR:
                chosen_node.update(MACROPHAGE_REGULAR, -1)
                chosen_node.update(MACROPHAGE_INFECTED, 1)


class MacrophageDestroysLoad(DieByOtherClass):
    """
    An infected macrophage destroys one intracellular bacteria
    """
    def __init__(self, probability):
        DieByOtherClass.__init__(self, BACTERIA_INTRACELLULAR, MACROPHAGE_INFECTED, probability)

    def update_network(self, chosen_node, network):
        DieByOtherClass.update_network(self, chosen_node, network)
        if chosen_node.subpopulations[BACTERIA_INTRACELLULAR] < chosen_node.subpopulations[MACROPHAGE_INFECTED]:
            chosen_node.update(MACROPHAGE_INFECTED, -1)
            chosen_node.update(MACROPHAGE_REGULAR, 1)