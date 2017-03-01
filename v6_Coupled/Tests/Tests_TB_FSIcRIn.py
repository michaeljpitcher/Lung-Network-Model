import unittest
from ..Models.TB.TB_FSIcRIn import *


class TBFSIcRInInitialiseTestCase(unittest.TestCase):

    def setUp(self):
        self.positions = dict()
        for i in range(45):
            self.positions[i] = (5, 5)

        self.parameters = dict()
        self.parameters[FAST_BACTERIA_TO_LOAD] = 5
        self.parameters[SLOW_BACTERIA_TO_LOAD] = 4
        self.parameters[MACROPHAGES_PER_BPS] = 10
        self.parameters[MACROPHAGES_PER_LYMPH] = 7
        self.parameters[P_REPLICATE_FAST] = 0.01
        self.parameters[P_REPLICATE_SLOW] = 0.02
        self.parameters[P_REPLICATE_INTRACELLULAR] = 0.03
        self.parameters[P_MIGRATE_FAST] = 0.04
        self.parameters[P_MIGRATE_SLOW] = 0.05
        self.parameters[P_CHANGE_FAST_TO_SLOW] = 0.06
        self.parameters[P_CHANGE_SLOW_TO_FAST] = 0.07
        self.parameters[P_BPS_RECRUIT_MACROPHAGE] = 0.08
        self.parameters[P_LYMPH_RECRUIT_MACROPHAGE] = 0.09
        self.parameters[P_DEATH_REGULAR_MACROPHAGE] = 0.10
        self.parameters[P_DEATH_INFECTED_MACROPHAGE] = 0.11
        self.parameters[P_REGULAR_MACROPHAGE_INGEST_FAST] = 0.12
        self.parameters[P_REGULAR_MACROPHAGE_INGEST_SLOW] = 0.13
        self.parameters[P_INFECTED_MACROPHAGE_INGEST_FAST] = 0.14
        self.parameters[P_INFECTED_MACROPHAGE_INGEST_SLOW] = 0.15
        self.parameters[P_MIGRATE_REGULAR_MACROPHAGE] = 0.16
        self.parameters[P_MIGRATE_INFECTED_MACROPHAGE] = 0.17

        np.random.seed(101)

        self.network = TB_FSIcRIn(self.positions, self.parameters)

    def test_initialise(self):
        expected_species = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR,
                            MACROPHAGE_INFECTED]
        self.assertItemsEqual(self.network.species, expected_species)

        expected_parameters = self.parameters
        self.assertItemsEqual(self.network.parameters.keys(), expected_parameters.keys())
        for key in self.network.parameters:
            expected_value = expected_parameters[key]
            self.assertEqual(self.network.parameters[key], expected_value)

        # Check subpopulation values
        # BPS
        for n in range(0, 36):
            # Bacteria deposited in node 27
            if n == 27:
                self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_FAST],
                                 self.parameters[FAST_BACTERIA_TO_LOAD])
                self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_SLOW],
                                 self.parameters[SLOW_BACTERIA_TO_LOAD])
            else:
                self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_FAST], 0)
                self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_SLOW], 0)

            self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_INTRACELLULAR], 0)
            self.assertEqual(self.network.node_list[n].subpopulations[MACROPHAGE_REGULAR],
                             self.parameters[MACROPHAGES_PER_BPS])
            self.assertEqual(self.network.node_list[n].subpopulations[MACROPHAGE_INFECTED], 0)
        # LYMPH
        for n in range(36, 45):
            self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_FAST], 0)
            self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_SLOW], 0)

            self.assertEqual(self.network.node_list[n].subpopulations[BACTERIA_INTRACELLULAR], 0)
            self.assertEqual(self.network.node_list[n].subpopulations[MACROPHAGE_REGULAR],
                         self.parameters[MACROPHAGES_PER_LYMPH])
            self.assertEqual(self.network.node_list[n].subpopulations[MACROPHAGE_INFECTED], 0)

