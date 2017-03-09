__author__ = "Michael J. Pitcher"

import numpy as np
import networkx as nx
import math

from Patch import *

EDGE_TYPE = 'edge_type'


class MetapopulationNetwork(nx.Graph):

    def __init__(self, population_keys, nodes, edges, events):

        # Set up the networkx Graph
        nx.Graph.__init__(self)
        # Population keys
        self.population_keys = population_keys

        # Sort nodes by ID
        nodes.sort(key=lambda x: x.id, reverse=False)

        # Store nodes as a list for quicker processing
        self.node_list = []

        # Add nodes to graph
        for node in nodes:
            assert isinstance(node, Patch)
            for class_type in self.population_keys:
                assert class_type in node.subpopulations.keys(), "Node {0} missing key {1}".format(node, class_type)
            self.add_node(node)
            self.node_list.append(node)

        # Add edges to graph
        for (node1, node2, edge_data) in edges:
            assert node1 in nodes, "Node {0} not specified".format(node1)
            assert node2 in nodes, "Node {0} not specified".format(node2)
            assert EDGE_TYPE in edge_data.keys(), "Edge type not specified for edge {0}-{1}".format(node1, node2)
            self.add_edge(node1, node2, edge_data)

        # Events
        self.events = events

        # Time
        self.time = 0.0

    def run(self, time_limit):

        print "RUNNING"
        self.timestep_output()
        while self.time < time_limit:

            for event in self.events:
                event.total = 0

            for node in self.node_list:
                for event in self.events:
                    event.total += event.increment_from_node(node, network=self)

            total_rate = sum([event.get_rate() for event in self.events])
            if total_rate == 0.0:
                self.timestep_output()
                print "0% chance of any event - ending simulation"
                break

            # Calculate the timestep delta based on the total rates
            r = np.random.random()
            dt = (1.0 / total_rate) * math.log(1.0 / r)

            # Calculate which event happens based on their individual rates
            r2 = np.random.random() * total_rate
            running_total = 0
            for event in self.events:
                running_total += event.get_rate()
                if running_total > r2:
                    event.perform(network=self)
                    break

            self.time += dt
            self.timestep_output()

    def timestep_output(self):
        print "t = ", self.time