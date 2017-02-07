import unittest

from v5_Spatial_heterogeneity.Models.SimpleMultiAgentTB_2 import *


class SimpleMultiAgent_v2_TestCase(unittest.TestCase):

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

        self.mac_per_patch = 10
        self.initial_fast_bac = 3
        self.initial_slow_bac = 2

        np.random.seed(101)

        self.network = TBSimpleMultiAgentMetapopulationNetwork_v2(self.rates, self.mac_per_patch, self.initial_fast_bac,
                                                                  self.initial_slow_bac)
        self.network.update_totals()

    def test_initialise(self):
        self.assertItemsEqual(self.network.rates.keys(), [P_REPLICATE_FAST, P_REPLICATE_SLOW, P_MIGRATE_FAST,
                                                          P_MIGRATE_SLOW, P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                                                          P_RECRUIT, P_DEATH, P_INGEST_FAST, P_INGEST_SLOW])

        for key in self.rates:
            self.assertEqual(self.rates[key], self.network.rates[key])

        # Macrophages
        for id in self.network.node_list:
            node = self.network.node_list[id]
            self.assertEqual(node.subpopulations[MACROPHAGE], self.mac_per_patch)

        # Bacteria (expected f: 25, 26, 32, s: 34, 26)
        self.assertEqual(self.network.node_list[26].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[19].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[23].subpopulations[SLOW], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[SLOW], 1)


    def test_update_totals(self):
        self.network.update_totals()

        self.assertEqual(self.network.total_f, self.initial_fast_bac)
        self.assertEqual(self.network.total_s, self.initial_slow_bac)
        self.assertEqual(self.network.total_mac, 36 * self.mac_per_patch)
        self.assertEqual(self.network.total_f_degree, 3*1)
        self.assertEqual(self.network.total_s_degree, 2*1)
        self.assertEqual(self.network.total_mac_fast, 1*self.mac_per_patch + 1*self.mac_per_patch + 1*self.mac_per_patch)
        self.assertEqual(self.network.total_mac_slow, 1*self.mac_per_patch + 1*self.mac_per_patch)
        # TODO - based on simplistic V/Q
        self.assertEqual(self.network.total_f_o2, 3.0)
        self.assertEqual(self.network.total_s_o2, 2.0)

    def test_events(self):
        events = self.network.events()

        self.assertEqual(events[0][0], self.initial_fast_bac * 0.01)
        self.assertEqual(events[1][0], self.initial_slow_bac * 0.02)

        # TODO - based on simplistic V/Q
        self.assertEqual(events[2][0], 3.0 * 0.03)
        self.assertEqual(events[3][0], 2.0 * 0.04)

        self.assertEqual(events[4][0], (1*1 + 1*1 + 1*1) * 0.05)
        self.assertEqual(events[5][0], (1*1 + 1*1) * 0.06)
        self.assertEqual(events[6][0], 36 * 0.07)
        self.assertEqual(events[7][0], (36 * self.mac_per_patch) * 0.08)
        self.assertEqual(events[8][0], (1 * self.mac_per_patch + 1 * self.mac_per_patch + 1 * self.mac_per_patch) * 0.09)
        self.assertEqual(events[9][0], (1 * self.mac_per_patch + 1 * self.mac_per_patch) * 0.10)

    def test_replicate_fast(self):

        self.network.replicate(FAST)
        # Patch 26
        self.assertEqual(self.network.node_list[27].subpopulations[FAST], 2)
        self.assertEqual(self.network.node_list[27].subpopulations[SLOW], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE], self.mac_per_patch)

    def test_replicate_slow(self):

        self.network.replicate(SLOW)
        # Patch 27
        self.assertEqual(self.network.node_list[27].subpopulations[SLOW], 2)
        self.assertEqual(self.network.node_list[27].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE], self.mac_per_patch)

    def test_ingest_fast(self):
        np.random.seed(101)
        self.network.ingest(FAST)
        self.assertEqual(self.network.node_list[26].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE], self.mac_per_patch)

    def test_ingest_slow(self):
        np.random.seed(101)
        self.network.ingest(SLOW)
        self.assertEqual(self.network.node_list[27].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE], self.mac_per_patch)

    def test_recruit(self):
        np.random.seed(101)
        self.network.recruit_mac()
        # Patch 31
        self.assertEqual(self.network.node_list[31].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[31].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[31].subpopulations[MACROPHAGE], self.mac_per_patch+1)

    def test_death(self):
        np.random.seed(101)
        self.network.death_mac()
        # Patch 9
        self.assertEqual(self.network.node_list[18].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[18].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[18].subpopulations[MACROPHAGE], self.mac_per_patch-1)

    def test_migrate_fast(self):
        np.random.seed(101)
        self.network.migrate(FAST)
        # Patch 3 to patch 2
        self.assertEqual(self.network.node_list[26].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE], self.mac_per_patch)
        self.assertEqual(self.network.node_list[11].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[11].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[MACROPHAGE], self.mac_per_patch)

    def test_migrate_slow(self):
        np.random.seed(101)
        self.network.migrate(SLOW)
        # Patch 5 to patch 2
        self.assertEqual(self.network.node_list[27].subpopulations[FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE], self.mac_per_patch)
        self.assertEqual(self.network.node_list[11].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[SLOW], 1)
        self.assertEqual(self.network.node_list[11].subpopulations[MACROPHAGE], self.mac_per_patch)

    def test_change_fast_to_slow(self):
        np.random.seed(101)
        self.network.change(SLOW)
        self.assertEqual(self.network.node_list[26].subpopulations[FAST], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[SLOW], 1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE], self.mac_per_patch)

    def test_change_slow_to_fast(self):
        np.random.seed(101)
        self.network.change(FAST)
        self.assertEqual(self.network.node_list[27].subpopulations[FAST], 2)
        self.assertEqual(self.network.node_list[27].subpopulations[SLOW], 0)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE], self.mac_per_patch)

if __name__ == '__main__':
    unittest.main()
