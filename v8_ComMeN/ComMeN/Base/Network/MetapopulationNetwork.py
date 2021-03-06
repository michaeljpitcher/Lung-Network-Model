#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

import math
import logging
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

    def __init__(self, compartments, nodes, edges, events):
        nx.Graph.__init__(self)

        self.compartments = compartments

        self.node_list = []

        # Nodes
        for n in nodes:
            self.add_node(n)

        self.node_list = sorted(self.node_list, key=lambda node: node.node_id)

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

    def seed_network_node_type(self, node_type, seeding):
        nodes = [n for n in self.nodes() if isinstance(n, node_type)]
        for compartment in seeding:
            for node in nodes:
                node.update_subpopulation(compartment, seeding[compartment])

    def seed_network_node_id(self, node_id, seeding):
        node = [n for n in self.nodes() if n.node_id == node_id]
        assert len(node) == 1, "Node {0} not found"
        node = node[0]
        for compartment in seeding:
            node.update_subpopulation(compartment, seeding[compartment])

    def add_node(self, n, attr_dict=None, **attr):
        assert isinstance(n, Patch), "Node {0} is not a Patch object".format(n)
        assert len([k for k in self.node_list if k.node_id == n.node_id]) == 0, "Node with ID {0} already exists"\
            .format(n.node_id)


        nx.Graph.add_node(self, n)
        self.node_list.append(n)

    def add_edge(self, u, v, attr_dict=None, **attr):
        assert self.has_node(u), "Node {0} not present in network".format(u)
        assert self.has_node(v), "Node {0} not present in network".format(v)
        assert EDGE_TYPE in attr_dict.keys(), "Edge type not specified for edge {0} - {1}".format(u, v)
        nx.Graph.add_edge(self, u, v, attr_dict)
        # Add edges to neighbours
        u.neighbours.append((v, attr_dict))
        # Only add second neighbour if nodes are distinct (avoids adding self twice to neighbours)
        if u != v:
            v.neighbours.append((u, attr_dict))

    def run(self, start_time=0, time_limit=0, run_id=None, console_output=True, debug=None, record_steps=1):

        if start_time > 0:
            self.time = start_time

        print "ComMen Simulation - time limit:", time_limit
        csv_file = None
        csv_writer = None
        record_counter = 0.0

        if debug:
            filename = str(debug) + '.log'
            print "Logging to:", filename
            logging.basicConfig(filename=filename, format='%(asctime)s:%(levelname)s:%(message)s',
                                level=logging.DEBUG)
            logging.debug("Running ComMen Simulation - Class:{0} - runid:{1}".format(self.__class__.__name__, run_id))

        if run_id:
            filename = str(run_id) + '.csv'
            csv_file = open(filename, 'w')
            print "Data output to:", filename
            csv_writer = csv.DictWriter(csv_file, fieldnames=[TIMESTEP, NODE_ID] + self.compartments)
            csv_writer.writeheader()
            self.record_data(csv_writer)

        while self.time < time_limit:
            if console_output and record_counter % record_steps == 0:
                self.timestep_print()

            """ Gillespie simulation - derived from:
            [1] D. T. Gillespie, A general method for numerically simulating the stochastic time evolution of coupled
            chemical reactions, J. Comput. Phys., vol. 22, no. 4, pp. 403-434, 1976. doi:10.1016/0021-9991(76)90041-3"""
            for e in self.events:
                e.update_rate(self)
            total_rate = sum([e.rate for e in self.events])

            if total_rate == 0:
                print "0% of event occurring - ending simulation"
                return
            elif self.end_simulation():
                return

            # Calculate the timestep tau based on the total rates
            r1 = np.random.random()
            tau = (1.0 / total_rate) * math.log(1.0 / r1)

            # Calculate which event happens based on their individual rates
            r2 = np.random.random() * total_rate
            running_total = 0
            for e in self.events:
                running_total += e.rate
                if running_total >= r2:
                    e.update_network(self)
                    logging.debug("Event performed: " + e.__class__.__name__ + ". Time now:" + str(self.time + tau))
                    break

            self.time += tau
            record_counter += 1.0
            if run_id and record_counter % record_steps == 0:
                self.record_data(csv_writer)

        if console_output:
            self.timestep_print()
        if run_id is not None:
            csv_file.close()

    def record_data(self, csv_writer):
        for node in self.node_list:
            row = {TIMESTEP: self.time, NODE_ID: node.node_id}
            for compartment in self.compartments:
                row[compartment] = node.subpopulations[compartment]
            csv_writer.writerow(row)

    def timestep_print(self):
        print "t=", self.time

    def end_simulation(self):
        # Can be overridden to allow simulation to end at a given point
        return False
