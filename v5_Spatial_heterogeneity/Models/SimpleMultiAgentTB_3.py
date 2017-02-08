from v5_Spatial_heterogeneity.Base.LungMetapopulationNetwork import *

BACTERIA_FAST = 'bac_fast'
BACTERIA_SLOW = 'bac_slow'
MACROPHAGE_REGULAR = 'mac_regular'
MACROPHAGE_INFECTED = 'mac_infected'

P_REPLICATE_FAST = 'replication_fast'
P_REPLICATE_SLOW = 'replication_slow'
P_CHANGE_FAST_SLOW = 'change_fast_to_slow'
P_CHANGE_SLOW_FAST = 'change_slow_to_fast'
P_MIGRATE_FAST = 'fast_migrate'
P_MIGRATE_SLOW = 'slow_migrate'

P_RECRUIT = 'recruit_macrophage'
P_DEATH_REGULAR = 'mac_regular_death'
P_DEATH_INFECTED = 'mac_infected_death'

P_REGULAR_INGEST_FAST = 'regular_ingests_fast'
P_REGULAR_INGEST_SLOW = 'regular_ingests_slow'
P_INFECTED_INGEST_FAST = 'infected_ingests_fast'
P_INFECTED_INGEST_SLOW = 'infected_ingests_slow'


