from LungCompartmentalNetwork import *


class TBFastSlowMetapopulationNetwork(LungNetwork):

    def __init__(self, rates, time_limit, initial_loads, weight_method='horsfield'):

        # Create the network (allows use of networkx functions like neighbours for calculating edge weights)
        LungNetwork.__init__(self, time_limit, ['F', 'S'], initial_loads, weight_method)

        # Assert all rates present
        expected_rates = ['p_transmit_F', 'p_transmit_S', 'p_growth_F', 'p_growth_S', 'p_change_F_to_S',
                          'p_change_S_to_F']
        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        self.total_transmit_f = 0.0
        self.total_transmit_s = 0.0
        self.total_f = 0.0
        self.total_s = 0.0


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