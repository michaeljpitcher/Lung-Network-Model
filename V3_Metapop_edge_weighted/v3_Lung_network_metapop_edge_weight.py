import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation


class MetapopulationWeightedNetwork(nx.Graph):

    def __init__(self, edges, weights, positioning, initial_infections, p_transmit, p_growth, time_limit=100):
        """
        Metapopulation model over a weighted graph. Runs SIS dynamics (with nodes assigned a 'count') and a Gillespie-
        simulation-style time modelling.
        :param edges: Edges of network (also defines nodes)
        :param weights: Weights of edges (as a dict, with tuple (node1, node2) as key)
        :param positioning: Position of nodes (for displaying and movie)
        :param initial_infections: Count for initial infections (as dict, key=node, value=count)
        :param p_transmit:
        :param p_growth:
        :param time_limit:
        """
        nx.Graph.__init__(self)

        # Network Topology
        self.add_edges_from(edges)
        # Edge weights
        for e1, e2 in self.edges():
            # Check that the edge exists in the provided dictionary in some form
            if (e1, e2) in weights.keys():
                self.edge[e1][e2]['weight'] = weights[(e1, e2)]
            elif (e2, e1) in weights.keys():
                self.edge[e1][e2]['weight'] = weights[(e2, e1)]
            else:
                raise Exception, "Edge {0},{1} has not been assigned a weight".format(e1, e2)
        self.positioning = positioning

        # Dynamics
        self.rates = dict()
        self.rates['p_transmit'] = p_transmit
        self.rates['p_growth'] = p_growth

        self.max_count = 0
        self.infected_nodes = []

        # Seed network
        for n in self.nodes():
            # Set count to 0 (adds count as a key to the node)
            self.node[n]['count'] = 0

        for node in initial_infections:
            self.update_node(node, initial_infections[node])

        # Time
        self.timestep = 0.0
        self.time_limit = time_limit

        # Data
        self.data = dict()
        self.record_data()

        self.total_possible_transmission = 0.0
        self.total_bacteria = 0.0

    def display(self, title, save_name=None, node_labels='count', edge_labels=True):
        fig = plt.figure(figsize=(10, 10))
        plt.gca().set_axis_off()

        # nodes
        nodelist_inf = [n for n, data in self.nodes(data=True) if data['count'] > 0]
        nodelist_sus = [n for n, data in self.nodes(data=True) if data['count'] == 0]

        nx.draw_networkx_nodes(self, self.positioning, nodelist=nodelist_sus, node_size=400,
                               node_color="green")
        nx.draw_networkx_nodes(self, self.positioning, nodelist=nodelist_inf, node_size=400,
                               node_color="red")

        # edges
        nx.draw_networkx_edges(self, self.positioning)

        # node labels
        if node_labels == 'count':
            labels = dict((n,d['count']) for n,d in self.nodes(data=True))
            nx.draw_networkx_labels(self, self.positioning, labels=labels, font_family='sans-serif')
        elif node_labels == 'index':
            nx.draw_networkx_labels(self, self.positioning, font_family='sans-serif')
        else:
            raise Exception, "Invalid label choice"

        # edge labels
        if edge_labels:
            edge_labels = nx.get_edge_attributes(self, 'weight')
            nx.draw_networkx_edge_labels(self, self.positioning, edge_labels=edge_labels)

        plt.axis('off')
        plt.title(title)
        plt.show()
        if save_name is not None:
            fig.savefig(save_name + ".png")  # save as png

    def movie(self, filename, interval):
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
            circle = plt.Circle(self.positioning[n], radius=0.1, zorder=2)  # node markers at top of the z-order
            ax.add_patch(circle)
            node_markers.append({'node': n, 'position': circle})
        for e in self.edges_iter():
            xs = [self.positioning[e[0]][0], self.positioning[e[1]][0]]
            ys = [self.positioning[e[0]][1], self.positioning[e[1]][1]]
            line = plt.Line2D(xs, ys, zorder=1, color='k')  # edges lower down the z-order
            ax.add_line(line)
        timepoints = sorted(self.data.keys())

        def update_nodes(time):
            plt.title(str(time))
            for marker in node_markers:
                node=marker['node']
                count = self.data[time][node]
                # TODO - rigged so you can actually see colour change
                if count >= 20:
                    count = 20.0
                colour = (count/20.0,0,0)
                marker = marker['position']
                marker.set(color=colour)

        def init():
            update_nodes(0.0)

        def frame(i):
            update_nodes(timepoints[i])

        movie = animation.FuncAnimation(fig, frame, init_func=init, frames=len(self.data), interval=interval, blit=False)
        #plt.show()
        movie.save(filename + '.mp4', writer='ffmpeg_file')

    def record_data(self):
        self.data[self.timestep] = dict()
        for (n,data) in self.nodes_iter(data=True):
            self.data[self.timestep][n] = data['count']

    def update_node(self, node, amendment):
        # If previous count was 0, the node has just become infected
        if self.node[node]['count'] == 0:
            self.infected_nodes.append(node)

        self.node[node]['count'] += amendment
        assert self.node[node]['count'] >= 0, "update_node: Count cannot drop below zero"
        self.max_count = max(self.node[n]['count'] for n in self.nodes())

        # If new count is 0, node is no longer infected
        if self.node[node]['count'] == 0:
            self.infected_nodes.remove(node)

    def update_totals(self):
        # TODO - ASSUMPTION: transmission is affected by degree
        # TODO - ASSUMPTION: no maximum capacity in node
        self.total_possible_transmission = 0.0
        for node in self.infected_nodes:
            self.total_possible_transmission += self.node[node]['count'] * self.degree(node)
        self.total_bacteria = sum([self.node[n]['count'] for n in self.infected_nodes])

    def transitions(self):
        rate_for_transmit = self.total_possible_transmission * self.rates['p_transmit']
        rate_for_growth = self.total_bacteria * abs(self.rates['p_growth'])

        return [(rate_for_transmit, lambda t: self.transmit()),
                (rate_for_growth, lambda t: self.growth())]

    def calculate_dt(self, total):
        # calculate the timestep delta
        x = np.random.random()
        dt = (1.0 / total) * math.log(1.0 / x)
        return dt

    def choose_transition(self, total, transitions):
        # calculate which transition happens
        x = np.random.random() * total
        k = 0
        (xs, chosen_function) = transitions[k]
        while xs < x:
            k += 1
            (xsp, chosen_function) = transitions[k]
            xs = xs + xsp
        return k

    def transmit(self):
        # Pick a node
        chosen_node = -1
        r = np.random.random() * self.total_possible_transmission
        running_bacteria_total = 0
        for node in self.infected_nodes:
            running_bacteria_total += (self.node[node]['count'] * self.degree(node))
            if running_bacteria_total >= r:
                chosen_node = node
                break

        # Pick a neighbour
        weight_total = sum([data['weight'] for _,_,data in self.edges(chosen_node, data=True)])
        r2 = np.random.random() * weight_total
        running_weight_total = 0.0
        for e1, e2, data in self.edges(chosen_node, data=True):
            running_weight_total += data['weight']
            if running_weight_total > r2:
                self.update_node(e1, -1)
                self.update_node(e2, 1)
                return

    def growth(self):
        r = np.random.random() * self.total_bacteria
        running_total = 0
        for node in self.infected_nodes:
            running_total += self.node[node]['count']
            if running_total >= r:
                if self.rates['p_growth'] > 0.0:
                    self.update_node(node, 1)
                elif self.rates['p_growth'] < 0.0:
                    self.update_node(node, -1)
                return

    def run(self):
        print "RUNNING"
        while self.timestep < self.time_limit and len(self.infected_nodes) > 0:

            self.update_totals()

            transitions = self.transitions()

            total = 0.0
            for (r, _) in transitions:
                total += r

            dt = self.calculate_dt(total)
            chosen_function_index = self.choose_transition(total, transitions)

            # perform the transition
            transitions[chosen_function_index][1](self)

            self.timestep += dt
            self.record_data()


