#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Destruction import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageIngestBacteria(Destroy):

    def __init__(self, probability, macrophage_compartment, bacteria_compartment, macrophage_change_compartment=None,
                 bacteria_change_compartment=None):
        self.macrophage_compartment = macrophage_compartment
        self.macrophage_change_compartment = macrophage_change_compartment
        self.bacteria_change_compartment = bacteria_change_compartment
        Destroy.__init__(self, probability, bacteria_compartment)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment] * Destroy.increment_from_node(self, node, network)

    def update_node(self, node, network):
        if self.macrophage_change_compartment:
            node.update_subpopulation(self.macrophage_compartment, -1)
            node.update_subpopulation(self.macrophage_change_compartment, 1)

        Destroy.update_node(self, node, network)

        if self.bacteria_change_compartment:
            node.update_subpopulation(self.bacteria_change_compartment, 1)


class MacrophageDestroyInternalBacteria(Destroy):

    def __init__(self, probability, macrophage_compartment, bacteria_compartment, healed_macrophage_compartment):
        self.macrophage_compartment = macrophage_compartment
        # Compartment to return macrophage to if it destroys its last bacteria
        self.healed_macrophage_compartment = healed_macrophage_compartment
        Destroy.__init__(self, probability, bacteria_compartment)

    def increment_from_node(self, node, network):
        # TODO - this isn't dependent on bacterial loads, check validity
        # If there are intracellular bacteria present, then based on number of macs, else no chance
        if node.subpopulations[self.compartment_destroyed] > 0:
            return node.subpopulations[self.macrophage_compartment]
        else:
            return 0

    def update_node(self, node, network):
        Destroy.update_node(self, node, network)
        if node.subpopulations[self.compartment_destroyed] < node.subpopulations[self.macrophage_compartment]:
            node.update_subpopulation(self.macrophage_compartment, -1)
            node.update_subpopulation(self.healed_macrophage_compartment, 1)
