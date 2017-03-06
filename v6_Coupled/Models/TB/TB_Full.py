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

        # TODO - don't call species
        species = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR,
                   MACROPHAGE_REGULAR, MACROPHAGE_INFECTED,
                   T_CELL]

        expected_parameters = []

        for expected_parameter in expected_parameters:
            assert expected_parameter in parameters, "Parameter {0} missing".format(expected_parameter)

        self.parameters = parameters

        LungLymphNetwork.__init__(self, species, loads, positions, weight_method=HORSFIELD)

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

    def events(self):
        pass

    def bacteria_replication(self, metabolism):

        if metabolism == BACTERIA_FAST:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_FAST]
        elif metabolism == BACTERIA_SLOW:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_SLOW]
        elif metabolism == BACTERIA_INTRACELLULAR:
            r = np.random.random() * self.totals[TOTAL_BACTERIA_INTRACELLULAR]
        else:
            raise Exception("Incorrect metabolism specified: {0}".format(metabolism))

        running_total = 0
        for node in self.node_list.values():
            running_total += node.subpopulation[metabolism]
            if running_total > r:
                node.update(metabolism, 1)
                return

