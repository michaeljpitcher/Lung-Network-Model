import unittest
from ..Models.TB.TB_Full import *


class TBFullTestCase(unittest.TestCase):

    def setUp(self):
        self.positions = dict()
        for i in range(45):
            self.positions[i] = (5, 5)

        self.parameters = dict()
        self.parameters[P_REPLICATION_BACTERIA_FAST] = 0.0
        self.parameters[P_REPLICATION_BACTERIA_SLOW] = 0.0
        self.parameters[P_REPLICATION_BACTERIA_INTRACELLULAR] = 0.0

        self.loads = dict()

        np.random.seed(101)
        self.network = TBMetapopulationModel(self.positions, self.parameters, self.loads)

    def test_reset_totals(self):
        self.network.reset_totals()
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_FAST], 0)
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_SLOW], 0)
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_INTRACELLULAR], 0)

    def test_update_totals(self):
        self.network.update_totals()
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_FAST], 0)
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_SLOW], 0)
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_INTRACELLULAR], 0)

        self.network.node_list[0].update(BACTERIA_FAST, 1)
        self.network.node_list[1].update(BACTERIA_SLOW, 2)
        self.network.node_list[2].update(BACTERIA_INTRACELLULAR, 3)
        self.network.update_totals()

        self.assertEqual(self.network.totals[TOTAL_BACTERIA_FAST], 1)
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_SLOW], 2)
        self.assertEqual(self.network.totals[TOTAL_BACTERIA_INTRACELLULAR], 3)

    def test_bacteria_replication(self):
        self.network.node_list[0].update(BACTERIA_FAST, 10)
        self.network.node_list[1].update(BACTERIA_FAST, 20)
        self.network.update_totals()
        self.network.replicate_bacterium(BACTERIA_FAST)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_FAST], 10)
        self.assertEqual(self.network.node_list[1].subpopulations[BACTERIA_FAST], 21)

        self.network.node_list[2].update(BACTERIA_SLOW, 10)
        self.network.node_list[3].update(BACTERIA_SLOW, 20)
        self.network.update_totals()
        self.network.replicate_bacterium(BACTERIA_SLOW)
        self.assertEqual(self.network.node_list[2].subpopulations[BACTERIA_SLOW], 10)
        self.assertEqual(self.network.node_list[3].subpopulations[BACTERIA_SLOW], 21)

        self.network.node_list[4].update(BACTERIA_INTRACELLULAR, 10)
        self.network.node_list[5].update(BACTERIA_INTRACELLULAR, 20)
        self.network.update_totals()
        self.network.replicate_bacterium(BACTERIA_INTRACELLULAR)
        self.assertEqual(self.network.node_list[4].subpopulations[BACTERIA_INTRACELLULAR], 11)
        self.assertEqual(self.network.node_list[5].subpopulations[BACTERIA_INTRACELLULAR], 20)

if __name__ == '__main__':
    unittest.main()
