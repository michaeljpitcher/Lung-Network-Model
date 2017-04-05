#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from BaseClasses import *
from Patch import Patch
from Events.Event import Event
import networkx as nx
import numpy as np
import math

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MetapopulationNetwork(nx.Graph):

    def __init__(self, compartments, nodes, edges, events_and_node_types):
        nx.Graph.__init__(self)

        self.compartments = compartments

        # Nodes
        for n in nodes:
            self.add_node(n)

        # Edges
        for (node1, node2, edge_data) in edges:
            self.add_edge(node1, node2, edge_data)

        # Events
        assert isinstance(events_and_node_types, dict), "Supplied events must be of form - key:event, value:node_type"
        for event in events_and_node_types:
            assert isinstance(event, Event), "{0} is not an instance of Event class".format(event)
            for node_type in events_and_node_types[event]:
                viable_nodes = [n for n in nodes if isinstance(n, node_type)]
                assert len(viable_nodes) > 0, "Node type {0} does not exist in network".format(node_type)
                event.attach_nodes(viable_nodes)

        self.events = events_and_node_types.keys()

        self.time = 0.0

    def add_node(self, n, attr_dict=None, **attr):
        assert isinstance(n, Patch), "Node {0} is not a Patch object".format(n)
        nx.Graph.add_node(self, n)

    def add_edge(self, u, v, attr_dict=None, **attr):
        # TODO - better error messages
        assert self.has_node(u), "Node {0} not present in network".format(u)
        assert self.has_node(v), "Node {0} not present in network".format(v)
        assert EDGE_TYPE in attr_dict.keys(), "Edge type not specified for edge {0} - {1}".format(u, v)
        nx.Graph.add_edge(self, u, v, attr_dict)

    def run(self, time_limit=0):

        while self.time < time_limit:
            self.timestep_print()
            for e in self.events:
                e.update_rate(self)
            total_rate = sum([e.rate for e in self.events])
            if total_rate == 0:
                print "0% of event occurring"
                return

            # Calculate the timestep delta based on the total rates
            dt = (1.0 / total_rate) * math.log(1.0 / np.random.random())

            # Calculate which event happens based on their individual rates
            r = np.random.random() * total_rate
            running_total = 0
            for e in self.events:
                running_total += e.rate
                if running_total > r:
                    e.update_network(self)
                    break

            self.time += dt
        self.timestep_print()

    def timestep_print(self):
        print "t=", self.time

    def get_neighbouring_edges(self, node, edge_type=None):
        # TODO - may be slow to calculate this all the time, better to do it once and save
        if not edge_type:
            return [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)]
        else:
            return [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)
                                  if data[EDGE_TYPE] == edge_type]