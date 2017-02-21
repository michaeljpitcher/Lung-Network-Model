from v5_Spatial_heterogeneity.Lung_Models.LungLymphMetapopulationNetwork import *

BACTERIA_FAST = 'bac_fast'
BACTERIA_SLOW = 'bac_slow'
BACTERIA_INTRACELLULAR = 'bac_intra'
MACROPHAGE_REGULAR = 'mac_regular'
MACROPHAGE_INFECTED = 'mac_infected'

P_REPLICATE_FAST = 'replication_fast'
P_REPLICATE_SLOW = 'replication_slow'
P_REPLICATE_INTRACELLULAR = 'replication_intra'
P_CHANGE_FAST_SLOW = 'change_fast_to_slow'
P_CHANGE_SLOW_FAST = 'change_slow_to_fast'

P_MIGRATE_BRONCHI_FAST = 'fast_migrate_bronchi'
P_MIGRATE_BRONCHI_SLOW = 'slow_migrate_bronchi'

P_RECRUIT = 'recruit_macrophage'
P_DEATH_REGULAR = 'mac_regular_death'
P_DEATH_INFECTED = 'mac_infected_death'

P_REGULAR_INGEST_BAC = 'regular_ingests_bac'
P_INFECTED_INGEST_BAC = 'infected_ingests_bac'


