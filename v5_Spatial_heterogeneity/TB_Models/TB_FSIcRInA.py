from v5_Spatial_heterogeneity.Lung_Models.LungMetapopulationNetwork import *

BACTERIA_FAST = 'bac_fast'
BACTERIA_SLOW = 'bac_slow'
BACTERIA_INTRACELLULAR = 'bac_intra'
MACROPHAGE_REGULAR = 'mac_regular'
MACROPHAGE_INFECTED = 'mac_infected'
MACROPHAGE_ACTIVATED = 'mac_activated'

P_REPLICATE_FAST = 'replication_fast'
P_REPLICATE_SLOW = 'replication_slow'
P_REPLICATE_INTRACELLULAR = 'replication_intra'
P_CHANGE_FAST_SLOW = 'change_fast_to_slow'
P_CHANGE_SLOW_FAST = 'change_slow_to_fast'
P_MIGRATE_FAST = 'fast_migrate'
P_MIGRATE_SLOW = 'slow_migrate'

P_RECRUIT = 'recruit_macrophage'
P_DEATH_REGULAR = 'mac_regular_death'
P_DEATH_INFECTED = 'mac_infected_death'
P_DEATH_ACTIVATED = 'mac_activated_death'

P_ACTIVATION = 'activation'

P_REGULAR_INGEST_FAST = 'regular_ingests_fast'
P_REGULAR_INGEST_SLOW = 'regular_ingests_slow'
P_INFECTED_INGEST_FAST = 'infected_ingests_fast'
P_INFECTED_INGEST_SLOW = 'infected_ingests_slow'
P_ACTIVATED_INGEST_FAST = 'activated_ingests_fast'
P_ACTIVATED_INGEST_SLOW = 'activated_ingests_slow'


