import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation

class Patch:

    def __init__(self, id, compartments_counts, position=(0,0)):
        self.id = id
        self.position = position
        self.counts = compartments_counts

    def __str__(self):
        return "Patch: " + str(self.id)


class CompartmentalMetapopulationNetwork(nx.Graph):

    def __init__(self, node_count, edges, time_limit, compartments, initial_loads, node_positions=None):
        nx.Graph.__init__(self)

        self.compartments = compartments

        # For obtaining a patch via the ID
        self.node_list = {}
        for i in range(node_count):
            if node_positions is not None:
                position = node_positions[i]
            else:
                position = (np.random.uniform(0, 10))
            initialisation = initial_loads[i]
            p = Patch(i, initialisation, position)
            self.add_node(p)
            self.node_list[i] = p

        for (node1_index, node2_index) in edges:
            weight = edges[(node1_index, node2_index)]
            patch1 = [node for node in self.nodes() if node.id == node1_index][0]
            patch2 = [node for node in self.nodes() if node.id == node2_index][0]
            self.add_edge(patch1, patch2)
            self.edge[patch1][patch2]['weight'] = weight

        self.max_count = 0
        self.infected_nodes = []
        for n_index in initial_loads:
            node = self.node_list[n_index]
            node.count = initial_loads[n_index]
            self.infected_nodes.append(node)
            self.max_count = max(node.count, self.max_count)

        # Time
        self.timestep = 0.0
        self.time_limit = time_limit

        # Data
        self.data = dict()
        self.record_data()

    def display(self, title, save_name=None):
        fig = plt.figure(figsize=(10, 10))
        plt.axis('off')
        plt.title(title)

        pos = {}
        nodelist_sus = []
        nodelist_inf = []
        node_labels = {}
        for n in self.nodes():
            pos[n] = n.position
            if n.count > 0:
                nodelist_inf.append(n)
            else:
                nodelist_sus.append(n)
            node_labels[n] = str(n.id) + ":" + str(n.count)
        # Nodes
        nx.draw_networkx_nodes(self, pos, nodelist=nodelist_sus, node_size=400, node_color="green")
        nx.draw_networkx_nodes(self, pos, nodelist=nodelist_inf, node_size=400, node_color="red")
        # Node labels
        nx.draw_networkx_labels(self, pos, labels=node_labels, font_family='sans-serif')
        # Edges
        nx.draw_networkx_edges(self, pos)
        # Edge labels
        edge_labels = {}
        for n1,n2,data in self.edges(data=True):
            edge_labels[(n1,n2)] = data['weight']
        nx.draw_networkx_edge_labels(self, pos, edge_labels=edge_labels, font_family='sans-serif')

        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png

    def record_data(self):
        self.data[self.timestep] = dict()
        for n in self.nodes():
            self.data[self.timestep][n.id] = n.counts.copy()

    def update_node(self, node, compartment, amendment):
        assert compartment in self.compartments
        # If previous count was 0, the node has just become infected
        if sum(node.counts.values()) == 0:
            self.infected_nodes.append(node)
        node.count[compartment] += amendment
        assert node.counts[compartment] >= 0, "update_node: Count cannot drop below zero"
        # If new count is 0, node is no longer infected
        if sum(node.counts.values()) == 0:
            self.infected_nodes.remove(node)
        # Check the new maximum amount
        new_values = [sum(n.counts.values()) for n in self.nodes()]
        self.max_count = max(new_values)

if __name__ == '__main__':

    edges = {(0,1):10,(1,2):10,(2,3):10,(0,3):10, (1,3):10}
    compartments = ['F','S']
    initial_loads = dict()
    for i in range(0,4):
        initial_loads[i] = dict()
        initial_loads[i]['F'] = 10
        initial_loads[i]['S'] = 1
    pos = {0: (0, 0), 1: (0, 5), 2: (5,5), 3:(5, 0)}
    a = CompartmentalMetapopulationNetwork(4,edges,1,compartments,initial_loads,pos)
    #a.display("TITLE")
    a.update_node(a.node_list[0],'F',1)
    a.display("TITLE")
