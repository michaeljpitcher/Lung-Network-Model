#!/usr/bin/env python

"""Event occurring in a metapopulation network

Long Docstring

"""

import numpy as np

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


def destroy_internals(internals, compartment, node):
    for internal_compartment in internals:
        amount = node.compartment_per_compartment(internal_compartment, compartment)
        node.update_subpopulation(internal_compartment, -1 * amount)


class Event:
    """
    Basic event class. Each event has probability of happening and state variable (amount of opportunities to happen).
    Rate is calculated by multiplying probability by state variable. If chosen to be performed, event picks a node and 
    updates the counts at that node.
    Events can be specified to occur at specific node types.
    """

    def __init__(self, node_types, probability):
        self.node_types = node_types
        self.probability = probability
        self.state_variable = 0
        self.rate = 0
        self.nodes_impacted = []

    def attach_nodes(self, nodes):
        self.nodes_impacted += nodes

    def update_rate(self, network):
        """
        Go through every node, and increment the state variable. Multiply by probability to get the rate
        :param network: 
        :return: 
        """
        self.state_variable = 0
        for node in self.nodes_impacted:
            self.state_variable += self.increment_state_variable_from_node(node, network)
        self.rate = self.probability * self.state_variable

    def increment_state_variable_from_node(self, node, network):
        # To be overriden by event subclasses
        raise NotImplementedError

    def update_network(self, network):
        """
        Pick a node, based probabilistically on how much it contributes to the state variable
        :param network: 
        :return: 
        """
        r = np.random.random() * self.state_variable
        running_total = 0
        for n in self.nodes_impacted:
            increment = self.increment_state_variable_from_node(n, network)
            assert increment >= 0, "Cannot have negative state variable increment from node"
            running_total += increment
            if running_total >= r:
                self.update_node(n, network)
                return

    def update_node(self, node, network):
        # To be overriden by event subclasses
        raise NotImplementedError
