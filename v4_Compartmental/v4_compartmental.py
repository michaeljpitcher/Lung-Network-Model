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


class LungCompartmentalFastSlowMetapopulationNetwork(CompartmentalMetapopulationNetwork):

    def __init__(self, rates, time_limit, initial_loads, weight_method='horsfield'):

        # Assert all rates present
        expected_rates = ['p_transmit_F', 'p_transmit_S', 'p_growth_F', 'p_growth_S', 'p_change_F_to_S',
                          'p_change_S_to_F']
        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

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

        # Create the network (allows use of networkx functions like neighbours for calculating edge weights)
        CompartmentalMetapopulationNetwork.__init__(self, 36, edge_weights, time_limit, ['F','S'], initial_loads, pos)
        # Origin and terminal nodes (to compute edge weights)
        self.origin = 0
        self.terminal_nodes = [n for n in self.nodes() if self.degree(n) == 1 and n != self.origin]
        self.non_terminal_nodes = [n for n in self.nodes() if self.degree(n) != 1]
        # Calculate edge weights
        self.set_weights(weight_method)

        self.total_transmit_f = 0.0
        self.total_transmit_s = 0.0
        self.total_f = 0.0
        self.total_s = 0.0

    def set_weights(self, weight_method):
        """
        Set edge weights. Terminal branches order 1. Other branches depend on ordering method:
        Horsfield - parent branch has order 1 greater than maximum of child branches
        Stahler - parent branch has order 1 greater than child branches if they are equal, else has max of child orders
        :return:
        """

        # Get the nodes in an ordered list - gives a list where all child nodes appear in list before parent
        # So can add the order of an edge as all child edges (those futher from origin) will already have been computed

        # Start with origin node
        queued_nodes = [self.node_list[self.origin]]
        ordered_nodes = []

        # Pull a node from queued nodes, add it to the start of ordered nodes and add its neighbours to queued nodes
        while len(queued_nodes) > 0:
            node = queued_nodes.pop()
            ordered_nodes.insert(0, node)
            queued_nodes += [n for n in self.neighbors(node) if n not in ordered_nodes]

        # Process all nodes
        while len(ordered_nodes) > 0:
            # Pull the node from the list
            node = ordered_nodes.pop(0)
            # Don't process origin
            if node.id == self.origin:
                break
            # Find the parent edge (should only be one) as edge where weight hasn't already been set
            parent_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                            data['weight'] == 0.0]
            assert len(parent_edges) == 1
            # Get the data from parent edge to update
            parent_edge = parent_edges[0][2]
            # If the node is terminal, weight is 1.0
            if node in self.terminal_nodes:
                parent_edge['weight'] = 1.0
            else:
                # Get the child edges (those with weights already set)
                child_edges = [(node1, node2, data) for node1, node2, data in self.edges(node, data=True) if
                               data['weight'] > 0.0]
                # Get the weights
                child_orders = [data['weight'] for _,_,data in child_edges]
                # Determine new weight based on method chosen
                if weight_method == 'horsfield':
                    new_order = max(child_orders) + 1.0
                elif weight_method == 'stahler':
                    if len(set(child_orders)) <= 1:
                        new_order = max(child_orders) + 1.0
                    else:
                        new_order = max(child_orders)
                else:
                    raise Exception, "Invalid ordering method: {0}".format(weight_method)
                # Set the parent weight
                parent_edge['weight'] = new_order

    def transitions(self):

        self.total_transmit_f = sum([node.counts['F'] * self.degree(node) for node in self.infected_nodes])
        self.total_transmit_s = sum([node.counts['S'] * self.degree(node) for node in self.infected_nodes])

        self.total_f = sum([node.counts['F'] for node in self.infected_nodes])
        self.total_s = sum([node.counts['S'] for node in self.infected_nodes])

        rate_for_transmit_f = self.total_transmit_f * self.rates['p_transmit_F']
        rate_for_transmit_s = self.total_transmit_f * self.rates['p_transmit_S']

        rate_for_growth_f = self.total_f * abs(self.rates['p_growth_F'])
        rate_for_growth_s = self.total_f * abs(self.rates['p_growth_S'])

        rate_for_change_f_s = self.total_f * self.rates['p_change_F_to_S']
        rate_for_change_s_f = self.total_f * self.rates['p_change_S_to_F']

        return [(rate_for_transmit_f, lambda t: self.transmit('F')),
                (rate_for_transmit_s, lambda t: self.transmit('S')),
                (rate_for_growth_f, lambda t: self.growth('F')),
                (rate_for_growth_s, lambda t: self.growth('S')),
                (rate_for_change_f_s, lambda t: self.change('S','F')),
                (rate_for_change_s_f, lambda t: self.change('F','S'))]

    def transmit(self, type):

        if type == 'F':
            r = np.random.random() * self.total_transmit_f
        elif type == 'S':
            r = np.random.random() * self.total_transmit_s
        else:
            raise Exception, "Invalid transmission: {0} compartment not valid".format(type)

        running_total = 0
        for node in self.infected_nodes:
            running_total += node.counts[type] * self.degree(node)
            if running_total >= r:
                total_weights = sum(d['weight'] for _, _, d in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                for _, neighbour, d in self.edges(node, data=True):
                    running_total_weights += d['weight']
                    if running_total_weights > r2:
                        self.update_node(node, type, -1)
                        self.update_node(neighbour, type, 1)
                        return

    def growth(self, type):

        if type == 'F':
            r = np.random.random() * self.total_f
        elif type == 'S':
            r = np.random.random() * self.total_s
        else:
            raise Exception, "Invalid growth: {0} compartment not valid".format(type)

        running_total = 0
        for node in self.infected_nodes:
            running_total += node.counts[type]
            if running_total >= r:
                if type == 'F':
                    rate = self.rates['p_growth_F']
                else:
                    rate = self.rates['p_growth_S']

                if rate > 0:
                    self.update_node(node, type, 1)
                elif rate < 0:
                    self.update_node(node, type, -1)
                return

    def change(self, old_type, new_type):

        if old_type == 'F':
            r = np.random.random() * self.total_f
        elif old_type == 'S':
            r = np.random.random() * self.total_s
        else:
            raise Exception, "Invalid change: {0} compartment not valid".format(new_type)

        running_total = 0
        for node in self.infected_nodes:
            running_total += node.counts[old_type]
            if running_total >= r:
                self.update_node(node, old_type, 1)
                self.update_node(node, new_type, -1)
                return


if __name__ == '__main__':

    rates = {'p_transmit_F':0.1, 'p_transmit_S':0.0, 'p_growth_F':1.0, 'p_growth_S':0.0, 'p_change_F_to_S':0.0,
                      'p_change_S_to_F':0.0}

    initial_loads = dict()
    initial_loads[0] = {'F':10,'S':1}

    a = LungCompartmentalFastSlowMetapopulationNetwork(rates, 5, initial_loads, 'horsfield')
    # a.display("TITLE")
    a.run()
    a.display("END")