class TBMetapopulationNetwork_FSIcRInA(LungMetapopulationNetwork):
    """
    Metapopulation model of TB infection with host interaction.

    5 populations - Fast bacteria, slow bacteria, intracellular bacteria, regular macrophages and infected macrophages.
    Fast, slow, intracellular bacteria replicate at their own individual rates, and can migrate to new patches at their
    own rates and fast and slow can change between each other (based on oxygen in node).
    Macrophages are recruited at defined rate, ingest each type of bacteria at individual rates - ingestion of bacteria
    causes infection (removal of a regular macrophage and bacteria and addition of an infected macrophage and an
    intracellular bacteria).
    Death rates can be specified to differ between regular and infected. Death of infection returns bacteria to
    extracellular (i.e. -1 intracellular and +1 slow)

    TODO - bacteria can't die so always epidemic. Need adaptive immune system
    """

    def __init__(self, rates, number_of_macrophages_per_patch, num_fast_bacteria_to_deposit,
                 num_slow_bacteria_to_deposit, weight_method=HORSFIELD):
        """

        :param rates: Rates for events
        :param number_of_macrophages_per_patch: Number of macrophages in each node at start
        :param num_fast_bacteria_to_deposit: Number of fast bacteria to place in a terminal node
        :param num_slow_bacteria_to_deposit: Number of slow bacteria to place in a terminal node
        :param weight_method: Method to weight edges
        """

        # Assert all rates present
        expected_rates = [P_REPLICATE_FAST, P_REPLICATE_SLOW, P_REPLICATE_INTRACELLULAR,
                          P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                          P_MIGRATE_FAST, P_MIGRATE_SLOW,
                          P_REGULAR_INGEST_FAST, P_REGULAR_INGEST_SLOW,
                          P_INFECTED_INGEST_FAST, P_INFECTED_INGEST_SLOW,
                          P_ACTIVATED_INGEST_FAST, P_ACTIVATED_INGEST_SLOW,
                          P_RECRUIT, P_DEATH_REGULAR, P_DEATH_INFECTED, P_DEATH_ACTIVATED,
                          P_ACTIVATION]

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        # Initialise loads
        initial_loads = dict()
        for node_id in range(36):
            initial_loads[node_id] = dict()
            # Set initial macrophage levels
            initial_loads[node_id][MACROPHAGE_REGULAR] = number_of_macrophages_per_patch

        # Create the network
        LungMetapopulationNetwork.__init__(self, [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR,
                                                  MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED],
                                           initial_loads, weight_method)

        # Deposit bacteria based on ventilation
        total_ventilation = sum([patch.ventilation for patch in self.terminal_nodes])
        r = np.random.random() * total_ventilation
        running_total = 0
        # All bacteria are placed in one node
        for node in self.terminal_nodes:
            running_total += node.ventilation
            if running_total > r:
                node.subpopulations[BACTERIA_FAST] += num_fast_bacteria_to_deposit
                node.subpopulations[BACTERIA_SLOW] += num_slow_bacteria_to_deposit
                break

        # Initialise totals
        self.total_f = self.total_s = self.total_intra = self.total_mac_regular = self.total_mac_infected = \
            self.total_mac_activated = self.total_regular_fast = self.total_regular_slow = self.total_infected_fast = \
            self.total_infected_slow = self.total_activated_fast = self.total_activated_slow = self.total_f_degree = \
            self.total_s_degree = self.total_activation = 0
        self.total_f_o2 = self.total_s_o2 = 0.0

    def update_totals(self):
        """
        Update the totals, to be used for rate calculation for events
        :return:
        """
        # Reset counts to 0
        self.total_f = self.total_s = self.total_intra = self.total_mac_regular = self.total_mac_infected = \
            self.total_mac_activated = self.total_regular_fast = self.total_regular_slow = self.total_infected_fast = \
            self.total_infected_slow = self.total_activated_fast = self.total_activated_slow = self.total_f_degree = \
            self.total_s_degree = self.total_activation = 0
        self.total_f_o2 = self.total_s_o2 = 0.0

        for node in self.node_list.values():
            # Get values from node
            fast_in_node = node.subpopulations[BACTERIA_FAST]
            slow_in_node = node.subpopulations[BACTERIA_SLOW]
            intra_in_node = node.subpopulations[BACTERIA_INTRACELLULAR]
            reg_mac_in_node = node.subpopulations[MACROPHAGE_REGULAR]
            inf_mac_in_node = node.subpopulations[MACROPHAGE_INFECTED]
            act_mac_in_node = node.subpopulations[MACROPHAGE_ACTIVATED]
            degree = node.degree
            o2_tens = node.oxygen_tension
            # Update relevant totals
            self.total_f += fast_in_node
            self.total_s += slow_in_node
            self.total_intra += intra_in_node
            self.total_mac_regular += reg_mac_in_node
            self.total_mac_infected += inf_mac_in_node
            self.total_mac_activated += act_mac_in_node
            self.total_regular_fast += fast_in_node * reg_mac_in_node
            self.total_regular_slow += slow_in_node * reg_mac_in_node
            self.total_infected_fast += fast_in_node * inf_mac_in_node
            self.total_infected_slow += slow_in_node * inf_mac_in_node
            self.total_activated_fast += fast_in_node * act_mac_in_node
            self.total_activated_slow += slow_in_node * act_mac_in_node
            # TODO - check usage of degree
            self.total_f_degree += fast_in_node * degree
            self.total_s_degree += slow_in_node * degree
            self.total_f_o2 += fast_in_node * (1/o2_tens)
            self.total_s_o2 += slow_in_node * o2_tens
            self.total_activation += reg_mac_in_node * inf_mac_in_node

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
        events.append((self.total_intra * self.rates[P_REPLICATE_INTRACELLULAR],
                       lambda f: self.replicate(BACTERIA_INTRACELLULAR)))

        # Metabolism change - sum of (number of bacteria of metabolism in patch * o2 tension) * prob of change
        # TODO - check if this is ok
        events.append((self.total_f_o2 * self.rates[P_CHANGE_FAST_SLOW], lambda f: self.change(BACTERIA_SLOW)))
        events.append((self.total_s_o2 * self.rates[P_CHANGE_SLOW_FAST], lambda f: self.change(BACTERIA_FAST)))

        # Migrate - sum of (number of bacteria of metabolism in patch * degree of patch) * prob of migration
        events.append((self.total_f_degree * self.rates[P_MIGRATE_FAST], lambda f: self.migrate(BACTERIA_FAST)))
        events.append((self.total_s_degree * self.rates[P_MIGRATE_SLOW], lambda f: self.migrate(BACTERIA_SLOW)))

        # Recruit mac - num of nodes * prob of recruit
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

        # Activation
        events.append((self.total_activation * self.rates[P_ACTIVATION], lambda f: self.activate()))

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
        elif metabolism == BACTERIA_INTRACELLULAR:
            r = np.random.random() * self.total_intra
        else:
            raise Exception("Replication: {0} metabolism not valid".format(type))

        # Check nodes until total bac exceeds r
        running_total = 0
        for node in self.node_list.values():
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
        :param metabolism: Metabolism of bacteria being ingested
        :param mac_state: State of macrophage ingesting bacteria
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
            raise Exception("Ingest: bacteria {0} not valid".format(metabolism))

        # Count through node until count exceeds r
        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[metabolism] * node.subpopulations[mac_state]
            if running_total >= r:
                # Reduce the count for metabolism by 1
                self.update_node(node, metabolism, -1)
                self.update_node(node, BACTERIA_INTRACELLULAR, 1)
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
        node_id = np.random.randint(0, len(self.nodes()))
        node = self.node_list[node_id]
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
                # Calculate number of bacteria in mac if infected
                if state == MACROPHAGE_INFECTED:
                    amount = int(round(float(node.subpopulations[BACTERIA_INTRACELLULAR]) / float(
                        node.subpopulations[MACROPHAGE_INFECTED])))
                    self.update_node(node, BACTERIA_SLOW, amount)
                    self.update_node(node, BACTERIA_INTRACELLULAR, -1 * amount)
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
            raise Exception("Migrate: {0} not valid".format(metabolism))

        # Process each node adding count of bacteria * degree until r exceeded
        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[metabolism] * node.degree
            if running_total > r:
                # Find a new patch based on the weights of edges from node
                total_weights = sum(edge_data[EDGE_OBJECT].weight for _, _, edge_data in self.edges(node, data=True))
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                # Process all neighbours, adding edge weights until r2 exceeded
                neighbours = sorted(self.neighbors(node), key=lambda x: x.id, reverse=False)
                for neighbour in neighbours:
                    edge = self.edge[node][neighbour]
                    running_total_weights += edge[EDGE_OBJECT].weight
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
            raise Exception("Metabolism change: {0} metabolism not valid".format(new_metabolism))

        # Process all nodes, adding num of bacteria of metabolism * oxygen tension until r exceeded
        running_total = 0
        for node_id in self.node_list:
            node = self.node_list[node_id]
            running_total += node.subpopulations[old_metabolism] * node.oxygen_tension
            if running_total >= r:
                # Reduce old count by 1 and increment new count by 1
                self.update_node(node, new_metabolism, 1)
                self.update_node(node, old_metabolism, -1)
                return

    def activate(self):
        r = np.random.random() * self.total_activation
        running_total = 0
        for node_id in self.node_list:
            node = self.node_list[node_id]
            running_total += node.subpopulations[MACROPHAGE_REGULAR] * node.subpopulations[MACROPHAGE_INFECTED]
            if running_total >= r:
                self.update_node(node, MACROPHAGE_REGULAR, -1)
                self.update_node(node, MACROPHAGE_ACTIVATED, 1)
                return

    def timestep_output(self):

        output = "t=" + str(self.time)
        # Keep counts in line if self.time is less characters by adding spaces
        output += " " * (15 - len(output))
        output += " fast=" + str(self.total_f)
        output += " slow=" + str(self.total_s)
        output += " intra=" + str(self.total_intra)
        output += " reg_mac=" + str(self.total_mac_regular)
        output += " inf_mac=" + str(self.total_mac_infected)
        output += " act_mac=" + str(self.total_mac_activated)
        print output