class TBMetapopulationNetwork_FSIcRIn_Lymph(LungLymphMetapopulationNetwork):
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

    def __init__(self, rates, number_of_macrophages_per_bronch, number_of_macrophages_per_lymph,
                 num_fast_bacteria_to_deposit, num_slow_bacteria_to_deposit, weight_method=HORSFIELD):
        """

        :param rates: Rates for events
        :param number_of_macrophages_per_bronch: Number of macrophages in each node at start
        :param num_fast_bacteria_to_deposit: Number of fast bacteria to place in a terminal node
        :param num_slow_bacteria_to_deposit: Number of slow bacteria to place in a terminal node
        :param weight_method: Method to weight edges
        """

        # Assert all rates present
        expected_rates = [P_REPLICATE_FAST, P_REPLICATE_SLOW, P_REPLICATE_INTRACELLULAR,
                          P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                          P_MIGRATE_BRONCHI_FAST, P_MIGRATE_BRONCHI_SLOW,
                          P_REGULAR_INGEST_BAC, P_INFECTED_INGEST_BAC,
                          P_RECRUIT, P_DEATH_REGULAR, P_DEATH_INFECTED]

        for r in expected_rates:
            assert r in rates.keys(), "initialise: Rate {0} is not present".format(r)
        self.rates = rates

        # Initialise loads
        initial_loads_bronch = dict()
        for node_id in range(36):
            initial_loads_bronch[node_id] = dict()
            # Set initial macrophage levels
            initial_loads_bronch[node_id][MACROPHAGE_REGULAR] = number_of_macrophages_per_bronch

        # Initialise loads
        initial_loads_lymph = dict()
        for node_id in range(36, 42):
            initial_loads_lymph[node_id] = dict()
            # Set initial macrophage levels
            initial_loads_lymph[node_id][MACROPHAGE_REGULAR] = number_of_macrophages_per_lymph

        # Create the network
        species = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]
        # Species in bronch and lymph are same
        LungLymphMetapopulationNetwork.__init__(self, species, initial_loads_bronch, species, initial_loads_lymph,
                                           weight_method)

        # Deposit bacteria based on ventilation
        total_ventilation = sum([patch.ventilation for patch in self.alveoli])
        r = np.random.random() * total_ventilation
        running_total = 0
        # All bacteria are placed in one node
        for node in self.alveoli:
            running_total += node.ventilation
            if running_total > r:
                node.subpopulations[BACTERIA_FAST] += num_fast_bacteria_to_deposit
                node.subpopulations[BACTERIA_SLOW] += num_slow_bacteria_to_deposit
                break

        # Initialise totals
        self.total_f = self.total_s = self.total_intra = self.total_mac_regular = self.total_mac_infected = \
            self.total_f_o2 = self.total_s_o2 = self.total_f_migrate_bronchi = self.total_s_migrate_bronchi = \
            self.total_regular_bac = self.total_infected_bac =\
            0

    def update_totals(self):
        self.total_f = self.total_s = self.total_intra = self.total_mac_regular = self.total_mac_infected = \
            self.total_f_o2 = self.total_s_o2 = self.total_f_migrate_bronchi = self.total_s_migrate_bronchi = \
            self.total_regular_bac = self.total_infected_bac = \
            0

        # Update Bronchopulmonary segment totals
        for node in self.node_list_bps:
            self.total_f += node.subpopulations[BACTERIA_FAST]
            self.total_s += node.subpopulations[BACTERIA_SLOW]
            self.total_intra += node.subpopulations[BACTERIA_INTRACELLULAR]
            self.total_mac_regular += node.subpopulations[MACROPHAGE_REGULAR]
            self.total_mac_infected += node.subpopulations[MACROPHAGE_INFECTED]
            self.total_f_o2 += node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
            self.total_s_o2 += node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension
            self.total_f_migrate_bronchi += node.subpopulations[BACTERIA_FAST] * len(node.bronchi)
            self.total_s_migrate_bronchi += node.subpopulations[BACTERIA_SLOW] * len(node.bronchi)
            self.total_regular_bac += node.subpopulations[MACROPHAGE_REGULAR] * (
                node.subpopulations[BACTERIA_FAST] + node.subpopulations[BACTERIA_SLOW])
            self.total_infected_bac += node.subpopulations[MACROPHAGE_INFECTED] * (
                node.subpopulations[BACTERIA_FAST] + node.subpopulations[BACTERIA_SLOW])

        # Update lymph node total
        for node in self.node_list_lymph:
            self.total_f += node.subpopulations[BACTERIA_FAST]
            self.total_s += node.subpopulations[BACTERIA_SLOW]
            self.total_intra += node.subpopulations[BACTERIA_INTRACELLULAR]
            self.total_mac_regular += node.subpopulations[MACROPHAGE_REGULAR]
            self.total_mac_infected += node.subpopulations[MACROPHAGE_INFECTED]
            # TODO - assumes lymph nodes don't have change
            # self.total_f_o2 += node.subpopulations[BACTERIA_FAST] * 9999
            # self.total_s_o2 += node.subpopulations[BACTERIA_SLOW] * 0
            self.total_regular_bac += node.subpopulations[MACROPHAGE_REGULAR] * (
                node.subpopulations[BACTERIA_FAST] + node.subpopulations[BACTERIA_SLOW])
            self.total_infected_bac += node.subpopulations[MACROPHAGE_INFECTED] * (
                node.subpopulations[BACTERIA_FAST] + node.subpopulations[BACTERIA_SLOW])

    def events(self):
        """
        Generate a list, where each element is (x,y) - x=rate of event, y=lambda function for function of event
        :return:
        """
        events = []
        # Update the totals
        self.update_totals()

        # Replication
        events.append((self.total_f * self.rates[P_REPLICATE_FAST], lambda f: self.replicate(BACTERIA_FAST)))
        events.append((self.total_s * self.rates[P_REPLICATE_SLOW], lambda f: self.replicate(BACTERIA_SLOW)))
        events.append((self.total_intra * self.rates[P_REPLICATE_INTRACELLULAR],
                       lambda f: self.replicate(BACTERIA_INTRACELLULAR)))

        # Change metabolism
        events.append((self.total_f_o2 * self.rates[P_CHANGE_FAST_SLOW], lambda f: self.change(BACTERIA_SLOW)))
        events.append((self.total_s_o2 * self.rates[P_CHANGE_SLOW_FAST], lambda f: self.change(BACTERIA_FAST)))

        # Bac migrate - bronchi
        events.append((self.total_f_migrate_bronchi * self.rates[P_MIGRATE_BRONCHI_FAST], lambda f: self.migrate_bronchi(BACTERIA_FAST)))
        events.append((self.total_s_migrate_bronchi * self.rates[P_MIGRATE_BRONCHI_SLOW], lambda f: self.migrate_bronchi(BACTERIA_SLOW)))

        # Recruit
        # TODO - assumes recruit is even at bps and lymph
        events.append((len(self.node_list) * self.rates[P_RECRUIT], lambda f: self.recruit_mac()))

        # Death mac
        # Death of mac - total number of macs * prob of death
        events.append((self.total_mac_regular * self.rates[P_DEATH_REGULAR],
                       lambda f: self.death_mac(MACROPHAGE_REGULAR)))
        events.append((self.total_mac_infected * self.rates[P_DEATH_INFECTED],
                       lambda f: self.death_mac(MACROPHAGE_INFECTED)))

        # Ingest
        events.append((self.total_regular_bac * self.rates[P_REGULAR_INGEST_BAC],
                       lambda f: self.ingest(MACROPHAGE_REGULAR)))
        events.append((self.total_infected_bac * self.rates[P_INFECTED_INGEST_BAC],
                       lambda f: self.ingest(MACROPHAGE_INFECTED)))

        # Mac drain lymph

        # Mac migrate lymph

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

        # Check all nodes until total bac exceeds r
        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[metabolism]
            if running_total > r:
                assert node.subpopulations[metabolism] > 0, "Error: no bacteria of {0} metabolism present" \
                    .format(metabolism)
                # Increment the count by 1
                self.update_node(node, metabolism, 1)
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

        # Process all bps nodes, adding num of bacteria of metabolism * oxygen tension until r exceeded
        running_total = 0
        for node in self.node_list_bps:
            if new_metabolism == BACTERIA_SLOW:
                running_total += node.subpopulations[old_metabolism] * (1/node.oxygen_tension)
            else:
                running_total += node.subpopulations[old_metabolism] * node.oxygen_tension
            if running_total >= r:
                # Reduce old count by 1 and increment new count by 1
                self.update_node(node, new_metabolism, 1)
                self.update_node(node, old_metabolism, -1)
                return

    def migrate_bronchi(self, metabolism):
        """
        A bacteria of given metabolism moves from one bronchopulmonary segment to another.
        New patch depends on edge weights.
        :param metabolism:
        :return:
        """
        # TODO - check usage of degree / weights

        # Generate r based on metabolism and degree
        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.total_f_migrate_bronchi
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.total_s_migrate_bronchi
        else:
            raise Exception("Migrate: {0} not valid".format(metabolism))

        # Process each node adding count of bacteria * degree until r exceeded
        running_total = 0
        for node in self.node_list_bps:
            running_total += node.subpopulations[metabolism] * len(node.bronchi)
            if running_total > r:
                # Find a new patch based on the weights of edges from node
                total_weights = sum([data[EDGE_OBJECT].weight for (_,_,data) in node.bronchi])
                r2 = np.random.random() * total_weights
                running_total_weights = 0
                # Process all neighbours, adding edge weights until r2 exceeded
                for (_, neighbour, data) in node.bronchi:
                    running_total_weights += data[EDGE_OBJECT].weight
                    if running_total_weights > r2:
                        # Move bacteria from node to neighbour
                        self.update_node(node, metabolism, -1)
                        self.update_node(neighbour, metabolism, 1)
                        return

    def recruit_mac(self):
        """
        A new macrophage is recruited to the node
        :return:
        """
        node_id = np.random.randint(0, len(self.nodes()))
        node = self.node_list[node_id]
        self.update_node(node, MACROPHAGE_REGULAR, 1)

    def death_mac(self, state):
        """
        A macrophage dies

        If infected, a number of intracellular bacteria are returned to surface as slow bacteria (taken as average
        intracellular per infected macrophage)
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

    def ingest(self, mac_state):
        """
        A macrophage ingests a bacteria, reducing the count for a chosen metabolism by 1. Macrophage may change state
        if not previously infected
        :param mac_state: State of macrophage ingesting bacteria
        :return:
        """
        # Set r based on mac state count
        if mac_state == MACROPHAGE_REGULAR:
            r = np.random.random() * self.total_regular_bac
        else:
            r = np.random.random() * self.total_infected_bac

        # Count through node until count exceeds r
        running_total = 0
        for node in self.node_list.values():
            total_bac_in_node = node.subpopulations[BACTERIA_FAST] + node.subpopulations[BACTERIA_SLOW]
            running_total += total_bac_in_node * node.subpopulations[mac_state]
            if running_total >= r:
                r2 = np.random.random() * total_bac_in_node
                # Remove a bacteria
                if node.subpopulations[BACTERIA_FAST] >= r2:
                    self.update_node(node, BACTERIA_FAST, -1)
                else:
                    self.update_node(node, BACTERIA_SLOW, -1)
                self.update_node(node, BACTERIA_INTRACELLULAR, 1)
                # If macrophage was regular it becomes infected
                if mac_state == MACROPHAGE_REGULAR:
                    self.update_node(node, MACROPHAGE_REGULAR, -1)
                    self.update_node(node, MACROPHAGE_INFECTED, 1)
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
        print output

if __name__ == '__main__':
    rates_ = dict()
    rates_[P_REPLICATE_FAST] = 0.02
    rates_[P_REPLICATE_SLOW] = 0.001
    rates_[P_REPLICATE_INTRACELLULAR] = 0.0
    rates_[P_MIGRATE_BRONCHI_FAST] = 0.01
    rates_[P_MIGRATE_BRONCHI_SLOW] = 0.01
    rates_[P_CHANGE_FAST_SLOW] = 0.0
    rates_[P_CHANGE_SLOW_FAST] = 0.2

    # Recruitment rate * 100 to maintain mac levels
    rates_[P_RECRUIT] = 0.01 * 100
    rates_[P_DEATH_REGULAR] = 0.01
    rates_[P_DEATH_INFECTED] = 0.1

    rates_[P_REGULAR_INGEST_BAC] = 0.002
    rates_[P_INFECTED_INGEST_BAC] = 0.001

    netw = TBMetapopulationNetwork_FSIcRIn_Lymph(rates_, 100, 0, 10, 0)

    netw.run(50)
    #
    netw.display([BACTERIA_FAST])
