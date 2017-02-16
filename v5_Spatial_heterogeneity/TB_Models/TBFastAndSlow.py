from v5_Spatial_heterogeneity.Lung_Models.LungMetapopulationNetwork import *

FAST = 'F'
SLOW = 'S'
P_MIGRATE_F = 'p_migrate_f'
P_MIGRATE_S = 'p_migrate_s'
P_GROWTH_F = 'p_growth_f'
P_GROWTH_S = 'p_growth_s'
P_CHANGE_F_TO_S = 'p_change_f_s'
P_CHANGE_S_TO_F = 'p_change_s_f'


class TBFastSlowMetapopulationNetwork(LungMetapopulationNetwork):
    """ Metapopulation network with Fast and Slow bacteria as species

    Two species of bacteria: fast and slow. Both have user-specified individual growth rates, rates for migration to a
    new patch and rates of change from one to the other
    """

    def __init__(self, rates, initial_loads_fast, initial_loads_slow, weight_method='horsfield'):
        """

        :param rates: Dictionary containing rates for each event
        :param initial_loads_fast: Dictionary of initial loads of fast bacteria for each patch
        :param initial_loads_slow: Dictionary of initial loads of slow bacteria for each patch
        :param weight_method: Weighting method (Horsfield or Stahler)
        """
        # Set up initial loads
        initial_loads = dict()
        for id in initial_loads_fast:
            initial_loads[id] = dict()
            initial_loads[id][FAST] = initial_loads_fast[id]
        for id in initial_loads_slow:
            initial_loads[id] = dict()
            initial_loads[id][SLOW] = initial_loads_slow[id]

        # Create the network
        LungMetapopulationNetwork.__init__(self, [FAST, SLOW], initial_loads, weight_method)

        # Assert all rates present
        expected_rates = [P_MIGRATE_F, P_MIGRATE_S, P_GROWTH_F, P_GROWTH_S, P_CHANGE_F_TO_S, P_CHANGE_S_TO_F]
        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        # Initial total counts
        self.total_migrate_f = 0.0
        self.total_migrate_s = 0.0
        self.total_f = 0.0
        self.total_s = 0.0
        self.total_f_O2 = 0.0
        self.total_s_O2 = 0.0

    def update_totals(self):
        """
        Update the total counts - used to determine the rates based on how many of each species exist etc.
        :return:
        """

        # Migration is based on total bacteria * degree of patch where they reside
        # TODO - check use of degree
        self.total_migrate_f = sum([node.subpopulations[FAST] * node.degree for node in self.nodes()])
        self.total_migrate_s = sum([node.subpopulations[SLOW] * node.degree for node in self.nodes()])

        # Growth is based on total numbers of bacteria
        self.total_f = sum([node.subpopulations[FAST] for node in self.nodes()])
        self.total_s = sum([node.subpopulations[SLOW] for node in self.nodes()])

        # Change is based on total number of bacteria * oxygen tension of patch where they reside
        # TODO - check use of O2 tension & prob - maybe should just be a constant event
        self.total_f_O2 = sum([node.subpopulations[FAST] * (1/node.oxygen_tension) for node in self.nodes()])
        self.total_s_O2 = sum([node.subpopulations[SLOW] * node.oxygen_tension for node in self.nodes()])

    def events(self):
        """
        Calculate rates of events.
        :return:
        """

        # Update the counts
        self.update_totals()

        # Rate for migration
        rate_for_migrate_f = self.total_migrate_f * self.rates[P_MIGRATE_F]
        rate_for_migrate_s = self.total_migrate_s * self.rates[P_MIGRATE_S]
        # Rate for growth
        rate_for_growth_f = self.total_f * abs(self.rates[P_GROWTH_F])
        rate_for_growth_s = self.total_s * abs(self.rates[P_GROWTH_S])
        # Rate for change
        rate_for_change_f_s = self.total_f_O2 * self.rates[P_CHANGE_F_TO_S]
        rate_for_change_s_f = self.total_s_O2 * self.rates[P_CHANGE_S_TO_F]

        # Return rates and functions they apply to
        return [(rate_for_migrate_f, lambda t: self.migrate(FAST)),
                (rate_for_migrate_s, lambda t: self.migrate(SLOW)),
                (rate_for_growth_f, lambda t: self.growth(FAST)),
                (rate_for_growth_s, lambda t: self.growth(SLOW)),
                (rate_for_change_f_s, lambda t: self.change(FAST,SLOW)),
                (rate_for_change_s_f, lambda t: self.change(SLOW,FAST))]

    def migrate(self, type):
        """
        Move a bacteria of given type to a new patch.

        Bacteria on patches with greater degree are more likely to move.
        :param type:
        :return:
        """

        # Get relevant total (number * degree for each patch)
        if type == FAST:
            r = np.random.random() * self.total_migrate_f
        elif type == SLOW:
            r = np.random.random() * self.total_migrate_s
        else:
            raise Exception, "Invalid migration: {0} species not valid".format(type)
        # Pick a patch at random for bacteria to migrate from based on the total
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[type] * node.degree
            # Patch 1 chosen
            if running_total >= r:
                # Pick a neighbour based on the weights of the edges from patch 1
                # Get total edge weight
                total_weights = sum(edge[EDGE_OBJECT].weight for _, _, edge in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                # Get neighbours
                neighbour_ids = sorted([n.id for n in self.neighbors(node)])
                # Increment counter with edge weights until r2 exceeded
                for neighbour_id in neighbour_ids:
                    neighbour = self.node_list[neighbour_id]
                    edge = self.edge[node][neighbour][EDGE_OBJECT]
                    running_total_weights += edge.weight
                    # Neighbour patch chosen
                    if running_total_weights > r2:
                        # Update node and neighbour to move one bacteria to neighbour from patch
                        self.update_node(node, type, -1)
                        self.update_node(neighbour, type, 1)
                        return

    def growth(self, type):
        """
        Specified type of bacteria replicates/dies, incrementing/decrementing the subpopulation
        :param type:
        :return:
        """
        # Get the relevant rate
        if type == FAST:
            r = np.random.random() * self.total_f
            rate = self.rates[P_GROWTH_F]
        elif type == SLOW:
            r = np.random.random() * self.total_s
            rate = self.rates[P_GROWTH_S]
        else:
            raise Exception, "Invalid growth: {0} species not valid".format(type)
        # Pick a patch at random based on their counts for this bacteria type
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[type]
            # Patch chosen
            if running_total >= r:
                # Increment / decrement the count
                if rate > 0:
                    self.update_node(node, type, 1)
                elif rate < 0:
                    self.update_node(node, type, -1)
                return

    def change(self, old_type, new_type):
        """
        Change a bacteria from one type to the other
        :param old_type: Previous type
        :param new_type: New type
        :return:
        """
        # Get rate dependent of type of bacteria that is changing
        if old_type == FAST:
            r = np.random.random() * self.total_f
        elif old_type == SLOW:
            r = np.random.random() * self.total_s
        else:
            raise Exception, "Invalid change: {0} species not valid".format(new_type)
        # Chose a patch based on numbers of type of bacteria in it
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[old_type]
            # Patch chosen
            if running_total >= r:
                self.update_node(node, old_type, -1)
                self.update_node(node, new_type, 1)
                return

if __name__ == '__main__':
    rates = {}
    rates[P_MIGRATE_F] = 0.01
    rates[P_MIGRATE_S] = 0.01
    rates[P_GROWTH_F] = 0.1
    rates[P_GROWTH_S] = 0.01
    rates[P_CHANGE_F_TO_S] = 0.1
    rates[P_CHANGE_S_TO_F] = 0.1

    loads_fast = dict()
    loads_fast[0] = 1

    loads_slow = dict()

    model = TBFastSlowMetapopulationNetwork(rates, loads_fast, loads_slow)

    limit = 50
    model.run(limit)

    model.display([FAST, SLOW])