class TBSimpleMultiAgentMetapopulationNetwork_v3(LungMetapopulationNetwork):
    """
    Metapopulation model of TB infection with host interaction.

    4 populations - Fast bacteria, slow bacteria, regular macrophages and infected macrophages.
    Fast and slow bacteria replicate at their own individual rates, and can migrate to new patches at their own rates
    and can change between each other.
    Macrophages are recruited at defined rate, ingest each type of bacteria at individual rates - ingestion of bacteria
    causes infection (removal of a regular macrophage and bacteria and addition of an infected macrophage). Death
    rates can be specified to differ between regular and infected.

    Spatial element - bacteria rate of change fast-slow differs based on the oxygen tension attribute of the patch
    """

    def __init__(self, rates, number_of_macrophages_per_patch, number_of_fast_bacteria, number_of_slow_bacteria,
                 weight_method=HORSFIELD):
        """

        :param rates: Rates for events
        :param number_of_macrophages_per_patch: Number of macrophages in each patch at start
        :param number_of_fast_bacteria: Number of fast bacteria to be deposited
        :param number_of_slow_bacteria: Number of slow bacteria to be deposited
        :param weight_method: Method for weighting edges
        """

        # Initialise loads
        initial_loads = dict()
        for id in range(36):
            initial_loads[id] = dict()
            # Set initial macrophage levels
            initial_loads[id][MACROPHAGE_REGULAR] = number_of_macrophages_per_patch

        # Create the network
        LungMetapopulationNetwork.__init__(self, [BACTERIA_FAST, BACTERIA_SLOW, MACROPHAGE_REGULAR,
                                                  MACROPHAGE_INFECTED], initial_loads, weight_method)

        # Deposit bacteria based on ventilation
        # Bacteria deposition
        total_ventilation = sum([patch.attributes[VENTILATION] for patch in self.terminal_nodes])
        for i in range(number_of_fast_bacteria):
            self.deposit_bacteria(total_ventilation, BACTERIA_FAST)
        for i in range(number_of_slow_bacteria):
            self.deposit_bacteria(total_ventilation, BACTERIA_SLOW)

        # Assert all rates present
        expected_rates = [P_REPLICATE_FAST, P_REPLICATE_SLOW,
                          P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                          P_MIGRATE_FAST, P_MIGRATE_SLOW,
                          P_REGULAR_INGEST_FAST, P_REGULAR_INGEST_SLOW,
                          P_INFECTED_INGEST_FAST, P_INFECTED_INGEST_SLOW,
                          P_RECRUIT, P_DEATH_REGULAR, P_DEATH_INFECTED]

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        # Initialise totals
        self.total_f = 0
        self.total_s = 0
        self.total_mac_regular = 0
        self.total_mac_infected = 0
        self.total_regular_fast = 0
        self.total_regular_slow = 0
        self.total_infected_fast = 0
        self.total_infected_slow = 0
        self.total_f_degree = 0
        self.total_s_degree = 0
        self.total_f_o2 = 0.0
        self.total_s_o2 = 0.0

    def deposit_bacteria(self, total_ventilation, metabolism):
        r = np.random.random() * total_ventilation
        running_total = 0
        for node in self.terminal_nodes:
            running_total += node.attributes[VENTILATION]
            if running_total > r:
                node.subpopulations[metabolism] += 1
                return

    def update_totals(self):
        """
        Update the totals, to be used for rate calculation for events
        :return:
        """
        self.total_f = 0
        self.total_s = 0
        self.total_mac_regular = 0
        self.total_mac_infected = 0
        self.total_regular_fast = 0
        self.total_regular_slow = 0
        self.total_infected_fast = 0
        self.total_infected_slow = 0
        self.total_f_degree = 0
        self.total_s_degree = 0
        self.total_f_o2 = 0.0
        self.total_s_o2 = 0.0

        for node in self.node_list.values():
            self.total_f += node.subpopulations[BACTERIA_FAST]
            self.total_s += node.subpopulations[BACTERIA_SLOW]
            self.total_mac_regular += node.subpopulations[MACROPHAGE_REGULAR]
            self.total_mac_infected += node.subpopulations[MACROPHAGE_INFECTED]
            self.total_regular_fast += node.subpopulations[BACTERIA_FAST] * node.subpopulations[MACROPHAGE_REGULAR]
            self.total_regular_slow += node.subpopulations[BACTERIA_SLOW] * node.subpopulations[MACROPHAGE_REGULAR]
            self.total_infected_fast += node.subpopulations[BACTERIA_FAST] * node.subpopulations[MACROPHAGE_INFECTED]
            self.total_infected_slow += node.subpopulations[BACTERIA_SLOW] * node.subpopulations[MACROPHAGE_INFECTED]
            # TODO - check usage of degree
            self.total_f_degree += node.subpopulations[BACTERIA_FAST] * node.degree
            self.total_s_degree += node.subpopulations[BACTERIA_SLOW] * node.degree
            self.total_f_o2 += node.subpopulations[BACTERIA_FAST] * (1/node.attributes[OXYGEN_TENSION])
            self.total_s_o2 += node.subpopulations[BACTERIA_SLOW] * node.attributes[OXYGEN_TENSION]

    def events(self):
        """
        Generate a list, where each element is (x,y) - x=rate of event, y=lambda function for function of event
        :return:
        """

        events = []
        # Update the totals
        self.update_totals()

        # Replication - total number of bacteria of metabolism * prob of replication
        events.append((self.total_f * self.rates[P_REPLICATE_FAST], lambda f: self.replicate(BACTERIA_FAST)))
        events.append((self.total_s * self.rates[P_REPLICATE_SLOW], lambda f: self.replicate(BACTERIA_SLOW)))

        # Metabolism change - sum of (number of bacteria of metabolism in patch * o2 tension) * prob of change
        # TODO - check if this is ok
        events.append((self.total_f_o2 * self.rates[P_CHANGE_FAST_SLOW], lambda f: self.change(BACTERIA_SLOW)))
        events.append((self.total_s_o2 * self.rates[P_CHANGE_SLOW_FAST], lambda f: self.change(BACTERIA_FAST)))

        # Migrate - sum of (number of bacteria of metabolism in patch * degree of patch) * prob of migration
        events.append((self.total_f_degree * self.rates[P_MIGRATE_FAST], lambda f: self.migrate(BACTERIA_FAST)))
        events.append((self.total_s_degree * self.rates[P_MIGRATE_SLOW], lambda f: self.migrate(BACTERIA_SLOW)))

        # Recruit mac - num of nodes * prob of recruit
        # TODO - this should probably be based on the level of infection
        events.append((len(self.nodes()) * self.rates[P_RECRUIT], lambda f: self.recruit_mac()))

        # Death of mac - total number of macs * prob of death
        events.append((self.total_mac_regular * self.rates[P_DEATH_REGULAR],
                       lambda f: self.death_mac(MACROPHAGE_REGULAR)))
        events.append((self.total_mac_infected * self.rates[P_DEATH_INFECTED],
                       lambda f: self.death_mac(MACROPHAGE_INFECTED)))

        # Mac ingest - sum of (number of bacteria of metabolism in patch * num of macrophages in patch) * prob of ingest
        events.append((self.total_regular_fast * self.rates[P_REGULAR_INGEST_FAST],
                       lambda f: self.ingest(BACTERIA_FAST, MACROPHAGE_REGULAR)))
        events.append((self.total_regular_slow * self.rates[P_REGULAR_INGEST_SLOW],
                       lambda f: self.ingest(BACTERIA_SLOW, MACROPHAGE_REGULAR)))
        events.append((self.total_infected_fast * self.rates[P_INFECTED_INGEST_FAST],
                       lambda f: self.ingest(BACTERIA_FAST, MACROPHAGE_INFECTED)))
        events.append((self.total_infected_slow * self.rates[P_INFECTED_INGEST_SLOW],
                       lambda f: self.ingest(BACTERIA_SLOW, MACROPHAGE_INFECTED)))

        return events

    def replicate(self, metabolism):
        """
        A bacteria replicates, creating a new bacteria of identical metabolism
        :param metabolism: FAST or SLOW
        :return:
        """
        # Set r based on metabolism
        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.total_f
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.total_s
        else:
            raise Exception, "Replication: {0} metabolism not valid".format(type)

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

    def ingest(self, metabolism, mac_state):
        """
        A macrophage ingests a bacteria, reducing the count for given metabolism by 1
        :param metabolism:
        :return:
        """
        # Set r based on metabolism count
        if metabolism == BACTERIA_FAST:
            if mac_state == MACROPHAGE_REGULAR:
                r = np.random.random() * self.total_regular_fast
            else:
                r = np.random.random() * self.total_infected_fast
        elif metabolism == BACTERIA_SLOW:
            if mac_state == MACROPHAGE_REGULAR:
                r = np.random.random() * self.total_regular_slow
            else:
                r = np.random.random() * self.total_infected_slow
        else:
            raise Exception, "Ingest: bacteria {0} not valid".format(metabolism)

        # Count through node until count exceeds r
        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[metabolism] * node.subpopulations[mac_state]
            if running_total >= r:
                # Reduce the count for metabolism by 1
                self.update_node(node, metabolism, -1)
                if mac_state == MACROPHAGE_REGULAR:
                    self.update_node(node, MACROPHAGE_REGULAR, -1)
                    self.update_node(node, MACROPHAGE_INFECTED, 1)
                return

    def recruit_mac(self):
        """
        A new macrophage is recruited to the patch
        :return:
        """
        # TODO - Based on level of infection?
        id = np.random.randint(0, len(self.nodes()))
        node = self.node_list[id]
        self.update_node(node, MACROPHAGE_REGULAR, 1)

    def death_mac(self, state):
        """
        A macrophage dies
        :return:
        """
        # Generate r based on total mac numbers
        if state == MACROPHAGE_REGULAR:
            r = np.random.random() * self.total_mac_regular
        else:
            r = np.random.random() * self.total_mac_infected

        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[state]
            if running_total >= r:
                # reduce the macrophage count by 1
                self.update_node(node, state, -1)
                return

    def migrate(self, metabolism):
        """
        A bacteria of given metabolism moves from one patch to another. New patch depends on edge weights.
        :param metabolism:
        :return:
        """
        # TODO - check usage of degree / weights

        # Generate r based on metabolism and degree
        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.total_f_degree
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.total_s_degree
        else:
            raise Exception, "Migrate: {0} not valid".format(metabolism)

        # Process each node adding count of bacteria * degree until r exceeded
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[metabolism] * node.degree
            if running_total > r:
                # Find a new patch based on the weights of edges from node
                total_weights = sum(edge_data[WEIGHT] for _, _, edge_data in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                # Process all neighbours, adding edge weights until r2 exceeded
                neighbours = sorted(self.neighbors(node), key=lambda x: x.id, reverse=False)
                for neighbour in neighbours:
                    edge = self.edge[node][neighbour]
                    running_total_weights += edge[WEIGHT]
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
        if new_metabolism == BACTERIA_FAST:
            r = np.random.random() * self.total_s_o2
            old_metabolism = BACTERIA_SLOW
        elif new_metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.total_f_o2
            old_metabolism = BACTERIA_FAST
        else:
            raise Exception, "Metabolism change: {0} metabolism not valid".format(new_metabolism)

        # Process all nodes, adding num of bacteria of metabolism * oxygen tension until r exceeded
        running_total = 0
        for id in self.node_list:
            node = self.node_list[id]
            running_total += node.subpopulations[old_metabolism] * node.attributes[OXYGEN_TENSION]
            if running_total >= r:
                # Reduce old count by 1 and increment new count by 1
                self.update_node(node, new_metabolism, 1)
                self.update_node(node, old_metabolism, -1)
                return

    def timestep_output(self):
        print "t=", self.time, "bac=", self.total_f + self.total_s, "mac=", self.total_mac_infected + \
                                                                            self.total_mac_regular

if __name__ == '__main__':
    rates = dict()
    rates[P_REPLICATE_FAST] = 0.1
    rates[P_REPLICATE_SLOW] = 0.01
    rates[P_MIGRATE_FAST] = 0.01
    rates[P_MIGRATE_SLOW] = 0.001
    rates[P_CHANGE_FAST_SLOW] = 0.3
    rates[P_CHANGE_SLOW_FAST] = 0.2

    # Recruitment rate * 100 to maintain mac levels
    rates[P_RECRUIT] = 0.01 * 100
    rates[P_DEATH_REGULAR] = 0.01
    rates[P_DEATH_INFECTED] = 0.1

    rates[P_REGULAR_INGEST_FAST] = 0.01
    rates[P_REGULAR_INGEST_SLOW] = 0.01
    rates[P_INFECTED_INGEST_FAST] = 0.01
    rates[P_INFECTED_INGEST_SLOW] = 0.01

    netw = TBSimpleMultiAgentMetapopulationNetwork_v3(rates, 100, 10, 10)

    netw.run(100)

    netw.display(node_contents_species=[MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, BACTERIA_FAST, BACTERIA_SLOW])
