#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

# TODO - bit too much code duplication here

from ...Pulmonary.Events.PulmonaryTranslocate import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def move_bacteria(node, neighbour, bac_compartment, mac_compartment):
    bac_number = node.compartment_per_compartment(bac_compartment, mac_compartment)
    node.update_subpopulation(bac_compartment, -1 * bac_number)
    neighbour.update_subpopulation(bac_compartment, bac_number)


class MacrophageTranslocateBronchus(TranslocateBronchus):

    def __init__(self, node_types, probability, macrophage_compartment, edge_choice_based_on_weight=False,
                 bacteria_compartment_to_translocate=None):
        self.bacteria_compartment_to_translocate = bacteria_compartment_to_translocate
        TranslocateBronchus.__init__(self, node_types, probability, macrophage_compartment, edge_choice_based_on_weight)

    def move(self, node, neighbour):
        if self.bacteria_compartment_to_translocate is not None:
            move_bacteria(node, neighbour, self.bacteria_compartment_to_translocate, self.translocate_compartment)
        TranslocateBronchus.move(self, node, neighbour)


class MacrophageTranslocateLymph(TranslocateLymph):

    def __init__(self, node_types, probability, macrophage_compartment, direction_only=True,
                 bacteria_compartment_to_translocate=None):
        self.bacteria_compartment_to_translocate = bacteria_compartment_to_translocate
        TranslocateLymph.__init__(self, node_types, probability, macrophage_compartment, direction_only)

    def move(self, node, neighbour):
        if self.bacteria_compartment_to_translocate is not None:
            move_bacteria(node, neighbour, self.bacteria_compartment_to_translocate, self.translocate_compartment)
        TranslocateLymph.move(self, node, neighbour)


class MacrophageTranslocateBlood(TranslocateBlood):

    def __init__(self, node_types, probability, macrophage_compartment, direction_only=True,
                 bacteria_compartment_to_translocate=None):
        self.bacteria_compartment_to_translocate = bacteria_compartment_to_translocate
        TranslocateBlood.__init__(self, node_types, probability, macrophage_compartment, direction_only)

    def move(self, node, neighbour):
        if self.bacteria_compartment_to_translocate is not None:
            move_bacteria(node, neighbour, self.bacteria_compartment_to_translocate, self.translocate_compartment)
        TranslocateBlood.move(self, node, neighbour)
