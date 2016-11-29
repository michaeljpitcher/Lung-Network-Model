import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.animation as animation


class LungNetwork(nx.Graph):

    def __init__(self, infected_nodes, p_infect, p_recover, time_limit=100):
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
        # self.terminal_nodes = [n for n in self.nodes_iter() if self.degree(n) == 1 and n != self.origin]
        # self.non_terminal_nodes = [n for n in self.nodes_iter() if self.degree(n) != 1]
        self.positioning = self.positioning()

        # Dynamics
        self.states = ['S','I']
        self.rates = dict()
        self.rates['p_infect'] = p_infect
        self.rates['p_recover'] = p_recover

        # Node populations
        self.populations = dict()
        for s in self.states:
            self.populations[s] = []

        # Seed network
        for n in self.nodes_iter():
            if n in infected_nodes:
                self.node[n]['state'] = 'I'
                self.populations['I'].append(n)
            else:
                self.node[n]['state'] = 'S'
                self.populations['S'].append(n)

        # Stochastic dynamics
        self.si_edges = []
        for (n, m) in self.edges_iter(self.populations['I']):
            if self.node[m]['state'] == 'S':
                self.si_edges.append((n, m))

        # Mark all edges as unoccupied
        # for (_, _, edge_data) in self.edges(data=True):
        #     edge_data['occupied'] = False

        # Time
        self.timestep = 0.0
        self.time_limit = time_limit

        # Data
        self.data = dict()
        self.record_data()

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

    def movie(self, filename, interval):
        print "MAKING MOVIE"
        fig = plt.figure(figsize=(10, 10))
        # manipulate the axes, since this isn't a data plot
        ax = fig.gca()
        ax.set_xlim([-0.2, 10.2])  # axes bounded around 1
        ax.set_ylim([-0.2, 12.2])
        ax.grid(False)  # no grid
        ax.get_xaxis().set_ticks([])  # no ticks on the axes
        ax.get_yaxis().set_ticks([])
        node_markers = []
        for n in self.nodes_iter():
            circ = plt.Circle(self.positioning[n], radius=0.1, zorder=2)  # node markers at top of the z-order
            ax.add_patch(circ)
            node_markers.append({'node_key': n, 'marker': circ})
        for e in self.edges_iter():
            xs = [self.positioning[e[0]][0], self.positioning[e[1]][0]]
            ys = [self.positioning[e[0]][1], self.positioning[e[1]][1]]
            line = plt.Line2D(xs, ys, zorder=1, color='k')  # edges lower down the z-order
            ax.add_line(line)
        timepoints = sorted(self.data.keys())

        def update_nodes(time):
            plt.title(str(time))
            for nm in node_markers:
                node=nm['node_key']
                state = self.data[time][node]
                if state == 'S':
                    colour = 'g'
                else:
                    colour = 'r'
                marker = nm['marker']
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
        for (n,node_data) in self.nodes_iter(data=True):
            self.data[self.timestep][n] = node_data['state']

    def update_node(self, node, new_state):
        assert self.node[node]['state'] != new_state
        self.populations[self.node[node]['state']].remove(node)
        self.populations[new_state].append(node)
        self.node[node]['state'] = new_state

    def infect(self):
        # choose an SI edge
        i = np.random.randint(len(self.si_edges))
        (infected_node, susceptible_node) = self.si_edges[i]
        # infect the susceptible end
        assert self.node[susceptible_node]['state'] == 'S'
        self.update_node(susceptible_node, 'I')
        # label the edge we traversed as occupied
        # self.edge[infected_node][susceptible_node]['occupied'] = True
        # remove all edges in the SI list from an infected node to this one
        self.si_edges = [(node_1, node_2) for (node_1, node_2) in self.si_edges if susceptible_node != node_2]
        # add all the edges incident on this node connected to susceptible nodes
        susceptible_neighbours = [e[1] for e in self.edges(susceptible_node) if self.node[e[1]]['state'] == 'S']
        for neighbour in susceptible_neighbours:
            self.si_edges.insert(0, (susceptible_node, neighbour))

    def recover(self):
        # choose an infected node at random
        index = np.random.randint(len(self.populations['I']))
        node_to_recover = self.populations['I'][index]
        # mark the node as recovered
        self.update_node(node_to_recover, 'S')
        # remove all edges in the SI list incident on this node
        self.si_edges = [(inf_node, sus_node) for (inf_node, sus_node) in self.si_edges if inf_node != node_to_recover]

    def transitions(self):
        return [(len(self.si_edges) * self.rates['p_infect'], lambda t: self.infect()),
                (len(self.populations['I']) * self.rates['p_recover'], lambda t: self.recover())]

    def run(self):
        print "RUNNING"
        while len(self.populations['I']) > 0:

            transitions = self.transitions()
            total = 0.0
            for (r, _) in transitions:
                total = total + r

            # calculate the timestep delta
            x = np.random.random()
            dt = (1.0 / total) * math.log(1.0 / x)

            if self.timestep + dt > self.time_limit:
                # Don't perform the task if it would break over the limit
                break

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


if __name__ == '__main__':
    ln = LungNetwork([2], 0.1, 0.0001, 300)
    ln.run()
    ln.movie('simple_sir',400)

