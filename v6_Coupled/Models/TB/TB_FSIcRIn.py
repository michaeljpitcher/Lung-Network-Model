__author__ = "Michael J. Pitcher"

from ..Lung.LungLymphNetwork import *

FAST_BACTERIA_TO_LOAD = 'load_fast_bacteria'
SLOW_BACTERIA_TO_LOAD = 'load_slow_bacteria'
MACROPHAGES_PER_BPS = 'macs_per_bps'
MACROPHAGES_PER_LYMPH = 'macs_per_lymph'

BACTERIA_FAST = 'bacteria_fast'
BACTERIA_SLOW = 'bacteria_slow'
BACTERIA_INTRACELLULAR = 'bacteria_intracellular'
MACROPHAGE_REGULAR = 'regular_macrophage'
MACROPHAGE_INFECTED = 'infected_macrophage'

P_REPLICATE_FAST = 'prob_replication_fast'
P_REPLICATE_SLOW = 'prob_replication_slow'
P_REPLICATE_INTRACELLULAR = 'prob_replication_intracellular'
P_MIGRATE_FAST = 'prob_migrate_fast'
P_MIGRATE_SLOW = 'prob_migrate_slow'
P_CHANGE_FAST_TO_SLOW = 'prob_change_fast_to_slow'
P_CHANGE_SLOW_TO_FAST = 'prob_change_slow_to_fast'
P_BPS_RECRUIT_MACROPHAGE = 'prob_bps_recruit_mac'
P_LYMPH_RECRUIT_MACROPHAGE = 'prob_lymph_recruit_mac'
P_DEATH_REGULAR_MACROPHAGE = 'prob_death_reg_mac'
P_DEATH_INFECTED_MACROPHAGE = 'prob_death_inf_mac'
P_REGULAR_MACROPHAGE_INGEST_FAST = 'prob_reg_mac_ingest_fast'
P_REGULAR_MACROPHAGE_INGEST_SLOW = 'prob_reg_mac_ingest_slow'
P_INFECTED_MACROPHAGE_INGEST_FAST = 'prob_inf_mac_ingest_fast'
P_INFECTED_MACROPHAGE_INGEST_SLOW = 'prob_inf_mac_ingest_slow'
P_MIGRATE_REGULAR_MACROPHAGE = 'prob_reg_mac_migrate'
P_MIGRATE_INFECTED_MACROPHAGE = 'prob_inf_mac_migrate'


