import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation


class Patch:

    def __init__(self, id, position=(0,0)):
        self.id = id
        self.position = position
        self.count = 0


class MetapopulationPatchWeightedNetwork(nx.Graph):
    def __init__(self, node_count, edges, p_transmit, p_growth, time_limit, initial_loads, node_positions=None):
        nx.Graph.__init__(self)

        # For obtaining a patch via the ID
        self.node_list = {}
        for i in range(node_count):
            if node_positions is not None:
                position = node_positions[i]
            else:
                position = (np.random.uniform(0, 10))
            p = Patch(i, position)
            self.add_node(p)
            self.node_list[i] = p

        for (node1_index, node2_index) in edges:
            weight = edges[(node1_index, node2_index)]
            patch1 = [node for node in self.nodes() if node.id == node1_index][0]
            patch2 = [node for node in self.nodes() if node.id == node2_index][0]
            self.add_edge(patch1, patch2)
            self.edge[patch1][patch2]['weight'] = weight

        self.rates = dict()
        self.rates['p_transmit'] = p_transmit
        self.rates['p_growth'] = p_growth

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

        self.total_transmit = 0
        self.total_growth = 0

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
            node_labels[n] = n.count
        # Nodes
        nx.draw_networkx_nodes(self, pos, nodelist=nodelist_sus, node_size=400, node_color="green")
        nx.draw_networkx_nodes(self, pos, nodelist=nodelist_inf, node_size=400, node_color="red")
        # Node labels
        nx.draw_networkx_labels(self, pos, labels=node_labels, font_family='sans-serif')
        # Edges
        nx.draw_networkx_edges(self, pos)

        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png

    def movie(self, filename, interval):
        pos = {}
        for n in self.nodes():
            pos[n] = n.position
        print "MAKING MOVIE"
        fig = plt.figure(figsize=(10, 10))
        ax = fig.gca()
        ax.set_xlim([-0.2, 10.2])
        ax.set_ylim([-0.2, 12.2])
        ax.grid(False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        node_markers = []
        for n in self.nodes_iter():
            circle = plt.Circle(pos[n], radius=0.1, zorder=2)  # node markers at top of the z-order
            ax.add_patch(circle)
            node_markers.append({'node': n.id, 'position': circle})
        for e in self.edges_iter():
            xs = [pos[e[0]][0], pos[e[1]][0]]
            ys = [pos[e[0]][1], pos[e[1]][1]]
            line = plt.Line2D(xs, ys, zorder=1, color='k')  # edges lower down the z-order
            ax.add_line(line)
        timepoints = sorted(self.data.keys())

        def update_nodes(time):
            plt.title(str(time))
            for marker in node_markers:
                node = marker['node']
                count = self.data[time][node]
                # TODO - rigged so you can actually see colour change
                if count >= 20:
                    count = 20.0
                colour = (count / 20.0, 0, 0)
                marker = marker['position']
                marker.set(color=colour)

        def init():
            update_nodes(0.0)

        def frame(i):
            update_nodes(timepoints[i])

        movie = animation.FuncAnimation(fig, frame, init_func=init, frames=len(self.data), interval=interval,
                                        blit=False)
        # plt.show()
        movie.save(filename + '.mp4', writer='ffmpeg_file')

    def record_data(self):
        self.data[self.timestep] = dict()
        for n in self.nodes():
            self.data[self.timestep][n.id] = n.count

    def update_node(self, node, amendment):
        # If previous count was 0, the node has just become infected
        if node.count == 0:
            self.infected_nodes.append(node)
        node.count += amendment
        assert node.count >= 0, "update_node: Count cannot drop below zero"
        # If new count is 0, node is no longer infected
        if node.count == 0:
            self.infected_nodes.remove(node)
        # Check the new maximum amount
        self.max_count = max([n.count for n in self.nodes()])

    def calculate_totals(self):
        # TODO - ASSUMPTION: transmission is affected by degree
        # TODO - ASSUMPTION: no maximum capacity in node
        self.total_transmit = sum([node.count * self.degree(node) for node in self.infected_nodes])
        self.total_growth = sum([node.count for node in self.infected_nodes])

    def transitions(self):
        rate_for_transmit = self.total_transmit * self.rates['p_transmit']
        rate_for_growth = self.total_growth * abs(self.rates['p_growth'])
        return [(rate_for_transmit, lambda t: self.transmit()),
                (rate_for_growth, lambda t: self.growth())]

    def transmit(self):
        r = np.random.random() * self.total_transmit
        running_total = 0
        for node in self.infected_nodes:
            running_total += node.count * self.degree(node)
            if running_total >= r:
                total_weights = sum(d['weight'] for _, _, d in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                for _, neighbour, d in self.edges(node, data=True):
                    running_total_weights += d['weight']
                    if running_total_weights > r2:
                        self.update_node(node, -1)
                        self.update_node(neighbour, 1)
                        return

    def growth(self):
        r = np.random.random() * self.total_growth
        running_total = 0
        for node in self.infected_nodes:
            running_total += node.count
            if running_total >= r:
                if self.rates['p_growth'] > 0:
                    self.update_node(node, 1)
                elif self.rates['p_growth'] < 0:
                    self.update_node(node, -1)
                return

    def run(self):
        print "RUNNING"
        while self.timestep < self.time_limit and len(self.infected_nodes) > 0:

            self.calculate_totals()

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


class LungMetapopulationWeightedNetwork(MetapopulationPatchWeightedNetwork):
    def __init__(self, p_transmit, p_growth, time_limit, initial_loads):
        # Trachea
        edges = [(0, 1)]
        # Main bronchi
        edges += [(1, 2), (2, 3), (1, 4)]
        # Lobar bronchi
        edges += [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15),
                  (15, 16), (16, 17)]
        # Segmental bronchi
        edges += [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28),
                  (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]

        edge_weights = {}
        for e in edges:
            edge_weights[e] = 0.0

        # Node positions TODO: done by eye
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
        pos[30] = (8.5, 7.5)
        pos[31] = (8.5, 6.5)
        pos[32] = (7, 5.5)
        pos[33] = (7.5, 3)
        pos[34] = (8.5, 4.25)
        pos[35] = (8.5, 3)
        MetapopulationPatchWeightedNetwork.__init__(self, 36, edge_weights, p_transmit, p_growth, time_limit,
                                                    initial_loads, pos)

        # TODO - Recalculate edge weights (stahler, horsfield/cumming)



if __name__ == '__main__':
    pos = {0: (0, 0), 1: (5, 5), 2: (0, 5)}
    init = {1: 10}
    edges = {(0, 1):10, (0, 2):5, (1, 2):3}
    mpn = MetapopulationPatchWeightedNetwork(3, edges, 0.2, 0.1, 10, init, node_positions=pos)
    mpn.run()
    mpn.display("T")
    mpn.movie("movie", 100)