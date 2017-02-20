from v5_Spatial_heterogeneity.Lung_Models.LungMetapopulationNetwork import *

FAST = 'fast'
SLOW = 'slow'
MACROPHAGE = 'macrophage'

P_REPLICATE_FAST = 'replication_fast'
P_REPLICATE_SLOW = 'replication_slow'
P_CHANGE_FAST_SLOW = 'change_fast_to_slow'
P_CHANGE_SLOW_FAST = 'change_slow_to_fast'
P_MIGRATE_FAST = 'fast_migrate'
P_MIGRATE_SLOW = 'slow_migrate'

P_RECRUIT = 'recruit_macrophage'
P_DEATH = 'mac_death'

P_INGEST_FAST = 'mac_ingests_fast'
P_INGEST_SLOW = 'mac_ingests_slow'


class TBMetapopulationNetwork_FSM(LungMetapopulationNetwork):
    """
    Metapopulation model of TB infection with host interaction.

    3 populations - Fast bacteria, slow bacteria and macrophages. Fast and slow bacteria replicate at their own
    individual rates, and can migrate to new patches at their own rates and can change between each other. Macrophages
    are recruited at defined rate, die at a defined rate and ingest each type of bacteria at individual rates.

    Spatial element - bacteria rate of change fast-slow differs based on the oxygen tension attribute of the patch
    """

    def __init__(self, rates, initial_loads, weight_method=HORSFIELD):
        """

        :param rates: User-defined rates for events
        :param initial_loads: Where to place initial populations
        :param weight_method: method of edge weighting
        """

        # Create the network
        LungMetapopulationNetwork.__init__(self, [FAST, SLOW, MACROPHAGE], initial_loads, weight_method)

        # Assert all rates present
        expected_rates = [P_REPLICATE_FAST, P_REPLICATE_SLOW,
                          P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                          P_MIGRATE_FAST, P_MIGRATE_SLOW,
                          P_INGEST_FAST, P_INGEST_SLOW,
                          P_RECRUIT, P_DEATH]

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        # Initialise totals
        self.total_f = 0
        self.total_s = 0
        self.total_mac = 0
        self.total_mac_fast = 0
        self.total_mac_slow = 0
        self.total_f_degree = 0
        self.total_s_degree = 0
        self.total_f_o2 = 0.0
        self.total_s_o2 = 0.0

    def update_totals(self):
        """
        Update the totals, to be used for rate calculation for events
        :return:
        """
        self.total_f = 0
        self.total_s = 0
        self.total_mac = 0
        self.total_mac_fast = 0
        self.total_mac_slow = 0
        self.total_f_degree = 0
        self.total_s_degree = 0
        self.total_f_o2 = 0.0
        self.total_s_o2 = 0.0

        for node in self.node_list.values():
            self.total_f += node.subpopulations[FAST]
            self.total_s += node.subpopulations[SLOW]
            self.total_mac += node.subpopulations[MACROPHAGE]
            self.total_mac_fast += node.subpopulations[FAST] * node.subpopulations[MACROPHAGE]
            self.total_mac_slow += node.subpopulations[SLOW] * node.subpopulations[MACROPHAGE]
            # TODO - check usage of degree
            self.total_f_degree += node.subpopulations[FAST] * node.degree
            self.total_s_degree += node.subpopulations[SLOW] * node.degree
            self.total_f_o2 += node.subpopulations[FAST] * node.oxygen_tension
            self.total_s_o2 += node.subpopulations[SLOW] * node.oxygen_tension
            pass

    def events(self):
        """
        Generate a list, where each element is (x,y) - x=rate of event, y=lambda function for function of event
        :return:
        """

        events = []
        # Update the totals
        self.update_totals()

        # Replication - total number of bacteria of metabolism * prob of replication
        events.append((self.total_f * self.rates[P_REPLICATE_FAST], lambda f: self.replicate(FAST)))
        events.append((self.total_s * self.rates[P_REPLICATE_SLOW], lambda f: self.replicate(SLOW)))

        # Metabolism change - sum of (number of bacteria of metabolism in patch * o2 tension) * prob of change
        # TODO - check if this is ok
        events.append((self.total_f_o2 * self.rates[P_CHANGE_FAST_SLOW], lambda f: self.change(SLOW)))
        events.append((self.total_s_o2 * self.rates[P_CHANGE_SLOW_FAST], lambda f: self.change(FAST)))

        # Migrate - sum of (number of bacteria of metabolism in patch * degree of patch) * prob of migration
        events.append((self.total_f_degree * self.rates[P_MIGRATE_FAST], lambda f: self.migrate(FAST)))
        events.append((self.total_s_degree * self.rates[P_MIGRATE_SLOW], lambda f: self.migrate(SLOW)))

        # Recruit mac - num of nodes * prob of recruit
        events.append((len(self.nodes()) * self.rates[P_RECRUIT], lambda f: self.recruit_mac()))

        # Death of mac - total number of macs * prob of death
        events.append((self.total_mac * self.rates[P_DEATH], lambda f: self.death_mac()))

        # Mac ingest - sum of (number of bacteria of metabolism in patch * num of macrophages in patch) * prob of ingest
        events.append((self.total_mac_fast * self.rates[P_INGEST_FAST], lambda f: self.ingest(FAST)))
        events.append((self.total_mac_slow * self.rates[P_INGEST_SLOW], lambda f: self.ingest(SLOW)))

        return events

    def replicate(self, metabolism):
        """
        A bacteria replicates, creating a new bacteria of identical metabolism
        :param metabolism: FAST or SLOW
        :return:
        """
        # Set r based on metabolism
        if metabolism == FAST:
            r = np.random.random() * self.total_f
        elif metabolism == SLOW:
            r = np.random.random() * self.total_s
        else:
            raise Exception, "Invalid replication: {0} metabolism not valid".format(type)

        # Check nodes until total bac exceeds r
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[metabolism]
            if running_total > r:
                assert node.subpopulations[metabolism] > 0, "Error: no bacteria of {0} metabolism present"\
                    .format(metabolism)
                # Increment the count by 1
                self.update_node(node, metabolism, 1)
                return

    def ingest(self, metabolism):
        """
        A macrophage ingests a bacteria, reducing the count for given metabolism by 1
        :param metabolism:
        :return:
        """
        # Set r based on metabolism count
        if metabolism == FAST:
            r = np.random.random() * self.total_mac_fast
        elif metabolism == SLOW:
            r = np.random.random() *self.total_mac_slow
        else:
            raise Exception, "Invalid ingest: bacteria {0} not valid".format(metabolism)

        # Count through node until count exceeds r
        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[metabolism] * node.subpopulations[MACROPHAGE]
            if running_total >= r:
                # Reduce the count for metabolism by 1
                self.update_node(node, metabolism, -1)
                return

    def recruit_mac(self):
        """
        A new macrophage is recruited to the patch
        :return:
        """
        # TODO - Based on level of infection?
        id = np.random.randint(0, len(self.nodes()))
        node = self.node_list[id]
        self.update_node(node, MACROPHAGE, 1)

    def death_mac(self):
        """
        A macrophage dies
        :return:
        """
        # Generate r based on total mac numbers
        r = np.random.random() * self.total_mac
        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[MACROPHAGE]
            if running_total >= r:
                # reduce the macrophage count by 1
                self.update_node(node, MACROPHAGE, -1)
                return

    def migrate(self, metabolism):
        """
        A bacteria of given metabolism moves from one patch to another. New patch depends on edge weights.
        :param metabolism:
        :return:
        """
        # TODO - check usage of degree / weights

        # Generate r based on metabolism and degree
        if metabolism == FAST:
            r = np.random.random() * self.total_f_degree
        elif metabolism == SLOW:
            r = np.random.random() * self.total_s_degree
        else:
            raise Exception, "Invalid migrate: {0} not valid".format(metabolism)

        # Process each node adding count of bacteria * degree until r exceeded
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[metabolism] * node.degree
            if running_total > r:
                # Find a new patch based on the weights of edges from node
                total_weights = sum(edge_data[EDGE_OBJECT].weight for _, _, edge_data in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                # Process all neighbours, adding edge weights until r2 exceeded
                neighbours = sorted(self.neighbors(node), key=lambda x: x.id, reverse=False)
                for neighbour in neighbours:
                    edge = self.edge[node][neighbour][EDGE_OBJECT]
                    running_total_weights += edge.weight
                    if running_total_weights > r2:
                        # Move bacteria from node to neighbour
                        self.update_node(node, metabolism, -1)
                        self.update_node(neighbour, metabolism, 1)
                        return

    def change(self, new_metabolism):
        """
        A bacteria changes its metabolism FAST -> SLOW (or vice versa). Dependent on oxygen tension at patch.
        :param new_metabolism:
        :return:
        """
        # Calculate r and get old metabolism
        if new_metabolism == FAST:
            r = np.random.random() * self.total_s_o2
            old_metabolism = SLOW
        elif new_metabolism == SLOW:
            r = np.random.random() * self.total_f_o2
            old_metabolism = FAST
        else:
            raise Exception, "Invalid metabolism change: {0} metabolism not valid".format(new_metabolism)

        # Process all nodes, adding num of bacteria of metabolism * oxygen tension until r exceeded
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[old_metabolism] * node.oxygen_tension
            if running_total >= r:
                # Reduce old count by 1 and increment new count by 1
                self.update_node(node, new_metabolism, 1)
                self.update_node(node, old_metabolism, -1)
                return


if __name__ == '__main__':
    rates = dict()
    rates[P_REPLICATE_FAST] = 0.1
    rates[P_REPLICATE_SLOW] = 0.01
    rates[P_MIGRATE_FAST] = 0.01
    rates[P_MIGRATE_SLOW] = 0.01
    rates[P_CHANGE_FAST_SLOW] = 0.01
    rates[P_CHANGE_SLOW_FAST] = 0.1

    rates[P_RECRUIT] = 0.01 * 10
    rates[P_DEATH] = 0.01

    rates[P_INGEST_FAST] = 0.0
    rates[P_INGEST_SLOW] = 0.0

    loads = dict()
    loads[5] = dict()
    loads[5][MACROPHAGE] = 10
    loads[13] = dict()
    loads[13][FAST] = 10
    loads[27] = dict()
    loads[27][SLOW] = 4


    netw = TBMetapopulationNetwork_FSM(rates, loads)

    import cProfile

    p = cProfile.Profile()
    p.enable()
    netw.run(50)
    p.disable()
    p.print_stats('tottime')

    netw.display([FAST,SLOW,MACROPHAGE], show_edge_labels=False)
