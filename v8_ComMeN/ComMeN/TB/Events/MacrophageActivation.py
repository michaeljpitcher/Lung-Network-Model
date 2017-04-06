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


class MacrophageActivation(Event):

    def __init__(self, probability, macrophage_compartment_from, macrophage_compartment_to):
        self.macrophage_compartment_from = macrophage_compartment_from
        self.macrophage_compartment_to = macrophage_compartment_to
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment_from]

    def update_node(self, node, network):
        node.update_subpopulation(self.macrophage_compartment_from, -1)
        node.update_subpopulation(self.macrophage_compartment_to, 1)


class MacrophageActivationByInfection(Event):

    def __init__(self, probability, macrophage_compartment_from, macrophage_compartment_to, infection_compartments):
        self.macrophage_compartment_from = macrophage_compartment_from
        self.macrophage_compartment_to = macrophage_compartment_to
        self.infection_compartments = infection_compartments
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment_from] * sum(node.subpopulations[c] for c in self.infection_compartments)

    def update_node(self, node, network):
        node.update_subpopulation(self.macrophage_compartment_from, -1)
        node.update_subpopulation(self.macrophage_compartment_to, 1)


class MacrophageActivationByTCell(Event):

    def __init__(self, probability, macrophage_compartment_from, macrophage_compartment_to, t_cell_compartments):
        self.macrophage_compartment_from = macrophage_compartment_from
        self.macrophage_compartment_to = macrophage_compartment_to
        self.t_cell_compartments = t_cell_compartments
        Event.__init__(self, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.macrophage_compartment_from] * sum(node.subpopulations[c] for c in self.t_cell_compartments)

    def update_node(self, node, network):
        node.update_subpopulation(self.macrophage_compartment_from, -1)
        node.update_subpopulation(self.macrophage_compartment_to, 1)