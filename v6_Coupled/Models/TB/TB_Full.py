from ..Lung.LungLymphNetwork import *

__author__ = "Michael J. Pitcher"

BACTERIA_FAST = 'B_f'
BACTERIA_SLOW = 'B_s'
BACTERIA_INTRACELLULAR = 'B_i'
MACROPHAGE_REGULAR = 'M_r'
MACROPHAGE_INFECTED = 'M_i'
T_CELL = 'T'

TOTAL_BACTERIA_FAST = 'total_B_f'
TOTAL_BACTERIA_SLOW = 'total_B_s'
TOTAL_BACTERIA_INTRACELLULAR = 'total_B_i'
TOTAL_BACTERIA_FAST_BY_O2 = 'total_B_f_by_O2'
TOTAL_BACTERIA_SLOW_BY_O2 = 'total_B_s_by_O2'
TOTAL_BACTERIA_FAST_BY_BRONCHUS_DEGREE = 'total_B_f_by_bronchus_degree'
TOTAL_BACTERIA_SLOW_BY_BRONCHUS_DEGREE = 'total_B_s_by_bronchus_degree'
TOTAL_BACTERIA_FAST_BY_LYMPH_DEGREE = 'total_B_f_by_lymph_degree'
TOTAL_BACTERIA_SLOW_BY_LYMPH_DEGREE = 'total_B_s_by_lymph_degree'

P_REPLICATION_BACTERIA_FAST = 'p_replication_B_f'
P_REPLICATION_BACTERIA_SLOW = 'p_replication_B_s'
P_REPLICATION_BACTERIA_INTRACELLULAR = 'p_replication_B_i'
P_CHANGE_BACTERIA_FAST_TO_SLOW = 'p_change_B_f_to_B_s'
P_CHANGE_BACTERIA_SLOW_TO_FAST = 'p_change_B_s_to_B_f'
P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST = 'p_translocate_bronchus_B_f'
P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW = 'p_translocate_bronchus_B_s'
P_TRANSLOCATE_LYMPH_BACTERIA_FAST = 'p_translocate_bronchus_B_f'
P_TRANSLOCATE_LYMPH_BACTERIA_SLOW = 'p_translocate_bronchus_B_s'
P_RECRUITMENT_BPS_MACROPHAGE = 'p_recruit_bps_M_r'
P_RECRUITMENT_LYMPH_MACROPHAGE = 'p_recruit_lymph_M_r'


