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


class MacrophageDeathRegular(Destroy):

    def __init__(self, probability, macrophage_compartment, internal_bacteria_compartment=None,
                 bacteria_release_compartment_to=None):
        self.internal_bacteria_compartment = internal_bacteria_compartment
        self.bacteria_release_compartment_to = bacteria_release_compartment_to
        Destroy.__init__(self, probability, macrophage_compartment)

    def update_node(self, node, network):
        # Check if there is bacteria inside
        if self.internal_bacteria_compartment is not None:
            bac_inside = node.compartment_per_compartment(self.internal_bacteria_compartment,
                                                          self.compartment_destroyed)
            # Do bacteria change to a new type (i.e. extracellular)?
            if self.bacteria_release_compartment_to is not None:
                change(node, self.internal_bacteria_compartment, self.bacteria_release_compartment_to, bac_inside)
            else: # Bacteria are destroyed
                node.update_subpopulations(self.internal_bacteria_compartment, -1*bac_inside)
        Destroy.update_node(self, node, network)


class MacrophageDeathByTCell(MacrophageDeathRegular):

    def __init__(self, probability, macrophage_compartment, t_cell_compartment, destroy_t_cell=True,
                 internal_bacteria_compartment=None, bacteria_release_compartment_to=None):
        self.t_cell_compartment = t_cell_compartment
        self.destroy_t_cell = destroy_t_cell
        MacrophageDeathRegular.__init__(self, probability, macrophage_compartment, internal_bacteria_compartment,
                                        bacteria_release_compartment_to)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.compartment_destroyed] * node.subpopulations[self.t_cell_compartment]

    def update_node(self, node, network):
        MacrophageDeathRegular.update_node(self, node, network)
        if self.destroy_t_cell:
            node.update_subpopulations(self.t_cell_compartment, -1)


class MacrophageDeathByInfection(MacrophageDeathRegular):

    def __init__(self, probability, macrophage_compartment, infection_compartments,
                 internal_bacteria_compartment=None, bacteria_release_compartment_to=None):
        self.infection_compartments = infection_compartments
        MacrophageDeathRegular.__init__(self, probability, macrophage_compartment, internal_bacteria_compartment,
                                        bacteria_release_compartment_to)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.compartment_destroyed] * sum([node.subpopulations[c] for c in
                                                                       self.infection_compartments])
