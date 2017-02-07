import unittest

import numpy as np

from v5_Spatial_heterogeneity.Models.TBFastAndSlow import *


class TBFastAndSlowTestCase(unittest.TestCase):

    def setUp(self):

        self.rates = dict()
        self.rates[P_MIGRATE_F] = 0.1
        self.rates[P_MIGRATE_S] = 0.2
        self.rates[P_CHANGE_F_TO_S] = 0.3
        self.rates[P_CHANGE_S_TO_F] = 0.4
        self.rates[P_GROWTH_F] = 0.5
        self.rates[P_GROWTH_S] = 0.6

        self.loads_fast = dict()
        self.loads_fast[1] = 10

        self.loads_slow = dict()
        self.loads_slow[13] = 3

        self.network = TBFastSlowMetapopulationNetwork(self.rates, self.loads_fast, self.loads_slow)

    def test_initialise(self):
        self.assertItemsEqual(self.network.rates.keys(), [P_MIGRATE_F, P_MIGRATE_S, P_CHANGE_F_TO_S, P_CHANGE_S_TO_F,
                                                          P_GROWTH_S, P_GROWTH_F])

        for a in [P_MIGRATE_F, P_MIGRATE_S, P_CHANGE_F_TO_S, P_CHANGE_S_TO_F, P_GROWTH_S, P_GROWTH_F]:
            self.assertEqual(self.network.rates[a], self.rates[a])

        for a in self.loads_fast:
            self.assertEqual(self.network.node_list[a].subpopulations[FAST], self.loads_fast[a])
        for a in self.loads_slow:
            self.assertEqual(self.network.node_list[a].subpopulations[SLOW], self.loads_slow[a])

        self.assertEqual(self.network.total_migrate_f, 0.0)
        self.assertEqual(self.network.total_migrate_s, 0.0)
        self.assertEqual(self.network.total_f, 0.0)
        self.assertEqual(self.network.total_s, 0.0)
        self.assertEqual(self.network.total_f_O2, 0.0)
        self.assertEqual(self.network.total_s_O2, 0.0)

    def test_update_totals(self):

        self.network.update_totals()
        self.assertEqual(self.network.total_migrate_f, 10*3)
        self.assertEqual(self.network.total_migrate_s, 3*3)
        self.assertEqual(self.network.total_f, 10)
        self.assertEqual(self.network.total_s, 3)
        # TODO - based on simplistic V/Q
        self.assertEqual(self.network.total_f_O2, 10)
        self.assertEqual(self.network.total_s_O2, 3.0)

    def test_events(self):

        events = self.network.events()

        self.assertEqual(events[0][0], 10 * 3 * 0.1)
        self.assertEqual(events[1][0], 3 * 3 * 0.2)
        self.assertEqual(events[2][0], 10 * 0.5)
        self.assertEqual(events[3][0], 3 * 0.6)
        self.assertEqual(events[4][0], 10 * 0.3)
        self.assertEqual(events[5][0], 3 * 0.4)

    def test_migrate_F(self):
        np.random.seed(101)
        self.network.update_totals()
        self.network.migrate(FAST)
        self.assertEqual(self.network.node_list[1].subpopulations[FAST], 9)
        self.assertEqual(self.network.node_list[2].subpopulations[FAST], 1)

    def test_migrate_S(self):
        np.random.seed(10111)
        self.network.update_totals()
        self.network.migrate(SLOW)
        self.assertEqual(self.network.node_list[13].subpopulations[SLOW], 2)
        self.assertEqual(self.network.node_list[12].subpopulations[SLOW], 1)

    def test_growth_F_pos(self):
        np.random.seed(101)
        self.network.update_totals()
        self.network.growth(FAST)
        self.assertEqual(self.network.node_list[1].subpopulations[FAST], 11)

    def test_growth_F_neg(self):
        np.random.seed(10111)
        self.network.rates[P_GROWTH_F] = -0.1
        self.network.update_totals()
        self.network.growth(FAST)
        self.assertEqual(self.network.node_list[1].subpopulations[FAST], 9)

    def test_growth_S_pos(self):
        np.random.seed(101)
        self.network.update_totals()
        self.network.growth(SLOW)
        self.assertEqual(self.network.node_list[13].subpopulations[SLOW], 4)

    def test_growth_S_neg(self):
        np.random.seed(23466)
        self.network.rates[P_GROWTH_S] = -0.1
        self.network.update_totals()
        self.network.growth(SLOW)
        self.assertEqual(self.network.node_list[13].subpopulations[SLOW], 2)

    def test_change_F_to_S(self):
        np.random.seed(101)
        self.network.update_totals()
        self.network.change(FAST,SLOW)
        self.assertEqual(self.network.node_list[1].subpopulations[FAST], 9)
        self.assertEqual(self.network.node_list[1].subpopulations[SLOW], 1)

    def test_change_S_to_F(self):
        np.random.seed(101)
        self.network.update_totals()
        self.network.change(SLOW,FAST)
        self.assertEqual(self.network.node_list[13].subpopulations[SLOW], 2)
        self.assertEqual(self.network.node_list[13].subpopulations[FAST], 1)






if __name__ == '__main__':
    unittest.main()