class TBMetapopulationModel(LungLymphNetwork):

    def __init__(self, positions, parameters, loads, weight_method=HORSFIELD):

        # TODO - shouldn't be called species, find a better name which doesn't have connotations RE bacteria
        species = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR,
                   MACROPHAGE_REGULAR, MACROPHAGE_INFECTED,
                   T_CELL]

        expected_parameters = [P_REPLICATION_BACTERIA_FAST, P_REPLICATION_BACTERIA_SLOW,
                               P_REPLICATION_BACTERIA_INTRACELLULAR, P_CHANGE_BACTERIA_FAST_TO_SLOW,
                               P_CHANGE_BACTERIA_SLOW_TO_FAST, P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST,
                               P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW, P_TRANSLOCATE_LYMPH_BACTERIA_FAST,
                               P_TRANSLOCATE_LYMPH_BACTERIA_SLOW, P_RECRUITMENT_BPS_MACROPHAGE,
                               P_RECRUITMENT_LYMPH_MACROPHAGE]

        for expected_parameter in expected_parameters:
            assert expected_parameter in parameters, "Parameter {0} missing".format(expected_parameter)

        self.parameters = parameters

        LungLymphNetwork.__init__(self, species, loads, positions, weight_method=weight_method)

        # Set totals
        self.totals = dict()

    def reset_totals(self):
        """
        Reset all total counts to zero
        :return:
        """
        totals_needed = [TOTAL_BACTERIA_FAST, TOTAL_BACTERIA_SLOW, TOTAL_BACTERIA_INTRACELLULAR,
                         TOTAL_BACTERIA_FAST_BY_O2, TOTAL_BACTERIA_SLOW_BY_O2, TOTAL_BACTERIA_FAST_BY_BRONCHUS_DEGREE,
                         TOTAL_BACTERIA_SLOW_BY_BRONCHUS_DEGREE, TOTAL_BACTERIA_FAST_BY_LYMPH_DEGREE,
                         TOTAL_BACTERIA_SLOW_BY_LYMPH_DEGREE]
        for t in totals_needed:
            self.totals[t] = 0.0

    def update_totals(self):
        """
        Update all the total counts to reflect current state of the network
        :return:
        """

        self.reset_totals()
        # Loop through all BPS nodes
        for node in self.node_list_bps:
            lymph_degree = self.get_neighbouring_edges(node, LYMPHATIC_VESSEL)
            bronchus_degree = self.get_neighbouring_edges(node, BRONCHUS)

            self.totals[TOTAL_BACTERIA_FAST] += node.subpopulations[BACTERIA_FAST]
            self.totals[TOTAL_BACTERIA_SLOW] += node.subpopulations[BACTERIA_SLOW]
            self.totals[TOTAL_BACTERIA_INTRACELLULAR] += node.subpopulations[BACTERIA_INTRACELLULAR]
            self.totals[TOTAL_BACTERIA_FAST_BY_O2] += node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
            self.totals[TOTAL_BACTERIA_SLOW_BY_O2] += node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension
            self.totals[TOTAL_BACTERIA_FAST_BY_BRONCHUS_DEGREE] += node.subpopulations[BACTERIA_FAST] * bronchus_degree
            self.totals[TOTAL_BACTERIA_SLOW_BY_BRONCHUS_DEGREE] += node.subpopulations[BACTERIA_SLOW] * bronchus_degree
            self.totals[TOTAL_BACTERIA_FAST_BY_LYMPH_DEGREE] += node.subpopulations[BACTERIA_FAST] * lymph_degree
            self.totals[TOTAL_BACTERIA_SLOW_BY_LYMPH_DEGREE] += node.subpopulations[BACTERIA_SLOW] * lymph_degree

        # Loop through all lymph nodes
        for node in self.node_list_ln:
            lymph_degree = self.get_neighbouring_edges(node, LYMPHATIC_VESSEL)

            self.totals[TOTAL_BACTERIA_FAST] += node.subpopulations[BACTERIA_FAST]
            self.totals[TOTAL_BACTERIA_SLOW] += node.subpopulations[BACTERIA_SLOW]
            self.totals[TOTAL_BACTERIA_INTRACELLULAR] += node.subpopulations[BACTERIA_INTRACELLULAR]
            self.totals[TOTAL_BACTERIA_FAST_BY_LYMPH_DEGREE] += node.subpopulations[BACTERIA_FAST] * lymph_degree
            self.totals[TOTAL_BACTERIA_SLOW_BY_LYMPH_DEGREE] += node.subpopulations[BACTERIA_SLOW] * lymph_degree

    def events(self):
        """
        List of events and rates.
        Each item in list is a tuple of (rate, event), where rate = prob * count, event = lambda function of event
        :return:
        """
        events = []

        # Replication events
        events.append((self.parameters[P_REPLICATION_BACTERIA_FAST] * self.totals[TOTAL_BACTERIA_FAST],
                       lambda f: self.replicate_bacterium(BACTERIA_FAST)))
        events.append((self.parameters[P_REPLICATION_BACTERIA_SLOW] * self.totals[TOTAL_BACTERIA_SLOW],
                       lambda f: self.replicate_bacterium(BACTERIA_SLOW)))
        events.append((self.parameters[P_REPLICATION_BACTERIA_INTRACELLULAR] * self.totals[TOTAL_BACTERIA_INTRACELLULAR]
                       , lambda f: self.replicate_bacterium(BACTERIA_INTRACELLULAR)))

        # Bacteria change metabolism events
        events.append((self.parameters[P_CHANGE_BACTERIA_FAST_TO_SLOW] * self.totals[TOTAL_BACTERIA_FAST_BY_O2],
                       lambda f: self.change_metabolism_bacterium(BACTERIA_FAST)))
        events.append((self.parameters[P_CHANGE_BACTERIA_SLOW_TO_FAST] * self.totals[TOTAL_BACTERIA_SLOW_BY_O2],
                       lambda f: self.change_metabolism_bacterium(BACTERIA_SLOW)))

        # Bacteria translocate along bronchi
        events.append((self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST] * self.totals[TOTAL_BACTERIA_FAST_BY_BRONCHUS_DEGREE],
                       lambda f: self.translocate_bronchi_bacterium(BACTERIA_FAST)))
        events.append((self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW] * self.totals[TOTAL_BACTERIA_SLOW_BY_BRONCHUS_DEGREE],
                       lambda f: self.translocate_bronchi_bacterium(BACTERIA_SLOW)))

        # Bacteria translocate along lymphatic vessel
        events.append((self.parameters[P_TRANSLOCATE_LYMPH_BACTERIA_FAST] * self.totals[TOTAL_BACTERIA_FAST_BY_LYMPH_DEGREE],
                       lambda f: self.translocate_lymph_bacterium(BACTERIA_FAST)))
        events.append((self.parameters[P_TRANSLOCATE_LYMPH_BACTERIA_SLOW] * self.totals[TOTAL_BACTERIA_SLOW_BY_LYMPH_DEGREE],
                       lambda f: self.translocate_lymph_bacterium(BACTERIA_SLOW)))

        # Macrophage recruited into BPS
        events.append((self.parameters[P_RECRUITMENT_BPS_MACROPHAGE] * len(self.node_list_bps),
                       lambda f: self.recruit_bps_macrophage()))
        # Macrophage recruited into BPS
        events.append((self.parameters[P_RECRUITMENT_LYMPH_MACROPHAGE] * len(self.node_list_ln),
                       lambda f: self.recruit_lymph_macrophage()))

        return events

    def replicate_bacterium(self, metabolism):
        """
        A bacterium replicates, creating an identical member of the same metabolism
        :param metabolism: Fast, slow or intracellular bacterium
        :return:
        """

        # Choose random threshold based on relevant counts
        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_FAST]
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_SLOW]
        elif metabolism == BACTERIA_INTRACELLULAR:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_INTRACELLULAR]
        else:
            raise Exception("Incorrect metabolism specified: {0}".format(metabolism))

        # Count up members of subpopulations until threshold exceeded
        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulations[metabolism]
            if running_total > r:
                # Create a new bacterium of the same metabolism
                node.update(metabolism, 1)
                return

    def change_metabolism_bacterium(self, old_metabolism):
        """
        A bacterium changes metabolism, changing from Fast to Slow (or vice versa), based on oxygen availability
        :param old_metabolism: The old metabolism to change from
        :return:
        """

        # Choose random threshold based on relevant counts
        if old_metabolism == BACTERIA_FAST:
            new_metabolism = BACTERIA_SLOW
            r = np.random.random() * self.totals[TOTAL_BACTERIA_FAST_BY_O2]
        elif old_metabolism == BACTERIA_SLOW:
            new_metabolism = BACTERIA_FAST
            r = np.random.random() * self.totals[TOTAL_BACTERIA_SLOW_BY_O2]
        else:
            raise Exception("Incorrect metabolism specified: {0}".format(old_metabolism))

        # Count up members of subpopulations until threshold exceeded
        running_total = 0
        for node in self.node_list.values():
            if old_metabolism == BACTERIA_SLOW:
                running_total += node.subpopulations[BACTERIA_SLOW] * node.oxygen_tension
            else:
                running_total += node.subpopulations[BACTERIA_FAST] * (1/node.oxygen_tension)
            if running_total > r:
                # Switch a bacteria from old to new metabolism
                node.update(new_metabolism, 1)
                node.update(old_metabolism, -1)
                return

    def translocate_bronchi_bacterium(self, metabolism):
        """
        A bacterium moves from on BPS node to another bronchial-adjacent node
        :param metabolism: State of bacteria that is moving
        :return:
        """
        # Choose random threshold based on relevant counts
        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_FAST_BY_BRONCHUS_DEGREE]
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_SLOW_BY_BRONCHUS_DEGREE]
        else:
            raise Exception("Incorrect metabolism specified: {0}".format(metabolism))

        # Count up members of subpopulations until threshold exceeded
        running_total = 0
        for node in self.node_list.values():
            bronchial_neighbours = self.get_neighbouring_edges(node, BRONCHUS)
            running_total += node.subpopulations[metabolism] * len(bronchial_neighbours)
            # Node has been chosen to lose a bacterium
            if running_total > r:
                # Pick a neighbour based on edge weight
                total_weight = [sum(data[WEIGHT] for _,data in bronchial_neighbours)]
                r2 = np.random.random() * total_weight
                running_total_weight = 0
                for (neighbour, data) in bronchial_neighbours:
                    running_total_weight += data[WEIGHT]
                    if running_total_weight > r2:
                        # Move a bacterium from node to neighbour
                        neighbour.update(metabolism, 1)
                        node.update(metabolism, -1)
                        return

    def translocate_lymph_bacterium(self, metabolism):
        """
        A bacterium moves from one node to another, along a lymphatic vessel
        :param metabolism:
        :return:
        """

        # Choose random threshold based on relevant counts
        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_FAST_BY_LYMPH_DEGREE]
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_SLOW_BY_LYMPH_DEGREE]
        else:
            raise Exception("Incorrect metabolism specified: {0}".format(metabolism))

        # Count up members of subpopulations until threshold exceeded
        running_total = 0
        for node in self.node_list.values():
            lymph_neighbours = self.get_neighbouring_edges(node, LYMPHATIC_VESSEL)
            running_total += node.subpopulations[metabolism] * len(lymph_neighbours)
            # Node has been chosen to lose a bacterium
            if running_total > r:
                # Pick a neighbour
                r2 = np.random.randint(0, len(lymph_neighbours))
                (neighbour, data) = lymph_neighbours[r2]
                neighbour.update(metabolism, 1)
                node.update(metabolism, -1)
                return

    def recruit_bps_macrophage(self):
        """
        A macrophage is recruited into the bronchopulmonary segment
        :return:
        """
        r = np.random.randint(0, len(self.node_list_bps))
        node = self.node_list_bps[r]
        node.update(MACROPHAGE_REGULAR, 1)
        return

    def recruit_lymph_macrophage(self):
        """
        A macrophage is recruited into a lymph node
        :return:
        """
        r = np.random.randint(0, len(self.node_list_ln))
        node = self.node_list_ln[r]
        node.update(MACROPHAGE_REGULAR, 1)
        return