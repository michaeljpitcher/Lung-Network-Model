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

        self.max_count = 0
        self.infected_nodes = []

        # Creating patches
        # Node list for obtaining a patch via the ID
        self.node_list = {}
        for node_id in range(node_count):
            # Set position
            if node_positions is not None:
                position = node_positions[node_id]
            else:
                position = (np.random.uniform(0, 10))

            # Check for each compartment if the count for this node has been specified, else set to 0
            count = dict()
            for compartment in compartments:
                if node_id in initial_loads and compartment in initial_loads[node_id]:
                    count[compartment] = initial_loads[node_id][compartment]
                else:
                    count[compartment] = 0
            # Create patch
            p = Patch(node_id, count, position)
            self.add_node(p)
            self.node_list[node_id] = p
            # Update the infected list and max count
            if sum(p.counts.values()) > 0:
                self.infected_nodes.append(p)
                self.max_count = max(self.max_count, sum(p.counts.values()))

        # Add edges
        for (node1_index, node2_index) in edges:
            weight = edges[(node1_index, node2_index)]
            patch1 = [node for node in self.nodes() if node.id == node1_index][0]
            patch2 = [node for node in self.nodes() if node.id == node2_index][0]
            self.add_edge(patch1, patch2)
            self.edge[patch1][patch2]['weight'] = weight

        # Time
        self.timestep = 0.0
        self.time_limit = time_limit

        # Data
        self.data = dict()
        self.record_data()

    def display(self, title = "", save_name=None):
        fig = plt.figure(figsize=(10, 10))
        plt.axis('off')
        plt.title(title)

        pos = {}
        node_labels = {}
        for n in self.nodes():
            pos[n] = n.position
            node_labels[n] = str(n.id) + ":" + str(sum(n.counts.values()))

        nodelist_inf = self.infected_nodes
        nodelist_sus = [n for n in self.nodes() if n not in self.infected_nodes]

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
        assert compartment in self.compartments, "update_node: Invalid compartment"
        # If previous count was 0, the node has just become infected
        if sum(node.counts.values()) == 0:
            self.infected_nodes.append(node)
        node.counts[compartment] += amendment
        assert node.counts[compartment] >= 0, "update_node: Count cannot drop below zero"
        # If new count is 0, node is no longer infected
        if sum(node.counts.values()) == 0:
            self.infected_nodes.remove(node)
        # Check the new maximum amount
        new_values = [sum(n.counts.values()) for n in self.nodes()]
        self.max_count = max(new_values)

    def transitions(self):
        raise NotImplementedError

    def run(self):
        print "RUNNING"
        while self.timestep < self.time_limit and len(self.infected_nodes) > 0:

            print self.timestep

            transitions = self.transitions()
            total = 0.0
            for (r, _) in transitions:
                total = total + r

            # calculate the timestep delta
            x = np.random.random()
            dt = (1.0 / total) * math.log(1.0 / x)

            # calculate which transition happens
            x = np.random.random() * total
            k = 0
            (xs, chosen_function) = transitions[k]
            while xs < x:
                k += 1
                (xsp, chosen_function) = transitions[k]
                xs = xs + xsp

            # perform the transition
            chosen_function(self)

            self.timestep += dt
            self.record_data()

