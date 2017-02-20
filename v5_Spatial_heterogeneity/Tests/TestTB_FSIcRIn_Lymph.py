import unittest
from v5_Spatial_heterogeneity.TB_Models.TB_FSIcRIn_Lymph import *


class TB_FSIcRIn_Lymph_TestCase(unittest.TestCase):

    def setUp(self):
        self.rates = dict()
        self.rates[P_REPLICATE_FAST] = 0.0
        self.rates[P_REPLICATE_SLOW] = 0.0
        self.rates[P_REPLICATE_INTRACELLULAR] = 0.0
        self.rates[P_MIGRATE_BRONCHI_FAST] = 0.0
        self.rates[P_MIGRATE_BRONCHI_SLOW] = 0.0
        self.rates[P_CHANGE_FAST_SLOW] = 0.0
        self.rates[P_CHANGE_SLOW_FAST] = 0.0
        self.rates[P_RECRUIT] = 0.0
        self.rates[P_DEATH_REGULAR] = 0.0
        self.rates[P_DEATH_INFECTED] = 0.0
        self.rates[P_REGULAR_INGEST_BAC] = 0.0
        self.rates[P_INFECTED_INGEST_BAC] = 0.0

        self.mac_per_bronch = 0
        self.mac_per_lymph = 0
        self.fast_to_deposit = 0
        self.slow_to_deposit = 0

        np.random.seed(101)
        self.network = TBMetapopulationNetwork_FSIcRIn_Lymph(self.rates, self.mac_per_bronch, self.mac_per_lymph,
                                                             self.fast_to_deposit, self.slow_to_deposit)

    def test_initialise(self):

        self.network = TBMetapopulationNetwork_FSIcRIn_Lymph(self.rates, 10, 7, 5, 3)

        for n in self.network.node_list_bps:
            self.assertEqual(n.subpopulations[MACROPHAGE_REGULAR], 10)
            self.assertEqual(n.subpopulations[MACROPHAGE_INFECTED], 0)
        for n in self.network.node_list_lymph:
            self.assertEqual(n.subpopulations[MACROPHAGE_REGULAR], 7)
            self.assertEqual(n.subpopulations[MACROPHAGE_INFECTED], 0)

        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_FAST], 5)
        self.assertEqual(self.network.node_list[27].subpopulations[BACTERIA_SLOW], 3)

    def test_update_totals(self):
        # All zero
        self.network.update_totals()
        self.assertEqual(self.network.total_f, 0)
        self.assertEqual(self.network.total_s, 0)
        self.assertEqual(self.network.total_intra, 0)
        self.assertEqual(self.network.total_mac_regular, 0)
        self.assertEqual(self.network.total_mac_infected, 0)
        self.assertEqual(self.network.total_f_o2, 0)
        self.assertEqual(self.network.total_s_o2, 0)
        self.assertEqual(self.network.total_f_migrate_bronchi, 0)
        self.assertEqual(self.network.total_s_migrate_bronchi, 0)
        self.assertEqual(self.network.total_regular_bac, 0)
        self.assertEqual(self.network.total_infected_bac, 0)

        # Set some values
        self.network.update_node(self.network.node_list[0], BACTERIA_FAST, 11)
        self.network.update_node(self.network.node_list[1], BACTERIA_FAST, 5)
        self.network.update_node(self.network.node_list[0], MACROPHAGE_REGULAR, 13)
        self.network.update_node(self.network.node_list[0], MACROPHAGE_INFECTED, 7)
        self.network.update_node(self.network.node_list[0], BACTERIA_INTRACELLULAR, 7)
        self.network.update_node(self.network.node_list[13], BACTERIA_SLOW, 17)

        self.network.update_node(self.network.node_list[30], MACROPHAGE_REGULAR, 2)
        self.network.update_node(self.network.node_list[30], MACROPHAGE_INFECTED, 4)
        self.network.update_node(self.network.node_list[30], BACTERIA_INTRACELLULAR, 50)

        self.network.update_totals()
        self.assertEqual(self.network.total_f, 11 + 5)
        self.assertEqual(self.network.total_s, 17)
        self.assertEqual(self.network.total_intra, 7 + 50)
        self.assertEqual(self.network.total_mac_regular, 13 + 2)
        self.assertEqual(self.network.total_mac_infected, 7 + 4)
        self.assertEqual(self.network.total_f_o2, (11*(1/self.network.node_list[0].oxygen_tension)) +
                         (5*(1/self.network.node_list[1].oxygen_tension)))
        self.assertEqual(self.network.total_s_o2, 17*self.network.node_list[13].oxygen_tension)
        self.assertEqual(self.network.total_f_migrate_bronchi, 11*1 + 5*3)
        self.assertEqual(self.network.total_s_migrate_bronchi, 17*3)
        self.assertEqual(self.network.total_regular_bac, 13*11)
        self.assertEqual(self.network.total_infected_bac, 7*11)

    def test_events(self):
        events = self.network.events()
        for (rate,event) in events:
            self.assertEqual(rate, 0.0)

        # Set some values
        self.network.update_node(self.network.node_list[0], BACTERIA_FAST, 11)
        self.network.update_node(self.network.node_list[1], BACTERIA_FAST, 5)
        self.network.update_node(self.network.node_list[0], MACROPHAGE_REGULAR, 13)
        self.network.update_node(self.network.node_list[0], MACROPHAGE_INFECTED, 7)
        self.network.update_node(self.network.node_list[0], BACTERIA_INTRACELLULAR, 7)
        self.network.update_node(self.network.node_list[13], BACTERIA_SLOW, 17)

        self.network.update_node(self.network.node_list[30], MACROPHAGE_REGULAR, 2)
        self.network.update_node(self.network.node_list[30], MACROPHAGE_INFECTED, 4)
        self.network.update_node(self.network.node_list[30], BACTERIA_INTRACELLULAR, 50)

        # Still 0 - p = 0 for all
        events = self.network.events()
        for (rate, event) in events:
            self.assertEqual(rate, 0.0)

        # set the p values
        self.network.rates[P_REPLICATE_FAST] = 0.01
        self.network.rates[P_REPLICATE_SLOW] = 0.02
        self.network.rates[P_REPLICATE_INTRACELLULAR] = 0.03
        self.network.rates[P_CHANGE_FAST_SLOW] = 0.04
        self.network.rates[P_CHANGE_SLOW_FAST] = 0.05

        self.network.rates[P_MIGRATE_BRONCHI_FAST] = 0.06
        self.network.rates[P_MIGRATE_BRONCHI_SLOW] = 0.07

        self.network.rates[P_RECRUIT] = 0.08
        self.network.rates[P_DEATH_REGULAR] = 0.09
        self.network.rates[P_DEATH_INFECTED] = 0.10
        self.network.rates[P_REGULAR_INGEST_BAC] = 0.11
        self.network.rates[P_INFECTED_INGEST_BAC] = 0.12

        events = self.network.events()

        # Replicate
        self.assertEqual(events[0][0], (11 + 5) * 0.01)
        self.assertEqual(events[1][0], 17 * 0.02)
        self.assertEqual(events[2][0], (50 + 7) * 0.03)

        # Change metabolism
        self.assertEqual(events[3][0], ((11*(1/self.network.node_list[0].oxygen_tension)) +
                         (5*(1/self.network.node_list[1].oxygen_tension))) * 0.04)
        self.assertEqual(events[4][0], (17*self.network.node_list[13].oxygen_tension) * 0.05)

        # Migrate
        self.assertEqual(events[5][0], (11*1 + 5*3) * 0.06)
        self.assertEqual(events[6][0], (17*3) * 0.07)

        # Recruit
        self.assertEqual(events[7][0], (42) * 0.08)

        # Death
        self.assertEqual(events[8][0], (13 + 2) * 0.09)
        self.assertEqual(events[9][0], (7 + 4) * 0.10)

        # Ingest
        self.assertEqual(events[10][0], (13*11) * 0.11)
        self.assertEqual(events[11][0], (7*11) * 0.12)


if __name__ == '__main__':
    unittest.main()
