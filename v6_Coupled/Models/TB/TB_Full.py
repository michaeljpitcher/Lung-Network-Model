from ..Lung.LungLymphNetwork import *

__author__ = "Michael J. Pitcher"

BACTERIA_FAST = 'B_f'
BACTERIA_SLOW = 'B_s'
BACTERIA_INTRACELLULAR = 'B_i'
MACROPHAGE_REGULAR = 'M_r'
MACROPHAGE_INFECTED = 'M_i'
T_CELL = 'T'

TOTAL_BACTERIA_FAST = 'total_b_f'
TOTAL_BACTERIA_SLOW = 'total_b_s'
TOTAL_BACTERIA_INTRACELLULAR = 'total_b_i'

P_REPLICATION_BACTERIA_FAST = 'p_replication_B_f'
P_REPLICATION_BACTERIA_SLOW = 'p_replication_B_s'
P_REPLICATION_BACTERIA_INTRACELLULAR = 'p_replication_B_i'


class TBMetapopulationModel(LungLymphNetwork):

    def __init__(self, positions, parameters, loads, weight_method=HORSFIELD):

        # TODO - shouldn't be called species, find a better name which doesn't have connotations RE bacteria
        species = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR,
                   MACROPHAGE_REGULAR, MACROPHAGE_INFECTED,
                   T_CELL]

        expected_parameters = [P_REPLICATION_BACTERIA_FAST, P_REPLICATION_BACTERIA_SLOW,
                               P_REPLICATION_BACTERIA_INTRACELLULAR]

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
        totals_needed = [TOTAL_BACTERIA_FAST, TOTAL_BACTERIA_SLOW, TOTAL_BACTERIA_INTRACELLULAR]
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
            self.totals[TOTAL_BACTERIA_FAST] += node.subpopulations[BACTERIA_FAST]
            self.totals[TOTAL_BACTERIA_SLOW] += node.subpopulations[BACTERIA_SLOW]
            self.totals[TOTAL_BACTERIA_INTRACELLULAR] += node.subpopulations[BACTERIA_INTRACELLULAR]
        # Loop through all lymph nodes
        for node in self.node_list_ln:
            self.totals[TOTAL_BACTERIA_FAST] += node.subpopulations[BACTERIA_FAST]
            self.totals[TOTAL_BACTERIA_SLOW] += node.subpopulations[BACTERIA_SLOW]
            self.totals[TOTAL_BACTERIA_INTRACELLULAR] += node.subpopulations[BACTERIA_INTRACELLULAR]

    def events(self):
        """
        List of events and rates.
        Each item in list is a tuple of (rate, event), where rate = prob * count, event = lambda function of event
        :return:
        """
        events = []

        # Replication events
        events.append((self.parameters[P_REPLICATION_BACTERIA_FAST] * self.totals[TOTAL_BACTERIA_FAST],
                       lambda f: self.bacteria_replication(BACTERIA_FAST)))
        events.append((self.parameters[P_REPLICATION_BACTERIA_SLOW] * self.totals[TOTAL_BACTERIA_SLOW],
                       lambda f: self.bacteria_replication(BACTERIA_SLOW)))
        events.append((self.parameters[P_REPLICATION_BACTERIA_INTRACELLULAR] * self.totals[TOTAL_BACTERIA_INTRACELLULAR]
                       , lambda f: self.bacteria_replication(BACTERIA_INTRACELLULAR)))

        return events

    def bacteria_replication(self, metabolism):
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

