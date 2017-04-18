#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MacrophageActivation(Change):

    def __init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to,
                 bacteria_compartment_destroy=None):
        self.bacteria_compartment_destroy = bacteria_compartment_destroy
        Change.__init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to)

    def update_node(self, node, network):
        if self.bacteria_compartment_destroy is not None:
            amount = node.compartment_per_compartment(self.bacteria_compartment_destroy,
                                                      self.compartment_from)
            node.update_subpopulation(self.bacteria_compartment_destroy, -1 * amount)
        Change.update_node(self, node, network)


class MacrophageActivationByInfection(MacrophageActivation):

    def __init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to, infection_compartments,
                 bacteria_compartment_destroy=None):
        self.infection_compartments = infection_compartments
        MacrophageActivation.__init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to,
                                      bacteria_compartment_destroy)

    def increment_from_node(self, node, network):
        return MacrophageActivation.increment_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.infection_compartments])


class MacrophageActivationByTCell(MacrophageActivation):

    def __init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to, t_cell_compartments,
                 bacteria_compartment_destroy=None):
        self.t_cell_compartments = t_cell_compartments
        MacrophageActivation.__init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to,
                                      bacteria_compartment_destroy)

    def increment_from_node(self, node, network):
        return MacrophageActivation.increment_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.t_cell_compartments])


class MacrophageDeactivation(Change):

    def __init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to):
        Change.__init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to)


class MacrophageDeactivationByLackOfInfection(MacrophageDeactivation):

    def __init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to, infection_compartments):
        self.infection_compartments = infection_compartments
        MacrophageDeactivation.__init__(self, node_types, probability, macrophage_compartment_from, macrophage_compartment_to)

    def increment_from_node(self, node, network):
        # TODO - check this: epsilon = low number
        epsilon = 0.00000001
        number_infection = sum([node.subpopulations[c] for c in self.infection_compartments])
        if number_infection == 0:
            return MacrophageDeactivation.increment_from_node(self, node, network) * (1 / epsilon)
        else:
            return MacrophageDeactivation.increment_from_node(self, node, network) * (1 / number_infection)
