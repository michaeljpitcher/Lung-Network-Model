__author__ = "Michael J. Pitcher"

from ..Lung.LungLymph import *

FAST_BACTERIA_TO_LOAD = 'load_fast_bacteria'
SLOW_BACTERIA_TO_LOAD = 'load_slow_bacteria'
MACROPHAGES_PER_BPS = 'macs_per_bps'
MACROPHAGES_PER_LYMPH = 'macs_per_lymph'

BACTERIA_FAST = 'bacteria_fast'
BACTERIA_SLOW = 'bacteria_slow'
MACROPHAGE = 'macrophage'

P_REPLICATE_FAST = 'prob_replication_fast'
P_REPLICATE_SLOW = 'prob_replication_slow'
P_MIGRATE_FAST = 'prob_migrate_fast'
P_MIGRATE_SLOW = 'prob_migrate_slow'
P_CHANGE_FAST_TO_SLOW = 'prob_change_fast_to_slow'
P_CHANGE_SLOW_TO_FAST = 'prob_change_slow_to_fast'
P_BPS_RECRUIT_MACROPHAGE = 'prob_bps_recruit_mac'
P_LYMPH_RECRUIT_MACROPHAGE = 'prob_lymph_recruit_mac'
P_DEATH_MACROPHAGE = 'prob_death_mac'
P_MACROPHAGE_INGEST_FAST = 'prob_mac_ingest_fast'
P_MACROPHAGE_INGEST_SLOW = 'prob_mac_ingest_slow'
P_MIGRATE_MACROPHAGE = 'prob_mac_migrate'


class TB_FSM(LungLymph):

    def __init__(self, positions, parameters, weight_method=HORSFIELD):

        species = [BACTERIA_FAST, BACTERIA_SLOW, MACROPHAGE]

        expected_parameters = [FAST_BACTERIA_TO_LOAD, SLOW_BACTERIA_TO_LOAD,
                               P_REPLICATE_FAST, P_REPLICATE_SLOW,
                               P_MIGRATE_FAST, P_MIGRATE_SLOW,
                               P_CHANGE_FAST_TO_SLOW, P_CHANGE_SLOW_TO_FAST,
                               P_BPS_RECRUIT_MACROPHAGE, P_LYMPH_RECRUIT_MACROPHAGE, P_DEATH_MACROPHAGE,
                               P_MACROPHAGE_INGEST_FAST, P_MACROPHAGE_INGEST_SLOW,
                               P_MIGRATE_MACROPHAGE]

        for param in expected_parameters:
            assert param in parameters, "Parameter {0} not provided"

        self.parameters = parameters

        loads = dict()
        for node in self.node_list_bps:
            loads[node] = dict()
            loads[node][MACROPHAGE] = self.parameters[MACROPHAGES_PER_BPS]

        for node in self.node_list_ln:
            loads[node] = dict()
            loads[node][MACROPHAGE] = self.parameters[MACROPHAGES_PER_LYMPH]

        LungLymph.__init__(self, species, loads, positions, weight_method)

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
        self.total_fast_bac = self.total_slow_bac = self.total_fast_migrate = self.total_slow_migrate = \
            self.total_fast_o2 = self.total_slow_o2 = self.total_macrophage = self.total_mac_migrate = 0.0

    def update_totals(self):

        self.total_fast_bac = self.total_slow_bac = self.total_fast_migrate = self.total_slow_migrate = \
            self.total_fast_o2 = self.total_slow_o2 = self.total_macrophage = self.total_mac_migrate = 0.0
        for node in self.node_list_bps:
            bronchi_degree = self.get_neighbouring_edges(node, BRONCHUS)
            self.total_fast_bac += node.subpopulations[BACTERIA_FAST]
            self.total_slow_bac += node.subpopulations[BACTERIA_SLOW]
            self.total_fast_migrate += node.subpopulations[BACTERIA_FAST] * bronchi_degree
            self.total_slow_migrate += node.subpopulations[BACTERIA_SLOW] * bronchi_degree
            self.total_fast_o2 += node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
            self.total_slow_o2 += node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension
            self.total_macrophage += node.subpopulations[MACROPHAGE]
            lymph_degree = self.get_neighbouring_edges(node, LYMPHATIC_VESSEL)
            self.total_mac_migrate += node.subpopulations[MACROPHAGE] * lymph_degree

    def events(self):

        self.update_totals()
        events = []

        # Replicate
        events.append((self.parameters[P_REPLICATE_FAST] * self.total_fast_bac,
                       lambda f: self.replicate(BACTERIA_FAST)))
        events.append((self.parameters[P_REPLICATE_SLOW] * self.total_slow_bac,
                       lambda f: self.replicate(BACTERIA_SLOW)))

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
        events.append((self.parameters[P_DEATH_MACROPHAGE] * self.total_macrophage,
                       lambda f: self.macrophage_death()))

        # Macrophage migration
        events.append((self.parameters[P_MIGRATE_MACROPHAGE] * self.total_mac_migrate,
                       lambda f: self.macrophage_migrate()))

        return events

    def replicate(self, metabolism):

        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.total_fast_bac
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.total_slow_bac
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
                total_weight = sum(weight for _, weight in neighbouring_edges)
                r2 = np.random.random() * total_weight
                running_neighbour_weight_total = 0
                for (neighbour, weight) in neighbouring_edges:
                    running_neighbour_weight_total += weight
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
        node.update(MACROPHAGE, 1)

    def recruit_macrophage_lymph(self):
        index = np.random.randint(0, len(self.node_list_ln))
        node = self.node_list_ln[index]
        node.update(MACROPHAGE, 1)

    def macrophage_death(self):
        r = np.random.random() * self.total_macrophage
        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[MACROPHAGE]
            if running_total > r:
                node.update(MACROPHAGE, -1)
                return

    def macrophage_migrate(self):
        r = np.random.random() * self.total_mac_migrate
        running_total = 0
        for node in self.node_list.values():
            neighbouring_lymph_edges = self.get_neighbouring_edges(node, LYMPHATIC_VESSEL)
            running_total += node.subpopulations[MACROPHAGE] * len(neighbouring_lymph_edges)
            if running_total > r:
                neighbour_index = np.random.randint(0, len(neighbouring_lymph_edges))
                neighbour = neighbouring_lymph_edges[neighbour_index]
                node.update(MACROPHAGE, -1)
                neighbour.update(MACROPHAGE, 1)
                return
