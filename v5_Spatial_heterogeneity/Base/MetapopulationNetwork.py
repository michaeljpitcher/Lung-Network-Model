import math

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from v5_Spatial_heterogeneity.Base.Patch import *

EDGE_OBJECT ='edge_object'


class MetapopulationNetwork(nx.Graph):
    """ Network with added metapopulation dynamics

    Extension of a NetworkX Graph. Each node of the graph is a Patch, each of which contains subpopulations of user-
    defined species. This class builds the initial network using specified parameters, and allows simulation whereby
    events are defined in terms of rates and actions in overriding versions of this class. Patches can be specified to
    contain attributes - resulting in spatial heterogeneity over the environment.
    """

    def __init__(self, nodes, edges, species_keys):

        # Create a NetworkX graph
        nx.Graph.__init__(self)
        self.species = species_keys
        # Creating patches
        # Node list is used for obtaining a patch via the ID
        self.node_list = {}
        for node in nodes:
            assert isinstance(node, Patch), "Node {0} is not instance of Patch class".format(node.id)
            # Add to graph
            self.add_node(node)
            # Add to list
            self.node_list[node.id] = node

        # Add edges
        for (node1_index, node2_index) in edges:
            node1 = self.node_list[node1_index]
            node2 = self.node_list[node2_index]
            self.add_edge(node1, node2)
            object = edges[(node1_index, node2_index)]
            self.edge[node1][node2][EDGE_OBJECT] = object

        # Degree is stored within each Patch (to speed up degree referencing)
        for node in self.nodes():
            node.degree = self.degree(node)

        # Time
        self.time = 0.0

        # Initialise data and record
        self.data = dict()
        self.record_data()

    def display(self, node_contents_species, title="", save_name=None, show_edge_labels=True):
        """

        :param node_contents_species: List of species to display for nodes
        :param title:
        :param save_name: Filename to save as png
        :param show_edge_labels: Boolean to show edge labels
        :return:
        """
        fig = plt.figure(figsize=(10, 10))
        plt.axis('off')
        plt.title(title)

        pos = {}
        node_labels = {}
        for n in self.nodes():
            pos[n] = n.position
            node_labels[n] = ""
            if node_contents_species is not None:
                for species in node_contents_species:
                    node_labels[n] += str(n.subpopulations[species]) + ":"

        # Nodes
        nx.draw_networkx_nodes(self, pos, node_size=400, node_color="green")
        # Node labels
        nx.draw_networkx_labels(self, pos, labels=node_labels, font_family='sans-serif')
        # Edges
        nx.draw_networkx_edges(self, pos)
        # Edge labels
        if show_edge_labels:
            edge_labels = {}
            for n1, n2, data in self.edges(data=True):
                edge_labels[(n1, n2)] = data[EDGE_OBJECT]
            nx.draw_networkx_edge_labels(self, pos, edge_labels=edge_labels, font_family='sans-serif')

        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png

    def record_data(self):
        """ Save a snapshot of the network at the current timestep """
        self.data[self.time] = dict()
        for n in self.nodes():
            self.data[self.time][n.id] = n.subpopulations.copy()

    def update_node(self, patch, species, amendment):
        """
        Amend the count of a species with a node
        :param patch: The patch to be updated
        :param species: The indicator of the species to update
        :param amendment: The integer amount to amend total by (positive or negative)
        :return:
        """
        assert species in self.species, "update_node: Invalid species {0}".format(species)
        assert patch.subpopulations[species] + amendment >= 0, "update_node: Count cannot drop below zero"
        patch.subpopulations[species] += amendment

    def events(self):
        """ Rate of events and specific function for event - to be defined in overriding class """
        raise NotImplementedError

    def run(self, time_limit):
        """
        Progress the simulation until the time limit is reached. For each timestep until time limit is reached, gets the
        events and their rates, then determines stochastically which event will occur and runs it, updating the
        network.
        :param time_limit: Time limit of simulation
        :return:
        """
        print "RUNNING"
        while self.time < time_limit:

            self.timestep_output()
            # Get the events and their rates
            events = self.events()
            # Pick an event and a time (dt) for it to occur
            total = 0.0
            for (r, _) in events:
                total = total + r
            if total == 0.0:
                print "0% chance of any event - ending simulation"
                break
            # Calculate the timestep delta based on the total rates
            x = np.random.random()
            dt = (1.0 / total) * math.log(1.0 / x)
            # Calculate which event happens based on their individual rates
            x = np.random.random() * total
            event_index = 0
            # Start with first event
            (running_total, chosen_event) = events[event_index]
            while running_total < x:
                (rate_for_event, chosen_event) = events[event_index]
                running_total = running_total + rate_for_event
                event_index += 1
            # Perform the event
            chosen_event(self)
            # Increment current time and record
            self.time += dt
            self.record_data()

    def timestep_output(self):
        print "t=", self.time