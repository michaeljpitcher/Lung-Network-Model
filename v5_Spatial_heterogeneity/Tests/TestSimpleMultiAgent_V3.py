import unittest

from v5_Spatial_heterogeneity.TB_Models.Old.SimpleMultiAgentTB_3 import *


class SimpleMultiAgent_v3_TestCase(unittest.TestCase):

    def setUp(self):

        self.rates = dict()
        self.rates[P_REPLICATE_FAST] = 0.01
        self.rates[P_REPLICATE_SLOW] = 0.02
        self.rates[P_CHANGE_FAST_SLOW] = 0.03
        self.rates[P_CHANGE_SLOW_FAST] = 0.04
        self.rates[P_MIGRATE_FAST] = 0.05
        self.rates[P_MIGRATE_SLOW] = 0.06
        self.rates[P_RECRUIT] = 0.07
        self.rates[P_DEATH_REGULAR] = 0.08
        self.rates[P_DEATH_INFECTED] = 0.09
        self.rates[P_REGULAR_INGEST_FAST] = 0.10
        self.rates[P_REGULAR_INGEST_SLOW] = 0.11
        self.rates[P_INFECTED_INGEST_FAST] = 0.12
        self.rates[P_INFECTED_INGEST_SLOW] = 0.13

        self.mac_per_patch = 10
        self.initial_fast_bac = 3
        self.initial_slow_bac = 2

        np.random.seed(101)

        self.network = TBSimpleMultiAgentMetapopulationNetwork_v3(self.rates, self.mac_per_patch, self.initial_fast_bac,
                                                                  self.initial_slow_bac)
        self.network.update_totals()

    def test_initialise(self):
        self.assertItemsEqual(self.network.rates.keys(), [P_REPLICATE_FAST, P_REPLICATE_SLOW, P_MIGRATE_FAST,
                                                          P_MIGRATE_SLOW, P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                                                          P_RECRUIT, P_DEATH_REGULAR, P_DEATH_INFECTED,
                                                          P_REGULAR_INGEST_FAST, P_REGULAR_INGEST_SLOW,
                                                          P_INFECTED_INGEST_FAST, P_INFECTED_INGEST_SLOW])

        for key in self.rates:
            self.assertEqual(self.rates[key], self.network.rates[key])

        # Macrophages
        for id in self.network.node_list:
            node = self.network.node_list[id]
            self.assertEqual(node.subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)

        # Bacteria (expected f: 25, 26, 32, s: 34, 26)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[19].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[23].subpopulations[BACTERIA_SLOW], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 1)

    def test_update_totals(self):
        # Put some infected macs in
        self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED] = 5
        self.network.node_list[23].subpopulations[MACROPHAGE_INFECTED] = 4
        self.network.node_list[13].subpopulations[MACROPHAGE_INFECTED] = 3
        self.network.update_totals()

        self.assertEqual(self.network.total_f, self.initial_fast_bac)
        self.assertEqual(self.network.total_s, self.initial_slow_bac)
        self.assertEqual(self.network.total_mac_regular, 36 * self.mac_per_patch)
        self.assertEqual(self.network.total_mac_infected, 5+4+3)
        self.assertEqual(self.network.total_f_degree, 3*1)
        self.assertEqual(self.network.total_s_degree, 2*1)
        self.assertEqual(self.network.total_regular_fast, 1*self.mac_per_patch + 1*self.mac_per_patch + 1*self.mac_per_patch)
        self.assertEqual(self.network.total_regular_slow, 1*self.mac_per_patch + 1*self.mac_per_patch)
        self.assertEqual(self.network.total_infected_fast, 5 * 1)
        self.assertEqual(self.network.total_infected_slow, 4 * 1)
        # TODO - based on simplistic V/Q
        self.assertEqual(self.network.total_f_o2, 3.0)
        self.assertEqual(self.network.total_s_o2, 2.0)

    def test_events(self):
        self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED] = 5
        self.network.node_list[23].subpopulations[MACROPHAGE_INFECTED] = 4
        self.network.node_list[13].subpopulations[MACROPHAGE_INFECTED] = 3
        events = self.network.events()

        # Replication
        self.assertEqual(events[0][0], self.initial_fast_bac * 0.01)
        self.assertEqual(events[1][0], self.initial_slow_bac * 0.02)

        # Metabolism change
        # TODO - based on simplistic V/Q
        self.assertEqual(events[2][0], 3.0 * 0.03)
        self.assertEqual(events[3][0], 2.0 * 0.04)

        # Migrate
        self.assertEqual(events[4][0], (1*1 + 1*1 + 1*1) * 0.05)
        self.assertEqual(events[5][0], (1*1 + 1*1) * 0.06)

        # Recruit
        self.assertEqual(events[6][0], 36 * 0.07)

        # Death
        self.assertEqual(events[7][0], (36 * self.mac_per_patch) * 0.08)
        self.assertEqual(events[8][0], (5+4+3) * 0.09)

        # Ingest
        self.assertEqual(events[9][0], (1 * self.mac_per_patch + 1 * self.mac_per_patch + 1 * self.mac_per_patch) * 0.10)
        self.assertEqual(events[10][0], (1 * self.mac_per_patch + 1 * self.mac_per_patch) * 0.11)
        self.assertEqual(events[11][0], (5 * 1) * 0.12)
        self.assertEqual(events[12][0], (4 * 1) * 0.13)

    def test_replicate_fast(self):

        self.network.replicate(BACTERIA_FAST)
        # Patch 26
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 2)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_replicate_slow(self):

        self.network.replicate(BACTERIA_SLOW)
        # Patch 27
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 2)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_regular_ingest_fast(self):
        np.random.seed(101)
        self.network.ingest(BACTERIA_FAST,MACROPHAGE_REGULAR)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch-1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 1)

    def test_regular_ingest_slow(self):
        np.random.seed(101)
        self.network.ingest(BACTERIA_SLOW,MACROPHAGE_REGULAR)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch-1)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_INFECTED], 1)

    def test_infected_ingest_fast(self):
        np.random.seed(101)
        self.network.update_node(self.network.node_list[26], MACROPHAGE_INFECTED, 13)
        self.network.update_totals()
        self.network.ingest(BACTERIA_FAST,MACROPHAGE_INFECTED)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 13)

    def test_infected_ingest_slow(self):
        np.random.seed(101)
        self.network.update_node(self.network.node_list[27], MACROPHAGE_INFECTED, 13)
        self.network.update_totals()
        self.network.ingest(BACTERIA_SLOW,MACROPHAGE_INFECTED)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_INFECTED], 13)

    def test_recruit(self):
        np.random.seed(101)
        self.network.recruit_mac()
        # Patch 31
        self.assertEqual(self.network.node_list[31].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[31].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[31].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch+1)
        self.assertEqual(self.network.node_list[31].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_death_regular(self):
        np.random.seed(101)
        self.network.death_mac(MACROPHAGE_REGULAR)
        self.assertEqual(self.network.node_list[18].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[18].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[18].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch-1)
        self.assertEqual(self.network.node_list[18].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_death_infected(self):
        np.random.seed(101)
        self.network.update_node(self.network.node_list[14],MACROPHAGE_INFECTED, 13)
        self.network.update_totals()
        self.network.death_mac(MACROPHAGE_INFECTED)
        self.assertEqual(self.network.node_list[14].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[14].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[14].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[14].subpopulations[MACROPHAGE_INFECTED], 12)

    def test_migrate_fast(self):
        np.random.seed(101)
        self.network.migrate(BACTERIA_FAST)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)

    def test_migrate_slow(self):
        np.random.seed(101)
        self.network.migrate(BACTERIA_SLOW)
        # Patch 5 to patch 2
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_SLOW], 1)
        self.assertEqual(self.network.node_list[11].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)

    def test_change_fast_to_slow(self):
        np.random.seed(101)
        self.network.change(BACTERIA_SLOW)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], 1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_change_slow_to_fast(self):
        np.random.seed(101)
        self.network.change(BACTERIA_FAST)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 2)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[27].subpopulations[MACROPHAGE_INFECTED], 0)

if __name__ == '__main__':
    unittest.main()
