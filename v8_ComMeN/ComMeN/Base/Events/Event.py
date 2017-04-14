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


class Event:

    def __init__(self, node_types, probability):
        self.node_types = node_types
        self.probability = probability
        self.total = 0
        self.rate = 0
        self.nodes_impacted = []

    def attach_nodes(self, nodes):
        self.nodes_impacted += nodes

    def update_rate(self, network):
        assert len(self.nodes_impacted) > 0, "No nodes for event {0}".format(type(self))
        self.total = 0
        for node in self.nodes_impacted:
            self.total += self.increment_from_node(node, network)
        self.rate = self.probability * self.total

    def increment_from_node(self, node, network):
        raise NotImplementedError

    def update_network(self, network):
        r = np.random.random() * self.total
        running_total = 0
        for n in self.nodes_impacted:
            running_total += self.increment_from_node(n, network)
            if running_total > r:
                self.update_node(n, network)
                return

    def update_node(self, node, network):
        raise NotImplementedError
