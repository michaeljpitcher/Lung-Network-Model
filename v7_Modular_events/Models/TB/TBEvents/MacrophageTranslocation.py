__author__ = "Michael J. Pitcher"

from ...PulmonaryAnatomy.PulmonaryEvents.PulmonaryTranslocate import *
from ..TBClasses import *


# Static function to work out bacteria to move
def calculate_bacteria_moving(class_translocating, node):
    amounts_to_move = {class_translocating: 1}
    if class_translocating in CLASSES_WITH_INTRACELLULAR:
        bacteria_to_move = int(round(node.subpopulations[BACTERIA_INTRACELLULAR] /
                                     node.subpopulations[class_translocating]))
        amounts_to_move[BACTERIA_INTRACELLULAR] = bacteria_to_move
    return amounts_to_move


class MacrophageTranslocateBronchus(TranslocateBronchus):

    def __init__(self, macrophage_type, probability, move_by_edge_weight=True):
        TranslocateBronchus.__init__(self, macrophage_type, probability, move_by_edge_weight)

    def amounts_to_move(self, node, neighbour):
        return calculate_bacteria_moving(self.class_translocating, node)


class MacrophageTranslocateLymphatic(TranslocateLymphatic):
    def __init__(self, macrophage_to_translocate, probability):
        TranslocateLymphatic.__init__(self, macrophage_to_translocate, probability)

    def amounts_to_move(self, node, neighbour):
        return calculate_bacteria_moving(self.class_translocating, node)

