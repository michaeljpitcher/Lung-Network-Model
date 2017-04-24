#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from v8_ComMeN.ComMeN.Base.Events.Change import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class PhagocyteActivation(Change):

    def __init__(self, node_types, probability, phagocyte_compartment_from, phagocyte_compartment_to,
                 bacteria_compartment_destroy=None):
        self.bacteria_compartment_destroy = bacteria_compartment_destroy
        Change.__init__(self, node_types, probability, phagocyte_compartment_from, phagocyte_compartment_to)

    def update_node(self, node, network):
        if self.bacteria_compartment_destroy is not None:
            amount = node.compartment_per_compartment(self.bacteria_compartment_destroy,
                                                      self.compartment_from)
            node.update_subpopulation(self.bacteria_compartment_destroy, -1 * amount)
        Change.update_node(self, node, network)


class PhagocyteActivationByExternals(PhagocyteActivation):

    def __init__(self, node_types, probability, phagocyte_compartment_from, phagocyte_compartment_to,
                 external_compartments, bacteria_compartment_destroy=None):
        self.external_compartments = external_compartments
        PhagocyteActivation.__init__(self, node_types, probability, phagocyte_compartment_from,
                                     phagocyte_compartment_to, bacteria_compartment_destroy)

    def increment_from_node(self, node, network):
        return PhagocyteActivation.increment_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.external_compartments])


class PhagocyteDeactivationByLackOfExternals(Change):

    def __init__(self, node_types, probability, phagocyte_compartment_from, phagocyte_compartment_to,
                 external_compartments):
        self.external_compartments = external_compartments
        Change.__init__(self, node_types, probability, phagocyte_compartment_from, phagocyte_compartment_to)

    def increment_from_node(self, node, network):
        # TODO - check this: epsilon = low number
        epsilon = 0.00000001
        number_externals = sum([node.subpopulations[c] for c in self.external_compartments])
        if number_externals == 0:
            return Change.increment_from_node(self, node, network) * (1 / epsilon)
        else:
            return Change.increment_from_node(self, node, network) * (1 / number_externals)
