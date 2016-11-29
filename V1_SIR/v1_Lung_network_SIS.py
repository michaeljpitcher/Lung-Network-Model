import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class LungNetwork(nx.Graph):

    def __init__(self, infected_nodes):
        nx.Graph.__init__(self)

        # Network Topology
        self.add_edge(0, 1)
        self.origin = 0
        self.add_edges_from([(1, 2), (2, 3), (1, 4)])
        self.add_edges_from(
            [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15),
             (15, 16), (16, 17)])
        self.add_edges_from([(5, 18), (6, 19), (6, 20),
                                       (7, 21), (7, 22),
                                       (8, 23), (9, 24), (10, 25), (11, 26), (11, 27),
                                       (13, 28), (13, 29),
                                       (14, 30), (14, 31),
                                       (15, 32), (16, 33), (17, 34), (17, 35)])
        self.terminal_nodes = [n for n in self.nodes() if self.degree(n) == 1 and n != self.origin]
        self.non_terminal_nodes = [n for n in self.nodes() if self.degree(n) != 1]
        self.positioning = self.positioning()

        # Dynamics
        self.states = ['S','I']

        # Node populations
        self.populations = dict()
        for s in self.states:
            self.populations[s] = []

        # Seed network
        for n in self.nodes():
            if n in infected_nodes:
                self.node[n]['state'] = 'I'
                self.populations['I'].append(n)
            else:
                self.node[n]['state'] = 'S'
                self.populations['S'].append(n)

        # Data
        self.data = dict()

        # Time
        self.timestep = 0.0

    def positioning(self):
        pos = dict()
        pos[0] = (5, 10)

        pos[1] = (5, 8)
        pos[2] = (4, 7)
        pos[3] = (3.5, 5)
        pos[4] = (6, 6)
        pos[5] = (3, 8)
        pos[6] = (2.75, 8.5)
        pos[7] = (3, 4.5)
        pos[8] = (4, 4)
        pos[9] = (3.5, 3)
        pos[10] = (3, 2.5)
        pos[11] = (2.5, 2)
        pos[12] = (7, 7)
        pos[13] = (7.5, 8)
        pos[14] = (8, 7)
        pos[15] = (6.5, 5)
        pos[16] = (7.5, 4)
        pos[17] = (8, 3.5)
        pos[18] = (2.5, 7.5)
        pos[19] = (2.5, 9)
        pos[20] = (3, 9)
        pos[21] = (2, 5)
        pos[22] = (2, 4)
        pos[23] = (3.5, 4.25)
        pos[24] = (4, 2)
        pos[25] = (2.5, 3.25)
        pos[26] = (1.5, 1)
        pos[27] = (2.75, 1)
        pos[28] = (7.25, 8.5)
        pos[29] = (8, 8.5)
        pos[30] = (8.25, 7.25)
        pos[31] = (8.25, 6.75)
        pos[32] = (7, 5.5)
        pos[33] = (7.5, 3)
        pos[34] = (8.5, 4.25)
        pos[35] = (8.5, 3)

        return pos

    def display(self, title, save_name=None, node_labels=True, edge_label_values=None):
        fig = plt.figure(figsize=(10, 10))
        plt.gca().set_axis_off()

        # nodes
        # S nodes
        nx.draw_networkx_nodes(self, self.positioning, nodelist=self.populations['S'], node_size=250,
                               node_color="green")
        # I nodes
        nx.draw_networkx_nodes(self, self.positioning, nodelist=self.populations['I'], node_size=250,
                               node_color="red")

        # edges
        nx.draw_networkx_edges(self, self.positioning)

        # node labels
        if node_labels:
            nx.draw_networkx_labels(self, self.positioning, font_family='sans-serif')

        # edge labels
        if edge_label_values is not None:
            edge_labels = nx.get_edge_attributes(self, edge_label_values)
            nx.draw_networkx_edge_labels(self, self.positioning, edge_labels=edge_labels)

        plt.axis('off')
        plt.title(title)
        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png

    def record_data(self):
        self.data[self.timestep] = dict()
        for n in self.nodes():
            self.data[self.timestep][n] = n['state']


if __name__ == '__main__':
    ln = LungNetwork([0])
    ln.display('Lung')