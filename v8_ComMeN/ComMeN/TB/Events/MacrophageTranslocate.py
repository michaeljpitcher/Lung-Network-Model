#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Pulmonary.Events.PulmonaryTranslocate import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageTranslocateBronchus(TranslocateBronchus):

    def __init__(self, probability, macrophage_compartment, edge_choice_based_on_weight=False,
                 bacteria_compartment_to_translocate=None):
        self.bacteria_compartment_to_translocate = bacteria_compartment_to_translocate
        TranslocateBronchus.__init__(self, probability, macrophage_compartment, edge_choice_based_on_weight)

    def update_node(self, node, network):
        chosen_neighbour = self.choose_neighbour(node, network)
        if self.bacteria_compartment_to_translocate is not None:
            bac_number = node.compartment_per_compartment(self.bacteria_compartment_to_translocate,
                                                          self.translocate_compartment)
            translocate(node, chosen_neighbour, self.bacteria_compartment_to_translocate, bac_number)
        translocate(node, chosen_neighbour, self.translocate_compartment)


class MacrophageTranslocateLymph(TranslocateLymph):

    def __init__(self, macrophage_compartment, probability, direction_only=True,
                 bacteria_compartment_to_translocate=None):
        self.bacteria_compartment_to_translocate = bacteria_compartment_to_translocate
        TranslocateLymph.__init__(self, probability, macrophage_compartment, direction_only)

    def update_node(self, node, network):
        chosen_neighbour = self.choose_neighbour(node, network)
        if self.bacteria_compartment_to_translocate is not None:
            bac_number = node.compartment_per_compartment(self.bacteria_compartment_to_translocate,
                                                          self.translocate_compartment)
            translocate(node, chosen_neighbour, self.bacteria_compartment_to_translocate, bac_number)
        translocate(node, chosen_neighbour, self.translocate_compartment)
