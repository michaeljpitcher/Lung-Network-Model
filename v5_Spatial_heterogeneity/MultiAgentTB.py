from LungMetapopulationNetwork import *

FAST = 'fast'
SLOW = 'slow'
INTRACELLULAR = 'intracellular'
RESTING = 'resting'
ACTIVE = 'active'
INFECTED = 'infected'
CHRONICALLY_INFECTED = 'chr_infected'
P_REPLICATE_FAST = 'replication_fast'
P_REPLICATE_SLOW = 'replication_slow'
P_INGEST_REST_FAST = 'resting_ingests_fast'
P_INGEST_REST_SLOW = 'resting_ingests_slow'
P_INGEST_ACTIVE_FAST = 'active_ingests_fast'
P_INGEST_ACTIVE_SLOW = 'active_ingests_slow'
P_INGEST_INFECTED_FAST = 'infected_ingests_fast'
P_INGEST_INFECTED_SLOW = 'infected_ingests_slow'
P_INGEST_CHR_INFECTED_FAST = 'chronically_infected_ingests_fast'
P_INGEST_CHR_INFECTED_SLOW = 'chronically_infected_ingests_slow'
P_RECRUIT = 'recruit_macrophage'
P_ACTIVATION = 'resting_activation'
P_DEACTIVATION = 'active_deactivation'
P_DEATH_RESTING = 'resting_death'
P_DEATH_ACTIVE = 'active_death'
P_DEATH_INFECTED = 'infected_death'
P_DEATH_CHR_INFECTED = 'chr_infected_death'
P_CHANGE_FAST_SLOW = 'change_fast_to_slow'
P_CHANGE_SLOW_FAST = 'change_slow_to_fast'
P_MIGRATE_FAST = 'fast_migrate'
P_MIGRATE_SLOW = 'slow_migrate'


