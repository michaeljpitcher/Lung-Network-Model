__author__ = "Michael J. Pitcher"

from ...Base.Events.Die import *
from ..TBClasses import *


def release_bacteria(node, class_to_die):
    bacteria_to_release = node.type_per_type(BACTERIA_INTRACELLULAR, class_to_die)
    node.update(BACTERIA_INTRACELLULAR, -1 * bacteria_to_release)
    node.update(BACTERIA_SLOW, bacteria_to_release)


class MacrophageDeath(Die):
    def __init__(self, macrophage_class, probability, release_load=True):
        self.release_load = release_load
        Die.__init__(self, macrophage_class, probability)

    def update_network(self, chosen_node, network):
        if self.release_load and self.class_to_die in CLASSES_WITH_INTRACELLULAR:
            release_bacteria(chosen_node, self.class_to_die)

        # Kill the macrophage
        Die.update_network(self, chosen_node, network)


class TCellKillsMacrophage(DieByOtherClass):
    def __init__(self, macrophage_type, t_cell_type, probability, release_load=False, kill_t_cell=False):
        self.release_load = release_load
        self.kill_t_cell = kill_t_cell
        DieByOtherClass.__init__(self, macrophage_type, t_cell_type, probability)

    def update_network(self, chosen_node, network):
        if self.release_load and self.class_to_die in CLASSES_WITH_INTRACELLULAR:
            release_bacteria(chosen_node, self.class_to_die)

        if self.kill_t_cell:
            chosen_node.update(self.class_which_kills, -1)

        # Kill the macrophage
        Die.update_network(self, chosen_node, network)
