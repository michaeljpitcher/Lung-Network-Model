import unittest

from v5_Spatial_heterogeneity.TB_Models.TB_FSIcRIn import *


class MultiAgentTestCase(unittest.TestCase):

    def setUp(self):

        self.rates = dict()
        self.rates[P_REPLICATE_FAST] = 0.01
        self.rates[P_REPLICATE_SLOW] = 0.02
        self.rates[P_REPLICATE_INTRACELLULAR] = 0.03
        self.rates[P_CHANGE_FAST_SLOW] = 0.04
        self.rates[P_CHANGE_SLOW_FAST] = 0.05
        self.rates[P_MIGRATE_FAST] = 0.06
        self.rates[P_MIGRATE_SLOW] = 0.07
        self.rates[P_RECRUIT] = 0.08
        self.rates[P_DEATH_REGULAR] = 0.09
        self.rates[P_DEATH_INFECTED] = 0.10
        self.rates[P_REGULAR_INGEST_FAST] = 0.11
        self.rates[P_REGULAR_INGEST_SLOW] = 0.12
        self.rates[P_INFECTED_INGEST_FAST] = 0.13
        self.rates[P_INFECTED_INGEST_SLOW] = 0.14

        self.mac_per_patch = 10
        self.initial_fast_bac = 3
        self.initial_slow_bac = 2

        np.random.seed(101)

        self.network = TBMetapopulationNetwork_FSIcRIn(self.rates, self.mac_per_patch, self.initial_fast_bac,
                                                       self.initial_slow_bac)
        self.network.update_totals()

    def test_initialise(self):
        self.assertItemsEqual(self.network.rates.keys(), [P_REPLICATE_FAST, P_REPLICATE_SLOW, P_REPLICATE_INTRACELLULAR,
                                                          P_MIGRATE_FAST, P_MIGRATE_SLOW,
                                                          P_CHANGE_FAST_SLOW, P_CHANGE_SLOW_FAST,
                                                          P_RECRUIT, P_DEATH_REGULAR, P_DEATH_INFECTED,
                                                          P_REGULAR_INGEST_FAST, P_REGULAR_INGEST_SLOW,
                                                          P_INFECTED_INGEST_FAST, P_INFECTED_INGEST_SLOW])

        for key in self.rates:
            self.assertEqual(self.rates[key], self.network.rates[key])

        # Macrophages
        for id in self.network.node_list:
            node = self.network.node_list[id]
            self.assertEqual(node.subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)

        # Bacteria (expected 26)

        for id in self.network.node_list:
            node = self.network.node_list[id]
            self.assertEqual(node.subpopulations[BACTERIA_INTRACELLULAR], 0)
            if id != 26:
                self.assertEqual(node.subpopulations[BACTERIA_FAST], 0)
                self.assertEqual(node.subpopulations[BACTERIA_SLOW], 0)
            else:
                self.assertEqual(node.subpopulations[BACTERIA_FAST], self.initial_fast_bac)
                self.assertEqual(node.subpopulations[BACTERIA_SLOW], self.initial_slow_bac)

    def test_update_totals(self):
        # Put some infected macs in
        self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED] = 5
        self.network.node_list[23].subpopulations[MACROPHAGE_INFECTED] = 4
        self.network.node_list[13].subpopulations[MACROPHAGE_INFECTED] = 3

        self.network.node_list[16].subpopulations[BACTERIA_INTRACELLULAR] = 6
        self.network.node_list[23].subpopulations[BACTERIA_INTRACELLULAR] = 8
        self.network.node_list[13].subpopulations[BACTERIA_INTRACELLULAR] = 4
        self.network.update_totals()

        self.assertEqual(self.network.total_f, self.initial_fast_bac)
        self.assertEqual(self.network.total_s, self.initial_slow_bac)
        self.assertEqual(self.network.total_mac_regular, 36 * self.mac_per_patch)
        self.assertEqual(self.network.total_mac_infected, 5+4+3)
        self.assertEqual(self.network.total_f_degree, 3*1)
        self.assertEqual(self.network.total_s_degree, 2*1)
        self.assertEqual(self.network.total_regular_fast, 1*self.mac_per_patch + 1*self.mac_per_patch + 1*self.mac_per_patch)
        self.assertEqual(self.network.total_regular_slow, 1*self.mac_per_patch + 1*self.mac_per_patch)
        self.assertEqual(self.network.total_infected_fast, 5 * self.initial_fast_bac)
        self.assertEqual(self.network.total_infected_slow, 5 * self.initial_slow_bac)
        self.assertEqual(self.network.total_intra, 6+8+4)
        # TODO - based on simplistic V/Q
        self.assertEqual(self.network.total_f_o2, 3.0)
        self.assertEqual(self.network.total_s_o2, 2.0)

    def test_events(self):
        self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED] = 5
        self.network.node_list[23].subpopulations[MACROPHAGE_INFECTED] = 4
        self.network.node_list[13].subpopulations[MACROPHAGE_INFECTED] = 3
        self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR] = 10
        self.network.node_list[23].subpopulations[BACTERIA_INTRACELLULAR] = 8
        self.network.node_list[13].subpopulations[BACTERIA_INTRACELLULAR] = 6

        events = self.network.events()

        # Replication
        self.assertEqual(events[0][0], self.initial_fast_bac * self.rates[P_REPLICATE_FAST])
        self.assertEqual(events[1][0], self.initial_slow_bac * self.rates[P_REPLICATE_SLOW])
        self.assertEqual(events[2][0], (10+8+6) * self.rates[P_REPLICATE_INTRACELLULAR])

        # Metabolism change
        # TODO - based on simplistic V/Q
        self.assertEqual(events[3][0], 3.0 * self.rates[P_CHANGE_FAST_SLOW])
        self.assertEqual(events[4][0], 2.0 * self.rates[P_CHANGE_SLOW_FAST])

        # Migrate
        self.assertEqual(events[5][0], (3*1) * self.rates[P_MIGRATE_FAST])
        self.assertEqual(events[6][0], (2*1) * self.rates[P_MIGRATE_SLOW])

        # Recruit
        self.assertEqual(events[7][0], 36 * self.rates[P_RECRUIT])

        # Death
        self.assertEqual(events[8][0], (36 * self.mac_per_patch) * self.rates[P_DEATH_REGULAR])
        self.assertEqual(events[9][0], (5+4+3) * self.rates[P_DEATH_INFECTED])

        # Ingest
        self.assertEqual(events[10][0], (3 * self.mac_per_patch) * self.rates[P_REGULAR_INGEST_FAST])
        self.assertEqual(events[11][0], (2 * self.mac_per_patch) * self.rates[P_REGULAR_INGEST_SLOW])
        self.assertEqual(events[12][0], (5 * 3) * self.rates[P_INFECTED_INGEST_FAST])
        self.assertEqual(events[13][0], (5 * 2) * self.rates[P_INFECTED_INGEST_SLOW])

    def test_replicate_fast(self):

        self.network.replicate(BACTERIA_FAST)
        # Patch 26
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac+1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_replicate_slow(self):

        self.network.replicate(BACTERIA_SLOW)
        # Patch 27
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac+1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_regular_ingest_fast(self):
        np.random.seed(101)
        self.network.ingest(BACTERIA_FAST,MACROPHAGE_REGULAR)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch-1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 1)

    def test_regular_ingest_slow(self):
        np.random.seed(101)
        self.network.ingest(BACTERIA_SLOW,MACROPHAGE_REGULAR)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch-1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 1)

    def test_infected_ingest_fast(self):
        np.random.seed(101)
        self.network.update_node(self.network.node_list[26], MACROPHAGE_INFECTED, 13)
        self.network.update_node(self.network.node_list[26], BACTERIA_INTRACELLULAR, 26)
        self.network.update_totals()
        self.network.ingest(BACTERIA_FAST,MACROPHAGE_INFECTED)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 27)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 13)

    def test_infected_ingest_slow(self):
        np.random.seed(101)
        self.network.update_node(self.network.node_list[26], MACROPHAGE_INFECTED, 13)
        self.network.update_node(self.network.node_list[26], BACTERIA_INTRACELLULAR, 26)
        self.network.update_totals()
        self.network.ingest(BACTERIA_SLOW,MACROPHAGE_INFECTED)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 27)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 13)

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
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_SLOW], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)

    def test_migrate_slow(self):
        np.random.seed(101)
        self.network.migrate(BACTERIA_SLOW)
        # Patch 5 to patch 2
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[11].subpopulations[BACTERIA_SLOW], 1)
        self.assertEqual(self.network.node_list[11].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)

    def test_change_fast_to_slow(self):
        np.random.seed(101)
        self.network.change(BACTERIA_SLOW)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac+1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 0)

    def test_change_slow_to_fast(self):
        np.random.seed(101)
        self.network.change(BACTERIA_FAST)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_FAST], self.initial_fast_bac+1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_SLOW], self.initial_slow_bac-1)
        self.assertEqual(self.network.node_list[26].subpopulations[BACTERIA_INTRACELLULAR], 0)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_REGULAR], self.mac_per_patch)
        self.assertEqual(self.network.node_list[26].subpopulations[MACROPHAGE_INFECTED], 0)

if __name__ == '__main__':
    unittest.main()
