import unittest

from v7_Modular_events.Models.TB.TBEvents.MacrophageIngestBacterium import *
from v7_Modular_events.Models.TB.TBClasses import *
from v7_Modular_events.Models.Base.Patch import *


class MacrophageIngestBacteriumTestCase(unittest.TestCase):
    def setUp(self):

        self.bac = BACTERIA_FAST
        self.mac = MACROPHAGE
        self.inf_mac = MACROPHAGE_INFECTED

        self.event_destroy_no_new_mac = MacrophageIngestBacterium(self.bac, self.mac, 0.1, True)
        self.event_destroy_new_mac = MacrophageIngestBacterium(self.bac, self.mac, 0.1, True, self.inf_mac)
        self.event_retain_and_change = MacrophageIngestBacterium(self.bac, self.mac, 0.1, False, self.inf_mac)
        self.event_retain_dont_change = MacrophageIngestBacterium(self.bac, self.inf_mac, 0.1, False)

    def test_initialise(self):
        self.assertTrue(self.event_destroy_no_new_mac.destroy_bacterium)
        self.assertTrue(self.event_destroy_new_mac.destroy_bacterium)
        self.assertFalse(self.event_retain_and_change.destroy_bacterium)
        self.assertFalse(self.event_retain_dont_change.destroy_bacterium)

        self.assertEqual(self.event_destroy_no_new_mac.new_macrophage_type, self.mac)
        self.assertEqual(self.event_retain_dont_change.new_macrophage_type, self.inf_mac)
        self.assertEqual(self.event_destroy_new_mac.new_macrophage_type, self.inf_mac)
        self.assertEqual(self.event_retain_and_change.new_macrophage_type, self.inf_mac)

        # Retain and don't change - current mac state can't hold bac
        with self.assertRaises(Exception) as context:
            ec = MacrophageIngestBacterium(self.bac, self.mac, 0.1, False)
        self.assertEqual("Class " + self.mac + " cannot retain bacteria", str(context.exception))

        # Retain and change - new mac state can't hold bac
        with self.assertRaises(Exception) as context:
            ec = MacrophageIngestBacterium(self.bac, self.mac, 0.1, False, MACROPHAGE_ACTIVATED)
        self.assertEqual("Class " + MACROPHAGE_ACTIVATED + " cannot retain bacteria", str(context.exception))

    def test_update_network(self):

        node = Patch(0, [BACTERIA_FAST, MACROPHAGE, MACROPHAGE_INFECTED])
        node.update(BACTERIA_FAST, 10)
        node.update(MACROPHAGE, 10)
        self.event_destroy_no_new_mac.update_network(node, None)
        self.assertEqual(node.subpopulations[BACTERIA_FAST], 10-1)
        self.assertEqual(node.subpopulations[MACROPHAGE], 10)
        self.assertEqual(node.subpopulations[MACROPHAGE_INFECTED], 0)

        node = Patch(0, [BACTERIA_FAST, MACROPHAGE, MACROPHAGE_INFECTED])
        node.update(BACTERIA_FAST, 10)
        node.update(MACROPHAGE, 10)
        self.event_destroy_new_mac.update_network(node, None)
        self.assertEqual(node.subpopulations[BACTERIA_FAST], 10 - 1)
        self.assertEqual(node.subpopulations[MACROPHAGE], 10-1)
        self.assertEqual(node.subpopulations[MACROPHAGE_INFECTED], 1)

        node = Patch(0, [BACTERIA_FAST, BACTERIA_INTRACELLULAR, MACROPHAGE, MACROPHAGE_INFECTED])
        node.update(BACTERIA_FAST, 10)
        node.update(MACROPHAGE, 10)
        self.event_retain_and_change.update_network(node, None)
        self.assertEqual(node.subpopulations[BACTERIA_FAST], 10 - 1)
        self.assertEqual(node.subpopulations[MACROPHAGE], 10 - 1)
        self.assertEqual(node.subpopulations[MACROPHAGE_INFECTED], 1)
        self.assertEqual(node.subpopulations[BACTERIA_INTRACELLULAR], 1)

        node = Patch(0, [BACTERIA_FAST, BACTERIA_INTRACELLULAR, MACROPHAGE, MACROPHAGE_INFECTED])
        node.update(BACTERIA_FAST, 10)
        node.update(MACROPHAGE_INFECTED, 10)
        self.event_retain_dont_change.update_network(node, None)
        self.assertEqual(node.subpopulations[BACTERIA_FAST], 10 - 1)
        self.assertEqual(node.subpopulations[MACROPHAGE], 0)
        self.assertEqual(node.subpopulations[MACROPHAGE_INFECTED], 10)
        self.assertEqual(node.subpopulations[BACTERIA_INTRACELLULAR], 1)


class MacrophageDestroysLoadTestCase(unittest.TestCase):

    def setUp(self):
        self.event = MacrophageDestroysLoad(0.1, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.mac_type_return_to, MACROPHAGE_REGULAR)

    def test_update_network(self):
        node = Patch(0, [BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, MACROPHAGE_INFECTED])
        node.update(BACTERIA_INTRACELLULAR, 100)
        node.update(MACROPHAGE_INFECTED, 10)
        self.event.update_network(node, None)
        self.assertEqual(node.subpopulations[BACTERIA_INTRACELLULAR], 99)
        self.assertEqual(node.subpopulations[MACROPHAGE_INFECTED], 10)

        node = Patch(0, [BACTERIA_INTRACELLULAR, MACROPHAGE_REGULAR, MACROPHAGE_INFECTED])
        node.update(BACTERIA_INTRACELLULAR, 10)
        node.update(MACROPHAGE_INFECTED, 10)
        self.event.update_network(node, None)
        self.assertEqual(node.subpopulations[BACTERIA_INTRACELLULAR], 9)
        self.assertEqual(node.subpopulations[MACROPHAGE_REGULAR], 1)
        self.assertEqual(node.subpopulations[MACROPHAGE_INFECTED], 9)


if __name__ == '__main__':
    unittest.main()