class TBFSIcRInFunctionsTestCase(unittest.TestCase):

    def setUp(self):
        self.positions = dict()
        for i in range(45):
            self.positions[i] = (np.random.randint(0, 10), np.random.randint(0, 10))

        self.parameters = dict()
        self.parameters[FAST_BACTERIA_TO_LOAD] = 0
        self.parameters[SLOW_BACTERIA_TO_LOAD] = 0
        self.parameters[MACROPHAGES_PER_BPS] = 0
        self.parameters[MACROPHAGES_PER_LYMPH] = 0
        self.parameters[P_REPLICATE_FAST] = 0.0
        self.parameters[P_REPLICATE_SLOW] = 0.0
        self.parameters[P_REPLICATE_INTRACELLULAR] = 0.0
        self.parameters[P_MIGRATE_FAST] = 0.0
        self.parameters[P_MIGRATE_SLOW] = 0.0
        self.parameters[P_CHANGE_FAST_TO_SLOW] = 0.0
        self.parameters[P_CHANGE_SLOW_TO_FAST] = 0.0
        self.parameters[P_BPS_RECRUIT_MACROPHAGE] = 0.0
        self.parameters[P_LYMPH_RECRUIT_MACROPHAGE] = 0.0
        self.parameters[P_DEATH_REGULAR_MACROPHAGE] = 0.0
        self.parameters[P_DEATH_INFECTED_MACROPHAGE] = 0.0
        self.parameters[P_REGULAR_MACROPHAGE_INGEST_FAST] = 0.0
        self.parameters[P_REGULAR_MACROPHAGE_INGEST_SLOW] = 0.0
        self.parameters[P_INFECTED_MACROPHAGE_INGEST_FAST] = 0.0
        self.parameters[P_INFECTED_MACROPHAGE_INGEST_SLOW] = 0.0
        self.parameters[P_MIGRATE_REGULAR_MACROPHAGE] = 0.0
        self.parameters[P_MIGRATE_INFECTED_MACROPHAGE] = 0.0

        np.random.seed(101)

        self.network = TB_FSIcRIn(self.positions, self.parameters)

    def test_update_totals(self):
        # All zero
        self.network.update_totals()
        self.assertEqual(self.network.total_fast_bac, 0)
        self.assertEqual(self.network.total_slow_bac, 0)
        self.assertEqual(self.network.total_intracellular_bac, 0)
        self.assertEqual(self.network.total_reg_macrophage, 0)
        self.assertEqual(self.network.total_inf_macrophage, 0)
        self.assertEqual(self.network.total_fast_o2, 0)
        self.assertEqual(self.network.total_slow_o2, 0)
        self.assertEqual(self.network.total_fast_migrate, 0)
        self.assertEqual(self.network.total_slow_migrate, 0)
        self.assertEqual(self.network.total_reg_macrophage_and_fast, 0)
        self.assertEqual(self.network.total_reg_macrophage_and_slow, 0)
        self.assertEqual(self.network.total_inf_macrophage_and_fast, 0)
        self.assertEqual(self.network.total_inf_macrophage_and_slow, 0)
        self.assertEqual(self.network.total_reg_mac_migrate, 0)
        self.assertEqual(self.network.total_inf_mac_migrate, 0)

    def test_update_totals_bacteria(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[1].subpopulations[BACTERIA_SLOW] = 4
        self.network.node_list[33].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[43].subpopulations[BACTERIA_SLOW] = 6
        self.network.node_list[7].subpopulations[BACTERIA_INTRACELLULAR] = 7
        self.network.node_list[29].subpopulations[BACTERIA_INTRACELLULAR] = 8
        self.network.node_list[41].subpopulations[BACTERIA_INTRACELLULAR] = 9

        self.network.update_totals()

        expected_fast = 1+2+3
        self.assertEqual(self.network.total_fast_bac, expected_fast)
        expected_slow = 4+5+6
        self.assertEqual(self.network.total_slow_bac, expected_slow)
        expected_intrac = 7+8+9
        self.assertEqual(self.network.total_intracellular_bac, expected_intrac)

    def test_update_totals_macrophages(self):
        self.network.node_list[15].subpopulations[MACROPHAGE_REGULAR] = 10
        self.network.node_list[30].subpopulations[MACROPHAGE_REGULAR] = 11
        self.network.node_list[39].subpopulations[MACROPHAGE_REGULAR] = 12
        self.network.node_list[3].subpopulations[MACROPHAGE_INFECTED] = 13
        self.network.node_list[22].subpopulations[MACROPHAGE_INFECTED] = 14
        self.network.node_list[41].subpopulations[MACROPHAGE_INFECTED] = 15

        self.network.update_totals()

        expected_regular = 10+11+12
        self.assertEqual(self.network.total_reg_macrophage, expected_regular)
        expected_infected = 13+14+15
        self.assertEqual(self.network.total_inf_macrophage, expected_infected)

    def test_update_totals_bac_migration(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[1].subpopulations[BACTERIA_SLOW] = 4
        self.network.node_list[33].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[43].subpopulations[BACTERIA_SLOW] = 6

        self.network.update_totals()

        expected_fast_migrate = (1 * len(self.network.get_neighbouring_edges(self.network.node_list[0], BRONCHUS))) + \
                                (2 * len(self.network.get_neighbouring_edges(self.network.node_list[2], BRONCHUS))) + \
                                (3 * len(self.network.get_neighbouring_edges(self.network.node_list[40], BRONCHUS)))
        self.assertEqual(self.network.total_fast_migrate, expected_fast_migrate)
        expected_slow_migrate = (4 * len(self.network.get_neighbouring_edges(self.network.node_list[1], BRONCHUS))) + \
                                (5 * len(self.network.get_neighbouring_edges(self.network.node_list[33], BRONCHUS))) + \
                                (6 * len(self.network.get_neighbouring_edges(self.network.node_list[43], BRONCHUS)))
        self.assertEqual(self.network.total_slow_migrate, expected_slow_migrate)

    def test_update_totals_bacteria_o2(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[1].subpopulations[BACTERIA_SLOW] = 4
        self.network.node_list[33].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[43].subpopulations[BACTERIA_SLOW] = 6

        self.network.update_totals()
        expected_fast_o2 = (1 * (1 / self.network.node_list[0].oxygen_tension)) + \
                                (2 * (1 / self.network.node_list[2].oxygen_tension))
        self.assertEqual(self.network.total_fast_o2, expected_fast_o2)
        expected_slow_o2 = (4 * self.network.node_list[1].oxygen_tension) + \
                                (5 * self.network.node_list[33].oxygen_tension)
        self.assertEqual(self.network.total_slow_o2, expected_slow_o2)

    def test_update_totals_reg_mac_and_bac(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[1].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[41].subpopulations[BACTERIA_FAST] = 4
        self.network.node_list[2].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[3].subpopulations[BACTERIA_SLOW] = 6
        self.network.node_list[39].subpopulations[BACTERIA_SLOW] = 7
        self.network.node_list[38].subpopulations[BACTERIA_SLOW] = 8
        self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR] = 9
        self.network.node_list[2].subpopulations[MACROPHAGE_REGULAR] = 11
        self.network.node_list[4].subpopulations[MACROPHAGE_REGULAR] = 12
        self.network.node_list[40].subpopulations[MACROPHAGE_REGULAR] = 13
        self.network.node_list[39].subpopulations[MACROPHAGE_REGULAR] = 14
        self.network.node_list[42].subpopulations[MACROPHAGE_REGULAR] = 15

        self.network.update_totals()

        expected_reg_and_fast = (1 * 9) + (3 * 13)
        self.assertEqual(self.network.total_reg_macrophage_and_fast, expected_reg_and_fast)
        expected_reg_and_slow = (5 * 11) + (7 * 14)
        self.assertEqual(self.network.total_reg_macrophage_and_slow, expected_reg_and_slow)

    def test_update_totals_inf_mac_and_bac(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[1].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[41].subpopulations[BACTERIA_FAST] = 4
        self.network.node_list[2].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[3].subpopulations[BACTERIA_SLOW] = 6
        self.network.node_list[39].subpopulations[BACTERIA_SLOW] = 7
        self.network.node_list[38].subpopulations[BACTERIA_SLOW] = 8
        self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED] = 9
        self.network.node_list[2].subpopulations[MACROPHAGE_INFECTED] = 11
        self.network.node_list[4].subpopulations[MACROPHAGE_INFECTED] = 12
        self.network.node_list[40].subpopulations[MACROPHAGE_INFECTED] = 13
        self.network.node_list[39].subpopulations[MACROPHAGE_INFECTED] = 14
        self.network.node_list[42].subpopulations[MACROPHAGE_INFECTED] = 15

        self.network.update_totals()

        expected_inf_and_fast = (1 * 9) + (3 * 13)
        self.assertEqual(self.network.total_inf_macrophage_and_fast, expected_inf_and_fast)
        expected_inf_and_slow = (5 * 11) + (7 * 14)
        self.assertEqual(self.network.total_inf_macrophage_and_slow, expected_inf_and_slow)

    def test_update_totals_mac_migrate(self):
        self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR] = 1
        self.network.node_list[32].subpopulations[MACROPHAGE_REGULAR] = 2
        self.network.node_list[36].subpopulations[MACROPHAGE_REGULAR] = 3
        self.network.node_list[38].subpopulations[MACROPHAGE_REGULAR] = 4
        self.network.node_list[1].subpopulations[MACROPHAGE_INFECTED] = 5
        self.network.node_list[28].subpopulations[MACROPHAGE_INFECTED] = 6
        self.network.node_list[37].subpopulations[MACROPHAGE_INFECTED] = 7
        self.network.node_list[40].subpopulations[MACROPHAGE_INFECTED] = 8

        self.network.update_totals()

        expected_regular_migrate = (1 * len(
            self.network.get_neighbouring_edges(self.network.node_list[0], LYMPHATIC_VESSEL))) + (2 * len(
            self.network.get_neighbouring_edges(self.network.node_list[32], LYMPHATIC_VESSEL))) + (3 * len(
            self.network.get_neighbouring_edges(self.network.node_list[36], LYMPHATIC_VESSEL))) + (4 * len(
            self.network.get_neighbouring_edges(self.network.node_list[38], LYMPHATIC_VESSEL)))
        self.assertEqual(self.network.total_reg_mac_migrate, expected_regular_migrate)
        expected_infected_migrate = (5 * len(
            self.network.get_neighbouring_edges(self.network.node_list[1], LYMPHATIC_VESSEL))) + (6 * len(
            self.network.get_neighbouring_edges(self.network.node_list[28], LYMPHATIC_VESSEL))) + (7 * len(
            self.network.get_neighbouring_edges(self.network.node_list[37], LYMPHATIC_VESSEL))) + (8 * len(
            self.network.get_neighbouring_edges(self.network.node_list[40], LYMPHATIC_VESSEL)))
        self.assertEqual(self.network.total_inf_mac_migrate, expected_infected_migrate)

    def test_events_bac_replication(self):

        self.network.parameters[P_REPLICATE_FAST] = 0.1
        self.network.parameters[P_REPLICATE_SLOW] = 0.2
        self.network.parameters[P_REPLICATE_INTRACELLULAR] = 0.3

        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[1].subpopulations[BACTERIA_SLOW] = 4
        self.network.node_list[33].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[43].subpopulations[BACTERIA_SLOW] = 6
        self.network.node_list[7].subpopulations[BACTERIA_INTRACELLULAR] = 7
        self.network.node_list[29].subpopulations[BACTERIA_INTRACELLULAR] = 8
        self.network.node_list[41].subpopulations[BACTERIA_INTRACELLULAR] = 9

        self.network.update_totals()
        events = self.network.events()

        fast_replication = events[0]
        slow_replication = events[1]
        intrac_replication = events[2]

        self.assertEqual(fast_replication[0], (1 + 2 + 3) * 0.1)
        self.assertEqual(slow_replication[0], (4 + 5 + 6) * 0.2)
        self.assertEqual(intrac_replication[0], (7 + 8 + 9) * 0.3)

    def test_events_bac_migrate(self):

        self.network.parameters[P_MIGRATE_FAST] = 0.1
        self.network.parameters[P_MIGRATE_SLOW] = 0.2

        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[1].subpopulations[BACTERIA_SLOW] = 4
        self.network.node_list[33].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[43].subpopulations[BACTERIA_SLOW] = 6

        self.network.update_totals()

        events = self.network.events()

        fast_migrate = events[3]
        slow_migrate = events[4]

        expected_fast_migrate = ((1 * len(self.network.get_neighbouring_edges(self.network.node_list[0], BRONCHUS))) +
                                (2 * len(self.network.get_neighbouring_edges(self.network.node_list[2], BRONCHUS))) +
                                (3 * len(self.network.get_neighbouring_edges(self.network.node_list[40], BRONCHUS)))) \
                                * 0.1
        self.assertEqual(fast_migrate[0], expected_fast_migrate)
        expected_slow_migrate = ((4 * len(self.network.get_neighbouring_edges(self.network.node_list[1], BRONCHUS))) +
                                (5 * len(self.network.get_neighbouring_edges(self.network.node_list[33], BRONCHUS))) +
                                (6 * len(self.network.get_neighbouring_edges(self.network.node_list[43], BRONCHUS)))) \
                                * 0.2
        self.assertEqual(slow_migrate[0], expected_slow_migrate)

    def test_events_bac_change(self):
        self.network.parameters[P_CHANGE_FAST_TO_SLOW] = 0.1
        self.network.parameters[P_CHANGE_SLOW_TO_FAST] = 0.2

        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[1].subpopulations[BACTERIA_SLOW] = 4
        self.network.node_list[33].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[43].subpopulations[BACTERIA_SLOW] = 6

        self.network.update_totals()
        events = self.network.events()

        fast_to_slow = events[5]
        slow_to_fast = events[6]

        expected_fast_to_slow = ((1 * (1 / self.network.node_list[0].oxygen_tension)) +
                           (2 * (1 / self.network.node_list[2].oxygen_tension))) * 0.1
        self.assertEqual(fast_to_slow[0], expected_fast_to_slow)
        expected_slow_to_fast = ((4 * self.network.node_list[1].oxygen_tension) +
                           (5 * self.network.node_list[33].oxygen_tension)) * 0.2
        self.assertEqual(slow_to_fast[0], expected_slow_to_fast)

    def test_events_recruitment(self):
        self.network.parameters[P_BPS_RECRUIT_MACROPHAGE] = 0.1
        self.network.parameters[P_LYMPH_RECRUIT_MACROPHAGE] = 0.2

        self.network.update_totals()
        events = self.network.events()

        bps_recruit = events[7]
        ln_recruit = events[8]

        self.assertEqual(bps_recruit[0], 0.1 * 36)
        self.assertEqual(ln_recruit[0], 0.2 * 9)

    def test_events_death(self):
        self.network.parameters[P_DEATH_REGULAR_MACROPHAGE] = 0.1
        self.network.parameters[P_DEATH_INFECTED_MACROPHAGE] = 0.2

        self.network.node_list[15].subpopulations[MACROPHAGE_REGULAR] = 10
        self.network.node_list[30].subpopulations[MACROPHAGE_REGULAR] = 11
        self.network.node_list[39].subpopulations[MACROPHAGE_REGULAR] = 12
        self.network.node_list[3].subpopulations[MACROPHAGE_INFECTED] = 13
        self.network.node_list[22].subpopulations[MACROPHAGE_INFECTED] = 14
        self.network.node_list[41].subpopulations[MACROPHAGE_INFECTED] = 15

        self.network.update_totals()
        events = self.network.events()

        death_regular = events[9]
        death_infected = events[10]

        expected_death_regular = (10 + 11 + 12) * 0.1
        expected_death_infected = (13 + 14 + 15) * 0.2

        self.assertEqual(death_regular[0], expected_death_regular)
        self.assertEqual(death_infected[0], expected_death_infected)

    def test_events_mac_migrate(self):
        self.network.parameters[P_MIGRATE_REGULAR_MACROPHAGE] = 0.1
        self.network.parameters[P_MIGRATE_INFECTED_MACROPHAGE] = 0.2

        self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR] = 1
        self.network.node_list[32].subpopulations[MACROPHAGE_REGULAR] = 2
        self.network.node_list[36].subpopulations[MACROPHAGE_REGULAR] = 3
        self.network.node_list[38].subpopulations[MACROPHAGE_REGULAR] = 4
        self.network.node_list[1].subpopulations[MACROPHAGE_INFECTED] = 5
        self.network.node_list[28].subpopulations[MACROPHAGE_INFECTED] = 6
        self.network.node_list[37].subpopulations[MACROPHAGE_INFECTED] = 7
        self.network.node_list[40].subpopulations[MACROPHAGE_INFECTED] = 8

        self.network.update_totals()
        events = self.network.events()

        regular_migrate = events[11]
        infected_migrate = events[12]

        expected_regular_migrate = ((1 * len(
            self.network.get_neighbouring_edges(self.network.node_list[0], LYMPHATIC_VESSEL))) + (2 * len(
            self.network.get_neighbouring_edges(self.network.node_list[32], LYMPHATIC_VESSEL))) + (3 * len(
            self.network.get_neighbouring_edges(self.network.node_list[36], LYMPHATIC_VESSEL))) + (4 * len(
            self.network.get_neighbouring_edges(self.network.node_list[38], LYMPHATIC_VESSEL)))) * 0.1
        self.assertEqual(regular_migrate[0], expected_regular_migrate)
        expected_infected_migrate = ((5 * len(
            self.network.get_neighbouring_edges(self.network.node_list[1], LYMPHATIC_VESSEL))) + (6 * len(
            self.network.get_neighbouring_edges(self.network.node_list[28], LYMPHATIC_VESSEL))) + (7 * len(
            self.network.get_neighbouring_edges(self.network.node_list[37], LYMPHATIC_VESSEL))) + (8 * len(
            self.network.get_neighbouring_edges(self.network.node_list[40], LYMPHATIC_VESSEL)))) * 0.2
        self.assertEqual(infected_migrate[0], expected_infected_migrate)

    def test_events_reg_mac_ingest_bac(self):
        self.network.parameters[P_REGULAR_MACROPHAGE_INGEST_FAST] = 0.1
        self.network.parameters[P_REGULAR_MACROPHAGE_INGEST_SLOW] = 0.2

        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[1].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[41].subpopulations[BACTERIA_FAST] = 4
        self.network.node_list[2].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[3].subpopulations[BACTERIA_SLOW] = 6
        self.network.node_list[39].subpopulations[BACTERIA_SLOW] = 7
        self.network.node_list[38].subpopulations[BACTERIA_SLOW] = 8
        self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR] = 9
        self.network.node_list[2].subpopulations[MACROPHAGE_REGULAR] = 11
        self.network.node_list[4].subpopulations[MACROPHAGE_REGULAR] = 12
        self.network.node_list[40].subpopulations[MACROPHAGE_REGULAR] = 13
        self.network.node_list[39].subpopulations[MACROPHAGE_REGULAR] = 14
        self.network.node_list[42].subpopulations[MACROPHAGE_REGULAR] = 15

        self.network.update_totals()
        events = self.network.events()

        regular_ingest_fast = events[13]
        regular_ingest_slow = events[14]

        expected_reg_and_fast = ((1 * 9) + (3 * 13)) * 0.1
        self.assertEqual(regular_ingest_fast[0], expected_reg_and_fast)
        expected_reg_and_slow = ((5 * 11) + (7 * 14)) * 0.2
        self.assertEqual(regular_ingest_slow[0], expected_reg_and_slow)

    def test_events_inf_mac_ingest_bac(self):
        self.network.parameters[P_INFECTED_MACROPHAGE_INGEST_FAST] = 0.1
        self.network.parameters[P_INFECTED_MACROPHAGE_INGEST_SLOW] = 0.2

        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[1].subpopulations[BACTERIA_FAST] = 2
        self.network.node_list[40].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[41].subpopulations[BACTERIA_FAST] = 4
        self.network.node_list[2].subpopulations[BACTERIA_SLOW] = 5
        self.network.node_list[3].subpopulations[BACTERIA_SLOW] = 6
        self.network.node_list[39].subpopulations[BACTERIA_SLOW] = 7
        self.network.node_list[38].subpopulations[BACTERIA_SLOW] = 8
        self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED] = 9
        self.network.node_list[2].subpopulations[MACROPHAGE_INFECTED] = 11
        self.network.node_list[4].subpopulations[MACROPHAGE_INFECTED] = 12
        self.network.node_list[40].subpopulations[MACROPHAGE_INFECTED] = 13
        self.network.node_list[39].subpopulations[MACROPHAGE_INFECTED] = 14
        self.network.node_list[42].subpopulations[MACROPHAGE_INFECTED] = 15

        self.network.update_totals()
        events = self.network.events()

        infected_ingest_fast = events[15]
        infected_ingest_slow = events[16]

        expected_inf_and_fast = ((1 * 9) + (3 * 13)) * 0.1
        self.assertEqual(infected_ingest_fast[0], expected_inf_and_fast)
        expected_inf_and_slow = ((5 * 11) + (7 * 14)) * 0.2
        self.assertEqual(infected_ingest_slow[0], expected_inf_and_slow)

    def test_replicate(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[1].subpopulations[BACTERIA_SLOW] = 2
        self.network.node_list[2].subpopulations[BACTERIA_INTRACELLULAR] = 3

        self.network.update_totals()

        self.network.replicate(BACTERIA_FAST)
        node = self.network.node_list[0]
        self.assertEqual(node.subpopulations[BACTERIA_FAST], 2)

        self.network.replicate(BACTERIA_SLOW)
        node = self.network.node_list[1]
        self.assertEqual(node.subpopulations[BACTERIA_SLOW], 3)

        self.network.replicate(BACTERIA_INTRACELLULAR)
        node = self.network.node_list[2]
        self.assertEqual(node.subpopulations[BACTERIA_INTRACELLULAR], 4)

    def test_bac_migrate(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[30].subpopulations[BACTERIA_SLOW] = 2

        self.network.update_totals()
        self.network.bacteria_migrate(BACTERIA_FAST)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[1].subpopulations[BACTERIA_FAST], 1)

        self.network.update_totals()
        self.network.bacteria_migrate(BACTERIA_SLOW)
        self.assertEqual(self.network.node_list[30].subpopulations[BACTERIA_SLOW], 1)
        self.assertEqual(self.network.node_list[14].subpopulations[BACTERIA_SLOW], 1)

    def test_change(self):
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 1
        self.network.node_list[30].subpopulations[BACTERIA_SLOW] = 2

        self.network.update_totals()
        self.network.change_metabolism(BACTERIA_FAST)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_FAST], 0)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_SLOW], 1)

        self.network.node_list[0].subpopulations[BACTERIA_SLOW] = 0
        self.network.update_totals()

        self.network.change_metabolism(BACTERIA_SLOW)
        self.assertEqual(self.network.node_list[30].subpopulations[BACTERIA_FAST], 1)
        self.assertEqual(self.network.node_list[30].subpopulations[BACTERIA_SLOW], 1)

    def test_recruit_mac_bps(self):
        self.network.recruit_macrophage_bps()
        self.assertEqual(self.network.node_list[17].subpopulations[MACROPHAGE_REGULAR], 1)

    def test_recruit_mac_ln(self):
        self.network.recruit_macrophage_lymph()
        self.assertEqual(self.network.node_list[37].subpopulations[MACROPHAGE_REGULAR], 1)

    def test_mac_death(self):
        self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR] = 1
        self.network.node_list[1].subpopulations[MACROPHAGE_INFECTED] = 2
        self.network.node_list[1].subpopulations[BACTERIA_INTRACELLULAR] = 10

        self.network.update_totals()

        self.network.macrophage_death(MACROPHAGE_REGULAR)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR], 0)

        self.network.macrophage_death(MACROPHAGE_INFECTED)
        self.assertEqual(self.network.node_list[1].subpopulations[MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.network.node_list[1].subpopulations[BACTERIA_INTRACELLULAR], 5)
        self.assertEqual(self.network.node_list[1].subpopulations[BACTERIA_SLOW], 5)

    def test_mac_migrate(self):
        self.network.node_list[30].subpopulations[MACROPHAGE_REGULAR] = 1

        self.network.update_totals()
        self.network.macrophage_migrate(MACROPHAGE_REGULAR)

        self.assertEqual(self.network.node_list[30].subpopulations[MACROPHAGE_REGULAR], 0)
        self.assertEqual(self.network.node_list[42].subpopulations[MACROPHAGE_REGULAR], 1)

        self.network.node_list[44].subpopulations[MACROPHAGE_INFECTED] = 5
        self.network.node_list[44].subpopulations[BACTERIA_INTRACELLULAR] = 100

        self.network.update_totals()
        self.network.macrophage_migrate(MACROPHAGE_INFECTED)

        self.assertEqual(self.network.node_list[44].subpopulations[MACROPHAGE_INFECTED], 4)
        self.assertEqual(self.network.node_list[44].subpopulations[BACTERIA_INTRACELLULAR], 100 - (100 / 5))
        self.assertEqual(self.network.node_list[43].subpopulations[MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.network.node_list[43].subpopulations[BACTERIA_INTRACELLULAR], 100 / 5)

    def test_ingest_reg_fast(self):
        self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR] = 1
        self.network.node_list[1].subpopulations[MACROPHAGE_REGULAR] = 2
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 4

        self.network.update_totals()
        self.network.ingest(MACROPHAGE_REGULAR, BACTERIA_FAST)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR], 0)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_FAST], 2)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_INTRACELLULAR], 1)

    def test_ingest_reg_slow(self):
        self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR] = 1
        self.network.node_list[1].subpopulations[MACROPHAGE_REGULAR] = 2
        self.network.node_list[0].subpopulations[BACTERIA_SLOW] = 3
        self.network.node_list[2].subpopulations[BACTERIA_SLOW] = 4

        self.network.update_totals()
        self.network.ingest(MACROPHAGE_REGULAR, BACTERIA_SLOW)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE_REGULAR], 0)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_SLOW], 2)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_INTRACELLULAR], 1)

    def test_ingest_inf_fast(self):
        self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED] = 1
        self.network.node_list[1].subpopulations[MACROPHAGE_INFECTED] = 2
        self.network.node_list[0].subpopulations[BACTERIA_FAST] = 3
        self.network.node_list[2].subpopulations[BACTERIA_FAST] = 4

        self.network.update_totals()
        self.network.ingest(MACROPHAGE_INFECTED, BACTERIA_FAST)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_FAST], 2)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_INTRACELLULAR], 1)

    def test_ingest_inf_slow(self):
        self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED] = 1
        self.network.node_list[1].subpopulations[MACROPHAGE_INFECTED] = 2
        self.network.node_list[0].subpopulations[BACTERIA_SLOW] = 3
        self.network.node_list[2].subpopulations[BACTERIA_SLOW] = 4

        self.network.update_totals()
        self.network.ingest(MACROPHAGE_INFECTED, BACTERIA_SLOW)
        self.assertEqual(self.network.node_list[0].subpopulations[MACROPHAGE_INFECTED], 1)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_SLOW], 2)
        self.assertEqual(self.network.node_list[0].subpopulations[BACTERIA_INTRACELLULAR], 1)

if __name__ == '__main__':
    unittest.main()