if __name__ == '__main__':
    rates_ = dict()
    rates_[P_REPLICATE_FAST] = 0.05
    rates_[P_REPLICATE_SLOW] = 0.01
    rates_[P_REPLICATE_INTRACELLULAR] = 0.0
    rates_[P_MIGRATE_FAST] = 0.01
    rates_[P_MIGRATE_SLOW] = 0.01
    rates_[P_CHANGE_FAST_SLOW] = 0.0
    rates_[P_CHANGE_SLOW_FAST] = 0.2

    # Recruitment rate * 100 to maintain mac levels
    rates_[P_RECRUIT] = 0.01 * 100
    rates_[P_DEATH_REGULAR] = 0.01
    rates_[P_DEATH_INFECTED] = 0.1
    rates_[P_DEATH_ACTIVATED] = 0.05

    rates_[P_REGULAR_INGEST_FAST] = 0.01
    rates_[P_REGULAR_INGEST_SLOW] = 0.0
    rates_[P_INFECTED_INGEST_FAST] = 0.01
    rates_[P_INFECTED_INGEST_SLOW] = 0.0
    rates_[P_ACTIVATED_INGEST_FAST] = 0.1
    rates_[P_ACTIVATED_INGEST_SLOW] = 0.0

    rates_[P_ACTIVATION] = 0.002

    np.random.seed(101)
    netw = TBMetapopulationNetwork_FSIcRInA(rates_, 100, 10, 0)

    netw.run(50)
