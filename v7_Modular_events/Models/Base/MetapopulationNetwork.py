__author__ = "Michael J. Pitcher"

import numpy as np
import networkx as nx
import math

from Patch import *
from Event import *

EDGE_TYPE = 'edge_type'


class MetapopulationNetwork(nx.Graph):
    """ A network-based metapopulation simulation framework.

    Given nodes, edges and events (where each node is a Patch object, each edge is a data dictionary and each event is
    of the Event class), a NetworkX Graph is constructed. Run function calculates the rates for each event based on the
    current state of the network. An event is chosen and performed to update the network.

    """

    def __init__(self, population_keys, nodes, edges, events):

        # Set up the NetworkX Graph
        nx.Graph.__init__(self)
        # Population keys
        self.population_keys = population_keys

        # Sort nodes by ID
        nodes.sort(key=lambda x: x.id, reverse=False)

        # Store nodes as a list for quicker processing
        self.node_list = []

        # Add nodes to graph
        for node in nodes:
            # Type check as user defined
            assert isinstance(node, Patch)
            # Check all classes have been defined within the node
            for class_type in self.population_keys:
                assert class_type in node.subpopulations.keys(), "Node {0} missing key {1}".format(node, class_type)
            # Add node to the graph
            self.add_node(node)
            # Add node to the node list
            self.node_list.append(node)

        # Add edges to graph
        for (node1, node2, edge_data) in edges:
            # Check the nodes are actually on the graph
            assert node1 in nodes, "Node {0} not specified".format(node1)
            assert node2 in nodes, "Node {0} not specified".format(node2)
            # Check the edge type has been specified - only edge key that is mandatory
            assert EDGE_TYPE in edge_data.keys(), "Edge type not specified for edge {0}-{1}".format(node1, node2)
            # Add the edge to the graph
            self.add_edge(node1, node2, edge_data)

        # Events
        # Check events are of correct type
        for event in events:
            assert isinstance(event, Event)
        self.events = events

        # Time
        self.time = 0.0

    def run(self, time_limit):
        """ Runs a simulation of the metapopulation network

        Runs continuously until time limit exceeded. Each time, loops through every node and increments each event's
        total. Rate is obtained and total rate calculated. Total rate is used to calculate the time delta (as per
        Gillespie simulation). Then an event is chosen and performed, updating the network. Repeat until time limit
        exceeded or 0% chance of any event occuring.

        :param time_limit:
        :return:
        """

        print "RUNNING"
        # Initial output
        self.timestep_output()
        # Continue until time limit reached
        while self.time < time_limit:
            # Reset all event totals to zero
            for event in self.events:
                event.total = 0
            # Loop through evert node and increment the total for every event based on node contents
            for node in self.node_list:
                for event in self.events:
                    event.total += event.increment_from_node(node, network=self)
            # Get the total rate
            total_rate = sum([event.get_rate() for event in self.events])
            # End simulation if no chance of anything happening
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
            # Pick an event
            for event in self.events:
                running_total += event.get_rate()
                if running_total > r2:
                    event.perform(network=self)
                    break
            # Increment time
            self.time += dt
            self.timestep_output()

    def timestep_output(self):
        print "t = ", self.time
