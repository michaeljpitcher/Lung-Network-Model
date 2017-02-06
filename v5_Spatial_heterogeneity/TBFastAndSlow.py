from LungMetapopulationNetwork import *


class TBFastSlowMetapopulationNetwork(LungMetapopulationNetwork):

    def __init__(self, rates, initial_loads_fast, initial_loads_slow, weight_method='horsfield'):

        initial_loads = dict()
        for id in initial_loads_fast:
            initial_loads[id] = dict()
            initial_loads[id]['F'] = initial_loads_fast[id]
        for id in initial_loads_slow:
            initial_loads[id] = dict()
            initial_loads[id]['S'] = initial_loads_slow[id]

        # Create the network
        LungMetapopulationNetwork.__init__(self, ['F', 'S'], initial_loads, weight_method)

        # Assert all rates present
        expected_rates = ['p_translocate_F', 'p_translocate_S', 'p_growth_F', 'p_growth_S', 'p_change_F_to_S',
                          'p_change_S_to_F']
        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        self.total_translocate_f = 0.0
        self.total_translocate_s = 0.0
        self.total_f = 0.0
        self.total_s = 0.0
        self.total_f_O2 = 0.0
        self.total_s_O2 = 0.0

    def update_totals(self):

        self.total_translocate_f = sum([node.counts['F'] * self.degree(node) for node in self.nodes()])
        self.total_translocate_s = sum([node.counts['S'] * self.degree(node) for node in self.nodes()])

        self.total_f = sum([node.counts['F'] for node in self.nodes()])
        self.total_s = sum([node.counts['S'] for node in self.nodes()])

        self.total_f_O2 = sum([node.counts['F'] * node.attributes['oxygen_tension'] for node in self.nodes()])
        self.total_s_O2 = sum([node.counts['S'] * node.attributes['oxygen_tension'] for node in self.nodes()])

    def events(self):

        self.update_totals()

        rate_for_translocate_f = self.total_translocate_f * self.rates['p_translocate_F']
        rate_for_translocate_s = self.total_translocate_s * self.rates['p_translocate_S']

        rate_for_growth_f = self.total_f * abs(self.rates['p_growth_F'])
        rate_for_growth_s = self.total_s * abs(self.rates['p_growth_S'])

        # TODO - check use of O2 tension - prob
        rate_for_change_f_s = self.total_f_O2 * self.rates['p_change_F_to_S']
        rate_for_change_s_f = self.total_s_O2 * self.rates['p_change_S_to_F']

        return [(rate_for_translocate_f, lambda t: self.translocate('F')),
                (rate_for_translocate_s, lambda t: self.translocate('S')),
                (rate_for_growth_f, lambda t: self.growth('F')),
                (rate_for_growth_s, lambda t: self.growth('S')),
                (rate_for_change_f_s, lambda t: self.change('F','S')),
                (rate_for_change_s_f, lambda t: self.change('S','F'))]

    def translocate(self, type):

        if type == 'F':
            r = np.random.random() * self.total_translocate_f
        elif type == 'S':
            r = np.random.random() * self.total_translocate_s
        else:
            raise Exception, "Invalid transmission: {0} compartment not valid".format(type)

        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.counts[type] * self.degree(node)
            if running_total >= r:
                total_weights = sum(edge['weight'] for _, _, edge in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                neighbour_ids = sorted([n.id for n in self.neighbors(node)])
                for neighbour_id in neighbour_ids:
                    neighbour = self.node_list[neighbour_id]
                    edge = self.edge[node][neighbour]
                    running_total_weights += edge['weight']
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
        for id in self.node_list:
            node = self.node_list[id]
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
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.counts[old_type]
            if running_total >= r:
                self.update_node(node, old_type, -1)
                self.update_node(node, new_type, 1)
                return

if __name__ == '__main__':
    rates = {}
    rates['p_translocate_F'] = 0.1
    rates['p_translocate_S'] = 0.1
    rates['p_growth_F'] = 0.1
    rates['p_growth_S'] = 0.1
    rates['p_change_F_to_S'] = 0.1
    rates['p_change_S_to_F'] = 0.1

    limit = 50

    loads_fast = dict()
    loads_fast[0] = 10
    loads_fast[1] = 7

    loads_slow = dict()
    loads_slow[15] = 1
    loads_slow[16] = 4

    model = TBFastSlowMetapopulationNetwork(rates, limit, loads_fast, loads_slow)

    model.run()

    model.display()