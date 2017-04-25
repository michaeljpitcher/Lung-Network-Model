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

    def __init__(self, node_types, probability, compartment_from, compartment_to):
        self.compartment_from = compartment_from
        self.compartment_to = compartment_to
        Event.__init__(self, node_types, probability)

    def increment_from_node(self, node, network):
        return node.subpopulations[self.compartment_from]

    def update_node(self, node, network):
        node.update_subpopulation(self.compartment_from, -1)
        node.update_subpopulation(self.compartment_to, 1)


class ChangeDestroyInternals(Change):
    def __init__(self, node_types, probability, compartment_from, compartment_to,
                 internal_compartments):
        self.internal_compartments = internal_compartments
        Change.__init__(self, node_types, probability, compartment_from, compartment_to)

    def update_node(self, node, network):
        for c in self.internal_compartments:
            amount = node.compartment_per_compartment(c, self.compartment_from)
            node.update_subpopulation(c, -1 * amount)
        Change.update_node(self, node, network)
