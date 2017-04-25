#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from Event import Event

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class Change(Event):

    def __init__(self, node_types, probability, compartment_from, compartment_to, internals_to_destroy=None):
        self.compartment_from = compartment_from
        self.compartment_to = compartment_to
        self.internals_to_destroy = internals_to_destroy
        Event.__init__(self, node_types, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.compartment_from]

    def update_node(self, node, network):
        if self.internals_to_destroy:
            for compartment in self.internals_to_destroy:
                amount = node.compartment_per_compartment(compartment, self.compartment_from)
                node.update_subpopulation(compartment, -1 * amount)
        node.update_subpopulation(self.compartment_from, -1)
        node.update_subpopulation(self.compartment_to, 1)


class ChangeByOtherCompartments(Change):

    def __init__(self, node_types, probability, compartment_from, compartment_to, external_compartments,
                 internals_to_destroy=None):
        self.influencing_compartments = external_compartments
        Change.__init__(self, node_types, probability, compartment_from, compartment_to, internals_to_destroy)

    def increment_from_node(self, node, network):
        return Change.increment_from_node(self, node, network) * \
               sum([node.subpopulations[c] for c in self.influencing_compartments])


class ChangeByLackOfOtherCompartments(Change):

    def __init__(self, node_types, probability, compartment_from, compartment_to, external_compartments,
                 internals_to_destroy=None):
        self.influencing_compartments = external_compartments
        Change.__init__(self, node_types, probability, compartment_from, compartment_to, internals_to_destroy)

    def increment_from_node(self, node, network):
        # TODO - check this: epsilon = low number
        epsilon = 0.00000001
        number_externals = sum([node.subpopulations[c] for c in self.influencing_compartments])
        if number_externals == 0:
            return Change.increment_from_node(self, node, network) * (1 / epsilon)
        else:
            return Change.increment_from_node(self, node, network) * (1 / number_externals)
