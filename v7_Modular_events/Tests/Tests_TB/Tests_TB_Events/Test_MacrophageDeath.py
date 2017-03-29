import unittest

from v7_Modular_events.Models.TB.TBEvents.MacrophageDeath import *
from v7_Modular_events.Models.Base.Patch import *


class MacrophageDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.class_die = MACROPHAGE_INFECTED
        self.class_released = BACTERIA_SLOW
        self.event_release = MacrophageDeath(self.class_die, 0.1, True, self.class_released)
        self.event_destroy = MacrophageDeath(self.class_die, 0.1, False)

    def test_initialise(self):
        self.assertEqual(self.event_release.class_to_die, self.class_die)
        self.assertTrue(self.event_release.release_load)
        self.assertEqual(self.event_release.class_to_release, self.class_released)
        self.assertEqual(self.event_destroy.class_to_die, self.class_die)
        self.assertFalse(self.event_destroy.release_load)

        # Release but no class defined
        with self.assertRaises(AssertionError) as context:
            e = MacrophageDeath(self.class_die, 0.1, True)
        self.assertEqual("Macrophage death: if bacteria released, must assign a class to release as",
                         str(context.exception))

    def test_update_network(self):
        # Release load and has intra
        node = Patch(0, [BACTERIA_INTRACELLULAR, self.class_die, self.class_released])
        node.update(self.class_die, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        self.event_release.update_network(node, None)
        expected_bac_released = 100/10
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[self.class_die], 10-1)

        # Not release load and has intra
        node = Patch(0, [BACTERIA_INTRACELLULAR, self.class_die, self.class_released])
        node.update(self.class_die, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        self.event_destroy.update_network(node, None)
        expected_bac_released = 0
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[self.class_die], 10 - 1)

        # Release load and doesn't have intra
        no_intra_event_release = MacrophageDeath(MACROPHAGE_REGULAR, 0.1, True, self.class_released)
        node = Patch(0, [BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, self.class_released])
        node.update(MACROPHAGE_REGULAR, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        no_intra_event_release.update_network(node, None)
        expected_bac_released = 0
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[MACROPHAGE_REGULAR], 10 - 1)

        # Not release load and doesn't have intra
        no_intra_event_destroy = MacrophageDeath(MACROPHAGE_REGULAR, 0.1, False)
        node = Patch(0, [BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, self.class_released])
        node.update(MACROPHAGE_REGULAR, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        no_intra_event_destroy.update_network(node, None)
        expected_bac_released = 0
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[MACROPHAGE_REGULAR], 10 - 1)


class TCellKillsMacrophageTestCase(unittest.TestCase):

    def setUp(self):
        self.mac_type = MACROPHAGE_INFECTED
        self.t_cell_type = T_CELL
        self.class_released = BACTERIA_SLOW
        self.event_release_kill = TCellKillsMacrophage(self.mac_type, self.t_cell_type, 0.1, True, self.class_released,
                                                       True)
        self.event_destroy_dont_kill = TCellKillsMacrophage(self.mac_type, self.t_cell_type, 0.1, False,
                                                            self.class_released, False)

    def test_initialise(self):
        self.assertEqual(self.event_release_kill.class_to_die, self.mac_type)
        self.assertTrue(self.event_release_kill.release_load)
        self.assertEqual(self.event_release_kill.class_to_release, self.class_released)
        self.assertTrue(self.event_release_kill.kill_t_cell)
        self.assertEqual(self.event_destroy_dont_kill.class_to_die, self.mac_type)
        self.assertFalse(self.event_destroy_dont_kill.release_load)
        self.assertFalse(self.event_destroy_dont_kill.kill_t_cell)

        # Release but no class defined
        with self.assertRaises(AssertionError) as context:
            e = TCellKillsMacrophage(self.mac_type, self.t_cell_type, 0.1, True)
        self.assertEqual("T Cell Kills Macrophage: if bacteria released, must assign a class to release as",
                         str(context.exception))

    def test_update_network(self):
        # Release load and has intra
        node = Patch(0, [BACTERIA_INTRACELLULAR, self.mac_type, self.class_released, self.t_cell_type])
        node.update(self.mac_type, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        node.update(self.t_cell_type, 7)
        self.event_release_kill.update_network(node, None)
        expected_bac_released = 100 / 10
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[self.mac_type], 10 - 1)

        # Kills t cell
        self.assertEqual(node.subpopulations[self.t_cell_type], 7 - 1)

        # Not release load and has intra
        node = Patch(0, [BACTERIA_INTRACELLULAR, self.mac_type, self.class_released, self.t_cell_type])
        node.update(self.mac_type, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        node.update(self.t_cell_type, 7)
        self.event_destroy_dont_kill.update_network(node, None)
        expected_bac_released = 0
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[self.mac_type], 10 - 1)

        # Doesn't kill t cell
        self.assertEqual(node.subpopulations[self.t_cell_type], 7)

        # Release load and doesn't have intra
        no_intra_event_release = MacrophageDeath(MACROPHAGE_REGULAR, 0.1, True, self.class_released)
        node = Patch(0, [BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, self.class_released, self.t_cell_type])
        node.update(MACROPHAGE_REGULAR, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        node.update(self.t_cell_type, 7)
        no_intra_event_release.update_network(node, None)
        expected_bac_released = 0
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[MACROPHAGE_REGULAR], 10 - 1)

        # Not release load and doesn't have intra
        no_intra_event_destroy = MacrophageDeath(MACROPHAGE_REGULAR, 0.1, False)
        node = Patch(0, [BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, self.class_released, self.t_cell_type])
        node.update(MACROPHAGE_REGULAR, 10)
        node.update(BACTERIA_INTRACELLULAR, 100)
        node.update(self.t_cell_type, 7)
        no_intra_event_destroy.update_network(node, None)
        expected_bac_released = 0
        self.assertEqual(node.subpopulations[self.class_released], expected_bac_released)
        self.assertEqual(node.subpopulations[MACROPHAGE_REGULAR], 10 - 1)


if __name__ == '__main__':
    unittest.main()
