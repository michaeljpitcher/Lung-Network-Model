from LungMetapopulationNetwork import *

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


class TBMultiAgentMetapopulationNetwork(LungMetapopulationNetwork):

    def __init__(self, rates, initial_loads, weight_method=HORSFIELD):

        compartments_bac = [FAST, SLOW]
        compartments_mac = [MACROPHAGE]

        # Create the network (allows use of networkx functions like neighbours for calculating edge weights)
        LungMetapopulationNetwork.__init__(self, compartments_bac + compartments_mac, initial_loads, weight_method)

        # Assert all rates present
        expected_rates = [P_REPLICATE_FAST, P_REPLICATE_SLOW,
                          P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                          P_MIGRATE_FAST, P_MIGRATE_SLOW,
                          P_INGEST_FAST, P_INGEST_SLOW,
                          P_RECRUIT, P_DEATH]

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

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

        self.total_f = sum([node.subpopulations[FAST] for node in self.nodes()])
        self.total_s = sum([node.subpopulations[SLOW] for node in self.nodes()])

        self.total_mac = sum([node.subpopulations[MACROPHAGE] for node in self.nodes()])

        self.total_mac_fast = sum(
            [node.subpopulations[FAST] * node.subpopulations[MACROPHAGE] for node in self.nodes()])
        self.total_mac_fast = sum(
            [node.subpopulations[SLOW] * node.subpopulations[MACROPHAGE] for node in self.nodes()])

        # TODO - check usage of degree
        self.total_f_degree = sum([node.subpopulations[FAST] * self.degree(node) for node in self.nodes()])
        self.total_s_degree = sum([node.subpopulations[SLOW] * self.degree(node) for node in self.nodes()])
        self.total_f_O2 = sum([node.subpopulations[FAST] * node.attributes[OXYGEN_TENSION] for node in self.nodes()])
        self.total_s_O2 = sum([node.subpopulations[SLOW] * node.attributes[OXYGEN_TENSION] for node in self.nodes()])


    def events(self):

        events = []

        self.update_totals()

        # Replication
        events.append((self.total_f * self.rates[P_REPLICATE_FAST], lambda f: self.replicate(FAST)))
        events.append((self.total_f * self.rates[P_REPLICATE_SLOW], lambda f: self.replicate(SLOW)))

        # Metabolism change
        events.append((self.total_f_o2 * self.rates[P_CHANGE_FAST_SLOW], lambda f: self.change(SLOW)))
        events.append((self.total_s_o2 * self.rates[P_CHANGE_SLOW_FAST], lambda f: self.change(FAST)))

        # Migrate
        events.append((self.total_f_degree * self.rates[P_MIGRATE_FAST], lambda f: self.migrate(FAST)))
        events.append((self.total_s_degree * self.rates[P_MIGRATE_SLOW], lambda f: self.migrate(SLOW)))

        # Recruit mac
        # TODO - this should probably be based on the level of infection
        events.append((len(self.nodes()) * self.rates[P_RECRUIT], lambda f: self.recruit_mac()))

        # Death of mac
        events.append((self.total_mac * self.rates[P_DEATH], lambda f: self.death_mac()))

        # Mac ingest fast
        events.append((self.total_mac_fast * self.rates[P_INGEST_FAST], lambda f: self.ingest(FAST)))
        # Mac ingest slow
        events.append((self.total_mac_slow * self.rates[P_INGEST_SLOW], lambda f: self.ingest(SLOW)))

        return events


    def replicate(self, metabolism):
        if metabolism == FAST:
            r = np.random.random() * self.total_f
            rate = self.rates[P_REPLICATE_FAST]
        elif metabolism == SLOW:
            r = np.random.random() * self.total_s
            rate = self.rates[P_REPLICATE_SLOW]
        else:
            raise Exception, "Invalid replication: {0} metabolism not valid".format(type)

        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[metabolism]
            if running_total >= r:
                if rate > 0:
                    self.update_node(node, metabolism, 1)
                elif rate < 0:
                    self.update_node(node, metabolism, -1)
                return

    def ingest(self, metabolism):
        if metabolism == FAST:
            total = self.total_mac_fast
        elif metabolism == SLOW:
            total = self.total_mac_slow
        else:
            raise Exception, "Invalid ingest: bacteria {0} not valid".format(metabolism)

        r = np.random.random() * total

        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[metabolism] * node.subpopulations[MACROPHAGE]
            if running_total >= r:
                self.update_node(node, metabolism, -1)
                # TODO - inf to chrinf? chrinf bursts?
                return

    def recruit_mac(self):
        # TODO - as above, based on level of infection?
        node = np.random.choice(self.nodes(),1)
        self.update_node(node, MACROPHAGE, 1)

    def death_mac(self):
        r = np.random.randint(0, self.total_mac)
        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[MACROPHAGE]
            if running_total >= r:
                self.update_node(node, MACROPHAGE, -1)
                return

    def migrate(self, metabolism):
        # TODO - check usage of degree / weights
        if metabolism == FAST:
            r = np.random.randint(0, self.total_f_degree)
        elif metabolism == SLOW:
            r = np.random.randint(0, self.total_s_degree)
        else:
            raise Exception, "Invalid migrate: {0} not valid".format(metabolism)

        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[metabolism]
            if running_total >= r:
                total_weights = sum(d[WEIGHT] for _, _, d in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                for _, neighbour, edge in self.edges(node, data=True):
                    running_total_weights += edge[WEIGHT]
                    if running_total_weights > r2:
                        self.update_node(node, metabolism, -1)
                        self.update_node(neighbour, metabolism, 1)
                        return

    def change(self, new_metabolism):
        if new_metabolism == FAST:
            r = np.random.random() * self.total_s
            old_metabolism = SLOW
        elif new_metabolism == SLOW:
            r = np.random.random() * self.total_f
            old_metabolism = FAST
        else:
            raise Exception, "Invalid metabolism change: {0} metabolism not valid".format(new_metabolism)

        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[old_metabolism]
            if running_total >= r:
                self.update_node(node, new_metabolism, 1)
                self.update_node(node, old_metabolism, -1)
                return


if __name__ == '__main__':
    rates = dict()
    rates[P_REPLICATE_FAST] = 0.1
    rates[P_REPLICATE_SLOW] = 0.001
    rates[P_MIGRATE_FAST] = 0.1
    rates[P_MIGRATE_SLOW] = 0.1
    rates[P_CHANGE_FAST_SLOW] = 0.1
    rates[P_CHANGE_SLOW_FAST] = 0.01

    rates[P_RECRUIT] = 0.0
    rates[P_DEATH] = 0.0

    rates[P_INGEST_FAST] = 0.0
    rates[P_INGEST_SLOW] = 0.0

    loads = dict()
    loads[0] = dict()
    loads[0][FAST] = 1

    netw = TBMultiAgentMetapopulationNetwork(rates, loads)

    netw.run(10)

    netw.display(show_node_contents=True, show_edge_labels=False)





