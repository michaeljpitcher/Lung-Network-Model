import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation


class MetapopulationWeightedNetwork(nx.Graph):

    def __init__(self, edges, weights, positioning, infected_nodes, initial_load, p_transmit, p_growth, time_limit=100):
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

        for n in infected_nodes:
            self.update_node(n, initial_load)

        # Time
        self.timestep = 0.0
        self.time_limit = time_limit

        # Data
        self.data = dict()
        self.record_data()

        self.total_possible_transmission = 0.0
        self.total_bacteria = 0.0

    def display(self, title, save_name=None, node_labels=True, edge_labels=True):
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
        if node_labels:
            labels = dict((n,d['count']) for n,d in self.nodes(data=True))
            nx.draw_networkx_labels(self, self.positioning, labels=labels, font_family='sans-serif')

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
            for neighbour in self.neighbors(node):
                self.total_possible_transmission += self.node[node]['count'] * self.edge[node][neighbour]['weight']
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
        r = np.random.random() * self.total_possible_transmission
        running_total = 0
        for node in self.infected_nodes:
            for neighbour in self.neighbors(node):
                running_total += self.node[node]['count'] * self.edge[node][neighbour]['weight']
                if running_total >= r:
                    self.update_node(node, -1)
                    self.update_node(neighbour, 1)
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


if __name__ == '__main__':
    # ln = LungNetwork([2], 200, 0.3, 0.5, 1)
    # ln.run()
    # ln.movie('metapop_weighted', 100)
    # ln.display('Metapop weighted', save_name="metapop_weighted")
    pass