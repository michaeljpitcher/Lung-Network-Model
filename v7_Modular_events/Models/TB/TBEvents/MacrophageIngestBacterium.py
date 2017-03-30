__author__ = "Michael J. Pitcher"

from ...Base.Events.Die import *
from ..TBClasses import *
from ...Base.Events.Change import *


class MacrophageIngestBacterium(DieByOtherClass):
    """
    A macrophage ingests a bacteria (possibly infecting the macrophage, possibly destroying the bacteria)
    """
    def __init__(self, bacterium_type, macrophage_type, probability, destroy_bacteria=False, new_macrophage_type=None):
        self.destroy_bacterium = destroy_bacteria
        if new_macrophage_type is None:
            self.new_macrophage_type = macrophage_type
        else:
            self.new_macrophage_type = new_macrophage_type

        if not self.destroy_bacterium and self.new_macrophage_type not in CLASSES_WITH_INTRACELLULAR:
            raise Exception("Class {0} cannot retain bacteria".format(self.new_macrophage_type))

        DieByOtherClass.__init__(self, bacterium_type, macrophage_type, probability)

    def update_network(self, chosen_node, network):
        DieByOtherClass.update_network(self, chosen_node, network)

        if not self.destroy_bacterium:
            chosen_node.update(BACTERIA_INTRACELLULAR, 1)

        if self.new_macrophage_type != self.class_which_kills:
            chosen_node.update(self.class_which_kills, -1)
            chosen_node.update(self.new_macrophage_type, 1)


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