class TB_FSIcRIn(LungLymphNetwork):

    def __init__(self, positions, parameters, weight_method=HORSFIELD):

        species = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, MACROPHAGE_INFECTED]

        expected_parameters = [FAST_BACTERIA_TO_LOAD, SLOW_BACTERIA_TO_LOAD,
                               MACROPHAGES_PER_BPS, MACROPHAGES_PER_LYMPH,
                               P_REPLICATE_FAST, P_REPLICATE_SLOW,
                               P_MIGRATE_FAST, P_MIGRATE_SLOW,
                               P_CHANGE_FAST_TO_SLOW, P_CHANGE_SLOW_TO_FAST,
                               P_BPS_RECRUIT_MACROPHAGE, P_LYMPH_RECRUIT_MACROPHAGE,
                               P_DEATH_REGULAR_MACROPHAGE, P_DEATH_INFECTED_MACROPHAGE,
                               P_REGULAR_MACROPHAGE_INGEST_FAST, P_REGULAR_MACROPHAGE_INGEST_SLOW,
                               P_INFECTED_MACROPHAGE_INGEST_FAST, P_INFECTED_MACROPHAGE_INGEST_SLOW,
                               P_MIGRATE_REGULAR_MACROPHAGE, P_MIGRATE_INFECTED_MACROPHAGE]

        for param in expected_parameters:
            assert param in parameters, "Parameter {0} not provided".format(param)

        self.parameters = parameters

        loads = dict()
        for node in range(0, 36):
            loads[node] = dict()
            loads[node][MACROPHAGE_REGULAR] = self.parameters[MACROPHAGES_PER_BPS]

        for node in range(36, 45):
            loads[node] = dict()
            loads[node][MACROPHAGE_REGULAR] = self.parameters[MACROPHAGES_PER_LYMPH]

        LungLymphNetwork.__init__(self, species, loads, positions, weight_method)

        # Bacteria are loaded after network creation to allow use of ventilation attributes
        # Load bacteria
        fast_to_load = self.parameters[FAST_BACTERIA_TO_LOAD]
        slow_to_load = self.parameters[SLOW_BACTERIA_TO_LOAD]
        node_to_distribute = None

        # Choose a node to load bacteria into
        total_ventilation = sum([n.ventilation for n in self.node_list_terminal_bps])
        r = np.random.random() * total_ventilation
        running_total = 0.0
        for n in self.node_list_terminal_bps:
            running_total += n.ventilation
            if running_total >= r:
                node_to_distribute = n
                break

        node_to_distribute.update(BACTERIA_FAST, fast_to_load)
        node_to_distribute.update(BACTERIA_SLOW, slow_to_load)

        # Totals
        self.total_fast_bac = self.total_slow_bac = self.total_intracellular_bac = \
            self.total_fast_migrate = self.total_slow_migrate = \
            self.total_fast_o2 = self.total_slow_o2 = self.total_reg_macrophage = self.total_inf_macrophage = \
            self.total_reg_mac_migrate = self.total_inf_mac_migrate = \
            self.total_reg_macrophage_and_fast = self.total_reg_macrophage_and_slow = \
            self.total_inf_macrophage_and_fast = self.total_inf_macrophage_and_slow = 0.0

    def update_totals(self):

        self.total_fast_bac = self.total_slow_bac = self.total_intracellular_bac = \
            self.total_fast_migrate = self.total_slow_migrate = \
            self.total_fast_o2 = self.total_slow_o2 = self.total_reg_macrophage = self.total_inf_macrophage = \
            self.total_reg_mac_migrate = self.total_inf_mac_migrate = \
            self.total_reg_macrophage_and_fast = self.total_reg_macrophage_and_slow = \
            self.total_inf_macrophage_and_fast = self.total_inf_macrophage_and_slow = 0.0

        for node in self.node_list_bps:
            bronchi_degree = len(self.get_neighbouring_edges(node, BRONCHUS))
            self.total_fast_bac += node.subpopulations[BACTERIA_FAST]
            self.total_slow_bac += node.subpopulations[BACTERIA_SLOW]
            self.total_intracellular_bac += node.subpopulations[BACTERIA_INTRACELLULAR]
            self.total_fast_migrate += node.subpopulations[BACTERIA_FAST] * bronchi_degree
            self.total_slow_migrate += node.subpopulations[BACTERIA_SLOW] * bronchi_degree
            self.total_fast_o2 += node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
            self.total_slow_o2 += node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension
            self.total_reg_macrophage += node.subpopulations[MACROPHAGE_REGULAR]
            self.total_inf_macrophage += node.subpopulations[MACROPHAGE_INFECTED]
            lymph_degree = len(self.get_neighbouring_edges(node, LYMPHATIC_VESSEL))
            self.total_reg_mac_migrate += node.subpopulations[MACROPHAGE_REGULAR] * lymph_degree
            self.total_inf_mac_migrate += node.subpopulations[MACROPHAGE_INFECTED] * lymph_degree
            self.total_reg_macrophage_and_fast += node.subpopulations[MACROPHAGE_REGULAR] * \
                                                  node.subpopulations[BACTERIA_FAST]
            self.total_reg_macrophage_and_slow += node.subpopulations[MACROPHAGE_REGULAR] * \
                                                  node.subpopulations[BACTERIA_SLOW]
            self.total_inf_macrophage_and_fast += node.subpopulations[MACROPHAGE_INFECTED] * \
                                                  node.subpopulations[BACTERIA_FAST]
            self.total_inf_macrophage_and_slow += node.subpopulations[MACROPHAGE_INFECTED] * \
                                                  node.subpopulations[BACTERIA_SLOW]

        for node in self.node_list_ln:
            self.total_fast_bac += node.subpopulations[BACTERIA_FAST]
            self.total_slow_bac += node.subpopulations[BACTERIA_SLOW]
            self.total_intracellular_bac += node.subpopulations[BACTERIA_INTRACELLULAR]
            self.total_reg_macrophage += node.subpopulations[MACROPHAGE_REGULAR]
            self.total_inf_macrophage += node.subpopulations[MACROPHAGE_INFECTED]
            lymph_degree = len(self.get_neighbouring_edges(node, LYMPHATIC_VESSEL))
            self.total_reg_mac_migrate += node.subpopulations[MACROPHAGE_REGULAR] * lymph_degree
            self.total_inf_mac_migrate += node.subpopulations[MACROPHAGE_INFECTED] * lymph_degree
            self.total_reg_macrophage_and_fast += node.subpopulations[MACROPHAGE_REGULAR] * \
                                                  node.subpopulations[BACTERIA_FAST]
            self.total_reg_macrophage_and_slow += node.subpopulations[MACROPHAGE_REGULAR] * \
                                                  node.subpopulations[BACTERIA_SLOW]
            self.total_inf_macrophage_and_fast += node.subpopulations[MACROPHAGE_INFECTED] * \
                                                  node.subpopulations[BACTERIA_FAST]
            self.total_inf_macrophage_and_slow += node.subpopulations[MACROPHAGE_INFECTED] * \
                                                  node.subpopulations[BACTERIA_SLOW]

    def events(self):

        self.update_totals()
        events = []

        # Replicate
        events.append((self.parameters[P_REPLICATE_FAST] * self.total_fast_bac,
                       lambda f: self.replicate(BACTERIA_FAST)))
        events.append((self.parameters[P_REPLICATE_SLOW] * self.total_slow_bac,
                       lambda f: self.replicate(BACTERIA_SLOW)))
        events.append((self.parameters[P_REPLICATE_INTRACELLULAR] * self.total_intracellular_bac,
                       lambda f: self.replicate(BACTERIA_INTRACELLULAR)))

        # Bacteria migrate
        events.append((self.parameters[P_MIGRATE_FAST] * self.total_fast_migrate,
                       lambda f: self.bacteria_migrate(BACTERIA_FAST)))
        events.append((self.parameters[P_MIGRATE_SLOW] * self.total_slow_migrate,
                       lambda f: self.bacteria_migrate(BACTERIA_SLOW)))

        # Change metabolism
        events.append((self.parameters[P_CHANGE_FAST_TO_SLOW] * self.total_fast_o2,
                       lambda f: self.change_metabolism(BACTERIA_FAST)))
        events.append((self.parameters[P_CHANGE_SLOW_TO_FAST] * self.total_slow_o2,
                       lambda f: self.change_metabolism(BACTERIA_SLOW)))

        # Macrophage recruited
        events.append((self.parameters[P_BPS_RECRUIT_MACROPHAGE] * len(self.node_list_bps),
                       lambda f: self.recruit_macrophage_bps()))
        events.append((self.parameters[P_LYMPH_RECRUIT_MACROPHAGE] * len(self.node_list_ln),
                       lambda f: self.recruit_macrophage_lymph()))

        # Macrophage death
        events.append((self.parameters[P_DEATH_REGULAR_MACROPHAGE] * self.total_reg_macrophage,
                       lambda f: self.macrophage_death(MACROPHAGE_REGULAR)))
        events.append((self.parameters[P_DEATH_INFECTED_MACROPHAGE] * self.total_inf_macrophage,
                       lambda f: self.macrophage_death(MACROPHAGE_INFECTED)))

        # Macrophage migration
        events.append((self.parameters[P_MIGRATE_REGULAR_MACROPHAGE] * self.total_reg_mac_migrate,
                       lambda f: self.macrophage_migrate(MACROPHAGE_REGULAR)))
        events.append((self.parameters[P_MIGRATE_INFECTED_MACROPHAGE] * self.total_inf_mac_migrate,
                       lambda f: self.macrophage_migrate(MACROPHAGE_INFECTED)))

        # Macrophage ingest bacteria
        events.append((self.parameters[P_REGULAR_MACROPHAGE_INGEST_FAST] * self.total_reg_macrophage_and_fast,
                       lambda f: self.ingest(MACROPHAGE_REGULAR, BACTERIA_FAST)))
        events.append((self.parameters[P_REGULAR_MACROPHAGE_INGEST_SLOW] * self.total_reg_macrophage_and_slow,
                       lambda f: self.ingest(MACROPHAGE_REGULAR, BACTERIA_SLOW)))
        events.append((self.parameters[P_INFECTED_MACROPHAGE_INGEST_FAST] * self.total_inf_macrophage_and_fast,
                       lambda f: self.ingest(MACROPHAGE_INFECTED, BACTERIA_FAST)))
        events.append((self.parameters[P_INFECTED_MACROPHAGE_INGEST_SLOW] * self.total_inf_macrophage_and_slow,
                       lambda f: self.ingest(MACROPHAGE_INFECTED, BACTERIA_SLOW)))

        return events

    def replicate(self, metabolism):

        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.total_fast_bac
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.total_slow_bac
        elif metabolism == BACTERIA_INTRACELLULAR:
            r = np.random.random() * self.total_intracellular_bac
        else:
            raise Exception("Invalid metabolism: {0}".format(metabolism))

        running_total = 0
        for node in self.node_list_bps:
            running_total += node.subpopulations[metabolism]
            if running_total > r:
                node.update(metabolism, 1)
                return

    def bacteria_migrate(self, metabolism):
        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.total_fast_migrate
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.total_slow_migrate
        else:
            raise Exception("Invalid metabolism: {0}".format(metabolism))

        running_total = 0
        for node in self.node_list_bps:
            running_total += node.subpopulations[metabolism] * self.degree(node)
            if running_total > r:
                neighbouring_edges = self.get_neighbouring_edges(node, BRONCHUS)
                total_weight = sum(data[WEIGHT] for _, data in neighbouring_edges)
                r2 = np.random.random() * total_weight
                running_neighbour_weight_total = 0
                for (neighbour, data) in neighbouring_edges:
                    running_neighbour_weight_total += data[WEIGHT]
                    if running_neighbour_weight_total > r2:
                        node.update(metabolism, -1)
                        neighbour.update(metabolism, 1)
                        return

    def change_metabolism(self, previous_metabolism):
        if previous_metabolism == BACTERIA_FAST:
            new_metabolism = BACTERIA_SLOW
            r = np.random.random() * self.total_fast_o2
        elif previous_metabolism == BACTERIA_SLOW:
            new_metabolism = BACTERIA_FAST
            r = np.random.random() * self.total_slow_o2
        else:
            raise Exception("Invalid metabolism: {0}".format(previous_metabolism))

        running_total = 0
        for node in self.node_list_bps:
            if previous_metabolism == BACTERIA_FAST:
                running_total += node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
            else:
                running_total += node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension

            if running_total > r:
                node.update(previous_metabolism, -1)
                node.update(new_metabolism, 1)
                return

    def recruit_macrophage_bps(self):
        index = np.random.randint(0, len(self.node_list_bps))
        node = self.node_list_bps[index]
        node.update(MACROPHAGE_REGULAR, 1)

    def recruit_macrophage_lymph(self):
        index = np.random.randint(0, len(self.node_list_ln))
        node = self.node_list_ln[index]
        node.update(MACROPHAGE_REGULAR, 1)

    def macrophage_death(self, mac_state):

        if mac_state == MACROPHAGE_REGULAR:
            r = np.random.random() * self.total_reg_macrophage
        elif mac_state == MACROPHAGE_INFECTED:
            r = np.random.random() * self.total_inf_macrophage
        else:
            raise Exception("Invalid macrophage state: {0}".format(mac_state))

        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[mac_state]
            if running_total > r:
                if mac_state == MACROPHAGE_INFECTED:
                    bacteria_to_disperse = int(round(node.subpopulations[BACTERIA_INTRACELLULAR] /
                                                     node.subpopulations[MACROPHAGE_INFECTED]))
                    node.update(BACTERIA_SLOW, bacteria_to_disperse)
                    node.update(BACTERIA_INTRACELLULAR, -1*bacteria_to_disperse)
                node.update(mac_state, -1)
                return

    def macrophage_migrate(self, mac_state):
        if mac_state == MACROPHAGE_REGULAR:
            r = np.random.random() * self.total_reg_mac_migrate
        elif mac_state == MACROPHAGE_INFECTED:
            r = np.random.random() * self.total_inf_mac_migrate
        else:
            raise Exception("Invalid macrophage state: {0}".format(mac_state))

        running_total = 0
        for node in self.node_list.values():
            neighbouring_lymph_edges = self.get_neighbouring_edges(node, LYMPHATIC_VESSEL)
            running_total += node.subpopulations[mac_state] * len(neighbouring_lymph_edges)
            if running_total > r:
                neighbour_index = np.random.randint(0, len(neighbouring_lymph_edges))
                neighbour = neighbouring_lymph_edges[neighbour_index][0]
                if mac_state == MACROPHAGE_INFECTED:
                    bacteria_to_migrate = int(round(node.subpopulations[BACTERIA_INTRACELLULAR] /
                                                    node.subpopulations[MACROPHAGE_INFECTED]))
                    node.update(BACTERIA_INTRACELLULAR, -1*bacteria_to_migrate)
                    neighbour.update(BACTERIA_INTRACELLULAR, bacteria_to_migrate)
                node.update(mac_state, -1)
                neighbour.update(mac_state, 1)
                return

    def ingest(self, mac_state, bacteria_metabolism):
        if bacteria_metabolism == BACTERIA_FAST and mac_state == MACROPHAGE_REGULAR:
            r = np.random.random() * self.total_reg_macrophage_and_fast
        elif bacteria_metabolism == BACTERIA_SLOW and mac_state == MACROPHAGE_REGULAR:
            r = np.random.random() * self.total_reg_macrophage_and_slow
        elif bacteria_metabolism == BACTERIA_FAST and mac_state == MACROPHAGE_INFECTED:
            r = np.random.random() * self.total_inf_macrophage_and_fast
        elif bacteria_metabolism == BACTERIA_SLOW and mac_state == MACROPHAGE_INFECTED:
            r = np.random.random() * self.total_inf_macrophage_and_slow
        else:
            raise Exception("Invalid metabolism/mac state combination: {0} - {1}"
                            .format(bacteria_metabolism, mac_state))

        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[mac_state] * node.subpopulations[bacteria_metabolism]
            if running_total > r:
                node.update(bacteria_metabolism, -1)
                node.update(BACTERIA_INTRACELLULAR, 1)
                if mac_state == MACROPHAGE_REGULAR:
                    node.update(MACROPHAGE_REGULAR, -1)
                    node.update(MACROPHAGE_INFECTED, 1)
                return