class LungMetapopulationWeighted(MetapopulationWeightedNetwork):

    def __init__(self, weight_method, infected_nodes, initial_load, p_transmit, p_growth, time_limit=100):
        edges = [(0, 1), (1, 2), (2, 3), (1, 4)]
        edges += [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15),
             (15, 16), (16, 17)]
        edges += [(5,18), (6,19), (6,20), (7,21), (7,22), (8,23), (9,24), (10,25), (11,26),(11,27), (13,28), (13,29),
                  (14,30), (14,31), (15,32), (16,33), (17,34),(17,35)]

        positioning = dict()
        positioning[0] = (5, 10)
        positioning[1] = (5, 8)
        positioning[2] = (4, 7)
        positioning[3] = (3.5, 5)
        positioning[4] = (6, 6)
        positioning[5] = (3, 8)
        positioning[6] = (2.75, 8.5)
        positioning[7] = (3, 4.5)
        positioning[8] = (4, 4)
        positioning[9] = (3.5, 3)
        positioning[10] = (3, 2.5)
        positioning[11] = (2.5, 2)
        positioning[12] = (7, 7)
        positioning[13] = (7.5, 8)
        positioning[14] = (8, 7)
        positioning[15] = (6.5, 5)
        positioning[16] = (7.5, 4)
        positioning[17] = (8, 3.5)
        positioning[18] = (2.5, 7.5)
        positioning[19] = (2.5, 9)
        positioning[20] = (3, 9)
        positioning[21] = (2, 5)
        positioning[22] = (2, 4)
        positioning[23] = (3.5, 4.25)
        positioning[24] = (4, 2)
        positioning[25] = (2.5, 3.25)
        positioning[26] = (1.5, 1)
        positioning[27] = (2.75, 1)
        positioning[28] = (7.25, 8.5)
        positioning[29] = (8, 8.5)
        positioning[30] = (8.5, 7.5)
        positioning[31] = (8.5, 6.5)
        positioning[32] = (7, 5.5)
        positioning[33] = (7.5, 3)
        positioning[34] = (8.5, 4.25)
        positioning[35] = (8.5, 3)

        # Pass in weights as 0 here, then override. Allows the use of network functions to find neighbours
        weights = dict()
        for e in edges:
            weights[e] = 0.0

        MetapopulationWeightedNetwork.__init__(self, edges, weights, positioning, infected_nodes, initial_load,
                                               p_transmit, p_growth, time_limit)

        self.origin = 0
        self.terminal_nodes = [n for n in self.nodes() if self.degree(n) == 1 and n != self.origin]
        self.non_terminal_nodes = [n for n in self.nodes() if self.degree(n) != 1]

        if weight_method == 'horsfield':
            self.set_horsfield_weights()
        elif weight_method == 'stahler':
            self.set_stahler_weights()
        else:
            raise Exception, "Invalid edge weight choice"

    def set_horsfield_weights(self):
        order = 1.0
        queued_nodes = []
        for child_node, parent_node in self.edges(self.terminal_nodes):
            self[child_node][parent_node]['weight'] = order
            queued_nodes.append(parent_node)
        # Order the queued list (highest value first)
        queued_nodes = sorted(set(queued_nodes), reverse=True)
        while len(queued_nodes) > 0:
            node = queued_nodes.pop(0)
            edges = self.edges(node, data=True)
            # Check that all child edges have an order (i.e. only parent is unfilled)
            child_orders = [e[2]['weight'] for e in edges if e[2]['weight'] > 0.0]
            assert len(child_orders) == len(self.edges(node)) - 1
            new_order = max(child_orders) + 1
            parent_node = [n for n in self.neighbors(node) if n < node][0]
            # Set the new order on the parent edge
            self[node][parent_node]['weight'] = new_order
            # Add the parent node to the queue
            if parent_node != self.origin:
                queued_nodes.append(parent_node)
            queued_nodes = sorted(set(queued_nodes), reverse=True)

    def set_stahler_weights(self):
        order = 1.0
        queued_nodes = []
        for child_node, parent_node in self.edges(self.terminal_nodes):
            self[child_node][parent_node]['weight'] = order
            queued_nodes.append(parent_node)
        # Order the queued list (highest value first)
        queued_nodes = sorted(set(queued_nodes), reverse=True)
        while len(queued_nodes) > 0:
            node = queued_nodes.pop(0)
            edges = self.edges(node, data=True)
            # Check that all child edges have an order (i.e. only parent is unfilled)
            child_orders = [e[2]['weight'] for e in edges if e[2]['weight'] > 0.0]
            assert len(child_orders) == len(self.edges(node)) - 1
            if max(child_orders) == min(child_orders):
                new_order = max(child_orders) + 1
            else:
                new_order = max(child_orders)
            parent_node = [n for n in self.neighbors(node) if n < node][0]
            # Set the new order on the parent edge
            self[node][parent_node]['weight'] = new_order
            # Add the parent node to the queue
            if parent_node != self.origin:
                queued_nodes.append(parent_node)
            queued_nodes = sorted(set(queued_nodes), reverse=True)


if __name__ == '__main__':
    ln = LungMetapopulationWeighted('horsfield', [2], 200, 0.3, 0.5, 1)
    ln.run()
    ln.display("TEST")