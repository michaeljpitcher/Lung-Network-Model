#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Event import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageDeathRegular(Event):

    def __init__(self, probability, macrophage_compartment, bacteria_release_compartment_from=None, bacteria_release_compartment_to=None):
        self.macrophage_compartment = macrophage_compartment
        self.bacteria_release_compartment_from = bacteria_release_compartment_from
        self.bacteria_release_compartment_to = bacteria_release_compartment_to
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment]

    def update_node(self, node, network):
        if self.bacteria_release_compartment_from is not None:
            bac_released = node.compartment_per_compartment(self.bacteria_release_compartment_from, self.macrophage_compartment)
            node.update_subpopulations(self.bacteria_release_compartment_from, -1*bac_released)
            node.update_subpopulations(self.bacteria_release_compartment_from, bac_released)
        node.update_subpopulations(self.macrophage_compartment, -1)


class MacrophageDeathByTCell(Event):

    def __init__(self, probability, macrophage_compartment, t_cell_compartment, destroy_t_cell=True, bacteria_release_compartment_from=None, bacteria_release_compartment_to=None):
        self.macrophage_compartment = macrophage_compartment
        self.t_cell_compartment = t_cell_compartment
        self.destroy_t_cell = destroy_t_cell
        self.bacteria_release_compartment_from = bacteria_release_compartment_from
        self.bacteria_release_compartment_to = bacteria_release_compartment_to
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment] * node.subpopulations[self.t_cell_compartment]

    def update_node(self, node, network):
        if self.bacteria_release_compartment_from is not None:
            bac_released = node.compartment_per_compartment(self.bacteria_release_compartment_from, self.macrophage_compartment)
            node.update_subpopulations(self.bacteria_release_compartment_from, -1*bac_released)
            node.update_subpopulations(self.bacteria_release_compartment_from, bac_released)
        node.update_subpopulations(self.macrophage_compartment, -1)
        if self.destroy_t_cell:
            node.update_subpopulations(self.t_cell_compartment, -1)


class MacrophageDeathByInfection(Event):

    def __init__(self, probability, macrophage_compartment, infection_compartments, destroy_t_cell=True, bacteria_release_compartment_from=None, bacteria_release_compartment_to=None):
        self.macrophage_compartment = macrophage_compartment
        self.infection_compartments = infection_compartments
        self.destroy_t_cell = destroy_t_cell
        self.bacteria_release_compartment_from = bacteria_release_compartment_from
        self.bacteria_release_compartment_to = bacteria_release_compartment_to
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment] * sum([node.subpopulations[c] for c in self.infection_compartments])

    def update_node(self, node, network):
        if self.bacteria_release_compartment_from is not None:
            bac_released = node.compartment_per_compartment(self.bacteria_release_compartment_from, self.macrophage_compartment)
            node.update_subpopulations(self.bacteria_release_compartment_from, -1*bac_released)
            node.update_subpopulations(self.bacteria_release_compartment_from, bac_released)
        node.update_subpopulations(self.macrophage_compartment, -1)