class TBMultiAgentMetapopulationNetwork(LungMetapopulationNetwork):

    def __init__(self, rates, initial_loads, weight_method=HORSFIELD):

        compartments_bac = [FAST, SLOW, INTRACELLULAR]
        compartments_mac = [RESTING, ACTIVE, INFECTED, CHRONICALLY_INFECTED]

        # Create the network (allows use of networkx functions like neighbours for calculating edge weights)
        LungMetapopulationNetwork.__init__(self, compartments_bac + compartments_mac, initial_loads, weight_method)

        # Assert all rates present
        expected_rates = [P_REPLICATE_FAST, P_REPLICATE_SLOW,
                          P_INGEST_REST_FAST, P_INGEST_REST_SLOW,
                          P_INGEST_ACTIVE_FAST, P_INGEST_ACTIVE_SLOW,
                          P_INGEST_INFECTED_FAST, P_INGEST_INFECTED_SLOW,
                          P_INGEST_CHR_INFECTED_FAST, P_INGEST_CHR_INFECTED_SLOW,
                          P_RECRUIT,
                          P_ACTIVATION, P_DEACTIVATION,
                          P_DEATH_RESTING, P_DEATH_ACTIVE, P_DEATH_INFECTED, P_DEATH_CHR_INFECTED,
                          P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                          P_MIGRATE_FAST, P_MIGRATE_SLOW]

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        self.total_f = 0
        self.total_s = 0
        self.total_f_r = 0
        self.total_s_r = 0
        self.total_r = 0
        self.total_f_a = 0
        self.total_s_a = 0
        self.total_a = 0
        self.total_i_m = 0
        self.total_f_im = 0
        self.total_s_im = 0
        self.total_c = 0
        self.total_f_degree = 0
        self.total_s_degree = 0
        self.total_f_o2 = 0.0
        self.total_s_o2 = 0.0

    def update_totals(self):

        self.total_f = sum([node.subpopulations[FAST] for node in self.nodes()])
        self.total_s = sum([node.subpopulations[SLOW] for node in self.nodes()])
        self.total_f_r = sum([node.subpopulations[FAST] * node.subpopulations[RESTING] for node in self.nodes()])
        self.total_s_r = sum([node.subpopulations[SLOW] * node.subpopulations[RESTING] for node in self.nodes()])
        self.total_r = sum([node.subpopulations[RESTING] for node in self.nodes()])
        self.total_f_a = sum([node.subpopulations[FAST] * node.subpopulations[ACTIVE] for node in self.nodes()])
        self.total_s_a = sum([node.subpopulations[SLOW] * node.subpopulations[ACTIVE] for node in self.nodes()])
        self.total_a = sum([node.subpopulations[ACTIVE] for node in self.nodes()])
        self.total_i_m = sum([node.subpopulations[INFECTED] for node in self.nodes()])
        self.total_f_im = sum([node.subpopulations[FAST] * node.subpopulations[INFECTED] for node in self.nodes()])
        self.total_s_im = sum([node.subpopulations[SLOW] * node.subpopulations[INFECTED] for node in self.nodes()])
        self.total_f_c = sum([node.subpopulations[FAST] * node.subpopulations[CHRONICALLY_INFECTED] for node in self.nodes()])
        self.total_s_c = sum([node.subpopulations[SLOW] * node.subpopulations[CHRONICALLY_INFECTED] for node in self.nodes()])
        self.total_c = sum([node.subpopulations[CHRONICALLY_INFECTED] for node in self.nodes()])
        # TODO - check usage of degree
        self.total_f_degree = sum([node.subpopulations[FAST] * self.degree(node) for node in self.nodes()])
        self.total_s_degree = sum([node.subpopulations[SLOW] * self.degree(node) for node in self.nodes()])
        self.total_f_O2 = sum([node.subpopulations['F'] * node.attributes[OXYGEN_TENSION] for node in self.nodes()])
        self.total_s_O2 = sum([node.subpopulations['S'] * node.attributes[OXYGEN_TENSION] for node in self.nodes()])

    def events(self):

        events = []

        self.update_totals()

        # Replication (FAST)
        events.append((self.total_f * self.rates[P_REPLICATE_FAST], self.replicate(FAST)))
        # Replication (SLOW)
        events.append((self.total_f * self.rates[P_REPLICATE_SLOW], self.replicate(SLOW)))

        # Resting ingests fast
        events.append((self.total_f_r * self.rates[P_INGEST_REST_FAST], self.ingest(RESTING, FAST)))
        # Resting ingests slow
        events.append((self.total_s_r * self.rates[P_INGEST_REST_FAST], self.ingest(RESTING, SLOW)))
        # Active ingests fast
        events.append((self.total_f_a * self.rates[P_INGEST_ACTIVE_FAST], self.ingest(ACTIVE, FAST)))
        # Active ingests slow
        events.append((self.total_s_a * self.rates[P_INGEST_ACTIVE_SLOW], self.ingest(ACTIVE, SLOW)))
        # Inf ingests fast
        events.append((self.total_f_im * self.rates[P_INGEST_INFECTED_FAST], self.ingest(INFECTED, FAST)))
        # Inf ingests slow
        events.append((self.total_s_im * self.rates[P_INGEST_INFECTED_SLOW], self.ingest(INFECTED, SLOW)))
        # Chr Inf ingests fast
        events.append((self.total_f_c * self.rates[P_INGEST_INFECTED_FAST], self.ingest(INFECTED, FAST)))
        # Chr Inf ingests slow
        events.append((self.total_s_ic * self.rates[P_INGEST_INFECTED_SLOW], self.ingest(INFECTED, SLOW)))

        # Recruit mac
        # TODO - this should probably be based on the level of infection
        events.append((len(self.nodes()) * self.rates[P_RECRUIT], self.recruit_mac()))

        # Activate mac
        # TODO - this should probably be based on the level of infection
        events.append((self.total_r * self.rates[P_ACTIVATION], self.activate()))

        # Deactivate mac
        # TODO - this should probably be based on the level of infection
        events.append((self.total_a * self.rates[P_DEACTIVATION], self.deactivate()))

        # Death of mac
        # Resting
        events.append((self.total_r * self.rates[P_DEATH_RESTING], self.death_mac(RESTING)))
        # Active
        events.append((self.total_a * self.rates[P_DEATH_ACTIVE], self.death_mac(ACTIVE)))
        # Inf
        events.append((self.total_i_m * self.rates[P_DEATH_INFECTED], self.death_mac(INFECTED)))
        # Chr Inf
        events.append((self.total_c * self.rates[P_DEATH_CHR_INFECTED], self.death_mac(CHRONICALLY_INFECTED)))

        # Metabolism change
        events.append((self.total_f_o2 * self.rates[P_CHANGE_FAST_SLOW], self.change(SLOW)))
        events.append((self.total_s_o2 * self.rates[P_CHANGE_SLOW_FAST], self.change(FAST)))

        # Migrate
        events.append((self.total_f_degree * self.rates[P_MIGRATE_FAST], self.migrate(FAST)))
        events.append((self.total_s_degree * self.rates[P_MIGRATE_SLOW], self.migrate(SLOW)))

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

    def ingest(self, mac_state, metabolism):
        if metabolism == FAST:
            if mac_state == RESTING:
                total = self.total_f_r
            elif mac_state == ACTIVE:
                total = self.total_f_a
            elif mac_state == INFECTED:
                total = self.total_f_im
            elif mac_state == CHRONICALLY_INFECTED:
                total = self.total_f_c
            else:
                raise Exception, "Invalid ingest: macrophage {0} not valid".format(mac_state)
        elif metabolism == SLOW:
            if mac_state == RESTING:
                total = self.total_s_r
            elif mac_state == ACTIVE:
                total = self.total_s_a
            elif mac_state == INFECTED:
                total = self.total_s_im
            elif mac_state == CHRONICALLY_INFECTED:
                total = self.total_s_c
            else:
                raise Exception, "Invalid ingest: macrophage {0} not valid".format(mac_state)
        else:
            raise Exception, "Invalid ingest: bacteria {0} not valid".format(metabolism)

        r = np.random.random() * total

        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[metabolism] * node.subpopulations[mac_state]
            if running_total >= r:
                self.update_node(node, metabolism, -1)
                if mac_state != ACTIVE:
                    self.update_node(node, INTRACELLULAR, 1)
                    if mac_state == RESTING:
                        self.update_node(node, RESTING, -1)
                        self.update_node(node, INFECTED, 1)
                # TODO - inf to chrinf? chrinf bursts?
                return

    def recruit_mac(self):
        # TODO - as above, based on level of infection?
        node = np.random.choice(self.nodes(),1)
        self.update_node(node, RESTING, 1)

    def activate(self):
        r = np.random.randint(0, self.total_r)
        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[RESTING]
            if running_total >= r:
                self.update_node(node, ACTIVE, 1)
                self.update_node(node, RESTING, -1)
                return

    def deactivate(self):
        r = np.random.randint(0, self.total_a)
        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[ACTIVE]
            if running_total >= r:
                self.update_node(node, RESTING, 1)
                self.update_node(node, ACTIVE, -1)
                return

    def death_mac(self, state):
        if state == RESTING:
            r = np.random.randint(0, self.total_r)
        elif state == ACTIVE:
            r = np.random.randint(0, self.total_a)
        elif state == INFECTED:
            r = np.random.randint(0, self.total_i_m)
        elif state == CHRONICALLY_INFECTED:
            r = np.random.randint(0, self.total_c)
        else:
            raise Exception, "Invalid death: macrophage {0} not valid".format(state)

        running_total = 0
        for node in self.nodes():
            running_total += node.subpopulations[state]
            if running_total >= r:
                self.update_node(node, state, -1)
                # TODO maybe add caseum
                return

    def migrate(self, metabolism):
        # TODO - check usage of degree / weights
        if metabolism == FAST:
            r = np.random.randint(0, self.total_f_degree)
        elif metabolism == SLOW:
            r = np.random.randint(0, self.total_s_degree)
        else:
            raise Exception, "Invalid translocate: {0} not valid".format(metabolism)

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
    rates[FAST] = 0.0
    rates[SLOW] = 0.0
    rates[INTRACELLULAR] = 0.0
    rates[RESTING] = 0.0
    rates[ACTIVE] = 0.0
    rates[INFECTED] = 0.0
    rates[CHRONICALLY_INFECTED] = 0.0
    rates[P_REPLICATE_FAST] = 0.0
    rates[P_REPLICATE_SLOW] = 0.0
    rates[P_INGEST_REST_FAST] = 0.0
    rates[P_INGEST_REST_SLOW] = 0.0
    rates[P_INGEST_ACTIVE_FAST] = 0.0
    rates[P_INGEST_ACTIVE_SLOW] = 0.0
    rates[P_INGEST_INFECTED_FAST] = 0.0
    rates[P_INGEST_INFECTED_SLOW] = 0.0
    rates[P_INGEST_CHR_INFECTED_FAST] = 0.0
    rates[P_INGEST_CHR_INFECTED_SLOW] = 0.0
    rates[P_RECRUIT] = 0.0
    rates[P_ACTIVATION] = 0.0
    rates[P_DEACTIVATION] = 0.0
    rates[P_DEATH_RESTING] = 0.0
    rates[P_DEATH_ACTIVE] = 0.0
    rates[P_DEATH_INFECTED] = 0.0
    rates[P_DEATH_CHR_INFECTED] = 0.0
    rates[P_MIGRATE_FAST] = 0.0
    rates[P_MIGRATE_SLOW] = 0.0
    rates[P_CHANGE_FAST_SLOW] = 0.0
    rates[P_CHANGE_SLOW_FAST] = 0.0

    loads = dict()

    netw = TBMultiAgentMetapopulationNetwork(rates, loads)

    netw.display(show_node_contents=True, show_edge_labels=False)





