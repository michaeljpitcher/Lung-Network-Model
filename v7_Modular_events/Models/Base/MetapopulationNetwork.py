__author__ = "Michael J. Pitcher"

import numpy as np
import networkx as nx
import math
import csv
import matplotlib.pyplot as plt

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
            # Add node to the graph
            self.add_node(node)
            # Add node to the node list
            self.node_list.append(node)

        # Add edges to graph
        for (node1, node2, edge_data) in edges:
            # Check the nodes are actually on the graph
            assert node1 in nodes, "Edge node {0} not specified in network".format(node1)
            assert node2 in nodes, "Edge node {0} not specified in network".format(node2)
            # Check the edge type has been specified - only edge key that is mandatory
            assert EDGE_TYPE in edge_data.keys(), "Edge type not specified for edge {0}-{1}".format(node1, node2)
            # Add the edge to the graph
            self.add_edge(node1, node2, edge_data)

        # Events
        # Check events are of correct type
        for event in events:
            assert isinstance(event, Event), "Events specified must be instances of class Event"
        self.events = events

        # Time
        self.time = 0.0
        # self.add_node()

    def add_node(self, n, attr_dict=None, **attr):
        assert isinstance(n, Patch), "Nodes specified must be of instances of Patch class"
        for class_type in self.population_keys:
            assert class_type in n.subpopulations.keys(), "Node {0} missing key {1}".format(n, class_type)
        nx.Graph.add_node(self, n)


    def run(self, time_limit, run_id=None):
        """ Runs a simulation of the metapopulation network

        Runs continuously until time limit exceeded. Each time, loops through every node and increments each event's
        total. Rate is obtained and total rate calculated. Total rate is used to calculate the time delta (as per
        Gillespie simulation). Then an event is chosen and performed, updating the network. Repeat until time limit
        exceeded or 0% chance of any event occurring.

        :param time_limit: Time limit, function ends when limit exceeded
        :param run_id: The run ID for distinguishing this execution (specifying enables data recording)
        :return:
        """

        print "RUNNING"
        # Initial output
        self.timestep_output()
        if run_id is not None:
            csv_file = open(str(run_id) + '.csv', 'wb')
            csv_writer = csv.writer(csv_file, delimiter=',')
            header_row = ["timestep", "patch_id"] + self.population_keys
            csv_writer.writerow(header_row)
            self.record_data(csv_writer)
        # Continue until time limit reached
        while self.time < time_limit:
            # Reset all event totals to zero
            for event in self.events:
                event.total = 0
            # Update the totals for each event
            for node in self.node_list:
                for event in self.events:
                    event.total += event.increment_from_node(node, network=self)
            total_rate = sum(event.get_rate() for event in self.events)
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
            if run_id is not None:
                self.record_data(csv_writer)
        if run_id is not None:
            csv_file.close()

    def timestep_output(self):
        print "t = ", self.time

    def record_data(self, csv_writer):
        for node in self.node_list:
            row = [self.time, node.id]
            for class_type in self.population_keys:
                row.append(node.subpopulations[class_type])
            csv_writer.writerow(row)

    def get_neighbouring_edges(self, node, edge_type=None):
        # TODO - may be slow to calculate this all the time, better to do it once and save
        if not edge_type:
            return [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)]
        else:
            return [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)
                                  if data[EDGE_TYPE] == edge_type]

    def display(self, class_types_to_display, node_colours, edge_colours, title="", save_name=None):
        fig = plt.figure(figsize=(10, 10))
        plt.axis('off')
        plt.title(title)

        pos = {}
        node_labels = {}
        for n in self.nodes():
            pos[n] = n.position
            node_labels[n] = ""
            if class_types_to_display is not None:
                for species in class_types_to_display:
                    node_labels[n] += str(n.subpopulations[species]) + ":"

        # Nodes
        for node_type in node_colours:
            nodelist = [node for node in self.nodes() if isinstance(node, node_type)]
            nx.draw_networkx_nodes(self, nodelist=nodelist, pos=pos, node_size=500, node_color=node_colours[node_type])

        # Node labels
        nx.draw_networkx_labels(self, pos, labels=node_labels, font_family='sans-serif')

        # Edges
        for edge_type in edge_colours:
            edgelist = [(n1, n2) for (n1, n2, data) in self.edges(data=True) if data[EDGE_TYPE] == edge_type]
            nx.draw_networkx_edges(self, pos, edgelist=edgelist, edge_color=edge_colours[edge_type])

        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png
