import unittest

from v5_Spatial_heterogeneity.Models.SimpleMultiAgentTB import *


class SimpleMultiAgentTestCase(unittest.TestCase):

    def setUp(self):

        self.rates = dict()
        self.rates[P_REPLICATE_FAST] = 0.01
        self.rates[P_REPLICATE_SLOW] = 0.02
        self.rates[P_CHANGE_FAST_SLOW] = 0.03
        self.rates[P_CHANGE_SLOW_FAST] = 0.04
        self.rates[P_MIGRATE_FAST] = 0.05
        self.rates[P_MIGRATE_SLOW] = 0.06
        self.rates[P_RECRUIT] = 0.07
        self.rates[P_DEATH] = 0.08
        self.rates[P_INGEST_FAST] = 0.09
        self.rates[P_INGEST_SLOW] = 0.10

        self.loads = dict()
        self.loads[0] = dict()
        self.loads[3] = dict()
        self.loads[5] = dict()
        self.loads[7] = dict()
        self.loads[9] = dict()
        self.loads[13] = dict()

        self.loads[0][FAST] = 11
        self.loads[3][FAST] = 10
        self.loads[5][SLOW] = 4
        self.loads[7][SLOW] = 3
        self.loads[9][MACROPHAGE] = 13
        self.loads[3][MACROPHAGE] = 1
        self.loads[7][MACROPHAGE] = 2

        self.network = TBSimpleMultiAgentMetapopulationNetwork(self.rates, self.loads)
        self.network.update_totals()

    def test_initialise(self):
        self.assertItemsEqual(self.network.rates.keys(), [P_REPLICATE_FAST, P_REPLICATE_SLOW, P_MIGRATE_FAST,
                                                          P_MIGRATE_SLOW, P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                                                          P_RECRUIT, P_DEATH, P_INGEST_FAST, P_INGEST_SLOW])

        for key in self.rates:
            self.assertEqual(self.rates[key], self.network.rates[key])

    def test_update_totals(self):
        self.network.update_totals()

        self.assertEqual(self.network.total_f, 21)
        self.assertEqual(self.network.total_s, 7)
        self.assertEqual(self.network.total_mac, 13+1+2)
        self.assertEqual(self.network.total_f_degree, 11 * 1 + 10 * 3)
        self.assertEqual(self.network.total_s_degree, 4 * 3 + 3 * 3)
        self.assertEqual(self.network.total_mac_fast, 1*10)
        self.assertEqual(self.network.total_mac_slow, 2*3)
        # TODO - based on simplistic V/Q
        self.assertEqual(self.network.total_f_o2, 21)
        self.assertEqual(self.network.total_s_o2, 7)

    def test_events(self):
        events = self.network.events()

        self.assertEqual(events[0][0], 21 * 0.01)
        self.assertEqual(events[1][0], 7 * 0.02)

        # TODO - based on simplistic V/Q
        self.assertEqual(events[2][0], 21 * 0.03)
        self.assertEqual(events[3][0], 7 * 0.04)

        self.assertEqual(events[4][0], (11 * 1 + 10 * 3) * 0.05)
        self.assertEqual(events[5][0], (4 * 3 + 3 * 3) * 0.06)
        self.assertEqual(events[6][0], 36 * 0.07)
        self.assertEqual(events[7][0], (13+1+2) * 0.08)
        self.assertEqual(events[8][0], (1 * 10) * 0.09)
        self.assertEqual(events[9][0], (2 * 3) * 0.10)

    def test_replicate_fast(self):
        np.random.seed(101)

        self.network.replicate(FAST)
        # Patch 0
        self.assertEqual(self.network.node_list[0].subpopulations[FAST], 12)
        self.assertEqual(self.network.node_list[0].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE], 0)

    def test_replicate_slow(self):
        np.random.seed(101)

        self.network.replicate(SLOW)
        # Patch 5
        self.assertEqual(self.network.node_list[5].subpopulations[SLOW], 5)
        self.assertEqual(self.network.node_list[5].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[5].subpopulations[MACROPHAGE], 0)

    def test_ingest_fast(self):
        np.random.seed(101)
        self.network.ingest(FAST)
        self.assertEqual(self.network.node_list[3].subpopulations[FAST], 9)
        self.assertEqual(self.network.node_list[3].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[3].subpopulations[MACROPHAGE], 1)

    def test_ingest_slow(self):
        np.random.seed(101)
        self.network.ingest(SLOW)
        self.assertEqual(self.network.node_list[7].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[7].subpopulations[SLOW], 2)
        self.assertEqual(self.network.node_list[7].subpopulations[MACROPHAGE], 2)

    def test_recruit(self):
        np.random.seed(101)
        self.network.recruit_mac()
        # Patch 31
        self.assertEqual(self.network.node_list[31].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[31].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[31].subpopulations[MACROPHAGE], 1)

    def test_death(self):
        np.random.seed(101)
        self.network.death_mac()
        # Patch 9
        self.assertEqual(self.network.node_list[9].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[9].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[9].subpopulations[MACROPHAGE], 12)

    def test_migrate_fast(self):
        np.random.seed(101)
        self.network.migrate(FAST)
        # Patch 3 to patch 2
        self.assertEqual(self.network.node_list[3].subpopulations[FAST], 9)
        self.assertEqual(self.network.node_list[3].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[3].subpopulations[MACROPHAGE], 1)
        self.assertEqual(self.network.node_list[7].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[7].subpopulations[SLOW], 3)
        self.assertEqual(self.network.node_list[7].subpopulations[MACROPHAGE], 2)

    def test_migrate_slow(self):
        np.random.seed(101)
        self.network.migrate(SLOW)
        # Patch 5 to patch 2
        self.assertEqual(self.network.node_list[5].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[5].subpopulations[SLOW], 3)
        self.assertEqual(self.network.node_list[5].subpopulations[MACROPHAGE], 0)
        self.assertEqual(self.network.node_list[6].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[6].subpopulations[SLOW], 1)
        self.assertEqual(self.network.node_list[6].subpopulations[MACROPHAGE], 0)

    def test_change_fast_to_slow(self):
        np.random.seed(101)
        self.network.change(SLOW)
        self.assertEqual(self.network.node_list[0].subpopulations[FAST], 10)
        self.assertEqual(self.network.node_list[0].subpopulations[SLOW], 1)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE], 0)

    def test_change_slow_to_fast(self):
        np.random.seed(101)
        self.network.change(FAST)
        self.assertEqual(self.network.node_list[5].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[5].subpopulations[SLOW], 3)
        self.assertEqual(self.network.node_list[5].subpopulations[MACROPHAGE], 0)

if __name__ == '__main__':
    unittest.main()
