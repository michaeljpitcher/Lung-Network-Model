#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import math

import networkx as nx
import numpy as np
import csv

from ..BaseClasses import *
from ..Events.Event import Event
from ..Node.Patch import Patch

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class MetapopulationNetwork(nx.Graph):

    def __init__(self, compartments, nodes, edges, events, seeding=None):
        nx.Graph.__init__(self)

        self.compartments = compartments

        # Nodes
        for n in nodes:
            self.add_node(n)

        # Edges
        for (node1, node2, edge_data) in edges:
            self.add_edge(node1, node2, edge_data)

        # Events
        assert len(events) > 0, "No events supplied"
        for event in events:
            assert isinstance(event, Event), "{0} is not an instance of Event class".format(event)
            assert len(event.node_types) > 0, "No node types specified for event {0}".format(event)
            for node_type in event.node_types:
                viable_nodes = [n for n in nodes if isinstance(n, node_type)]
                assert len(viable_nodes) > 0, "Node type {0} does not exist in network".format(node_type)
                event.attach_nodes(viable_nodes)

        self.events = events

        self.time = 0.0

    def seed_network(self, seeding):
        for node_id in seeding:
            node = [n for n in self.nodes() if n.node_id == node_id][0]
            for compartment in seeding[node_id]:
                value = seeding[node_id][compartment]
                node.update_subpopulation(compartment, value)

    def add_node(self, n, attr_dict=None, **attr):
        assert isinstance(n, Patch), "Node {0} is not a Patch object".format(n)
        nx.Graph.add_node(self, n)

    def add_edge(self, u, v, attr_dict=None, **attr):
        assert self.has_node(u), "Node {0} not present in network".format(u)
        assert self.has_node(v), "Node {0} not present in network".format(v)
        assert EDGE_TYPE in attr_dict.keys(), "Edge type not specified for edge {0} - {1}".format(u, v)
        nx.Graph.add_edge(self, u, v, attr_dict)
        # if attr_dict[EDGE_TYPE] in u.neighbours:
        #     u.neighbours[EDGE_TYPE].append(v)
        # else:
        #     u.neighbours[EDGE_TYPE] = [v]
        # if attr_dict[EDGE_TYPE] in v.neighbours:
        #     v.neighbours[EDGE_TYPE].append(u)
        # else:
        #     v.neighbours[EDGE_TYPE] = [u]

    def run(self, time_limit=0, run_id=None, output=True):
        csv_file = None
        csv_writer = None

        if run_id is not None:
            csv_file = open(str(run_id) + '.csv', 'wb')
            csv_writer = csv.writer(csv_file, delimiter=',')
            header_row = ["timestep", "node_id"] + self.compartments
            csv_writer.writerow(header_row)
            self.record_data(csv_writer)

        while self.time < time_limit:
            if output:
                self.timestep_print()
            for e in self.events:
                e.update_rate(self)
            total_rate = sum([e.rate for e in self.events])
            if total_rate == 0:
                print "0% of event occurring"
                return

            # Calculate the timestep delta based on the total rates
            # TODO - check
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
            if run_id is not None:
                self.record_data(csv_writer)
        if output:
            self.timestep_print()
        if run_id is not None:
            csv_file.close()

    def record_data(self, csv_writer):
        for node in self.nodes():
            row = [self.time, node.node_id]
            for compartment in self.compartments:
                row.append(node.subpopulations[compartment])
            csv_writer.writerow(row)

    def timestep_print(self):
        print "t=", self.time

    def get_neighbouring_edges(self, node, edge_type=None):
        # TODO - may be slow to calculate this all the time, better to do it once and save,
        # also hampers the unit tests because self.edges can change order
        if not edge_type:
            return [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)]
        else:
            return [(neighbour, data) for (_, neighbour, data) in self.edges(node, data=True)
                                  if data[EDGE_TYPE] == edge_type]
