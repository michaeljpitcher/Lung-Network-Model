import unittest

from v8_ComMeN.ComMeN.TB.Events.MacrophageIngestBacteria import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class MacrophageIngestBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        self.mac_original = 'mac_o'
        self.mac_new = 'mac_n'
        self.bac_original = 'bac_o'
        self.bac_new = 'bac_n'

        self.event_no_change = MacrophageIngestBacteria(None, 0.1, self.mac_original, self.bac_original)
        self.event_bac_change = MacrophageIngestBacteria(None, 0.1, self.mac_original, self.bac_original,
                                                         bacteria_change_compartment=self.bac_new)
        self.event_mac_change = MacrophageIngestBacteria(None, 0.1, self.mac_original, self.bac_original,
                                                         macrophage_change_compartment=self.mac_new)
        self.event_both_change = MacrophageIngestBacteria(None, 0.1, self.mac_original, self.bac_original,
                                                          bacteria_change_compartment=self.bac_new,
                                                          macrophage_change_compartment=self.mac_new)

    def test_initialise(self):
        self.assertEqual(self.event_no_change.macrophage_compartment, self.mac_original)
        self.assertEqual(self.event_no_change.macrophage_change_compartment, None)
        self.assertEqual(self.event_no_change.bacteria_change_compartment, None)
        self.assertEqual(self.event_bac_change.macrophage_compartment, self.mac_original)
        self.assertEqual(self.event_bac_change.macrophage_change_compartment, None)
        self.assertEqual(self.event_bac_change.bacteria_change_compartment, self.bac_new)
        self.assertEqual(self.event_mac_change.macrophage_compartment, self.mac_original)
        self.assertEqual(self.event_mac_change.macrophage_change_compartment, self.mac_new)
        self.assertEqual(self.event_mac_change.bacteria_change_compartment, None)
        self.assertEqual(self.event_both_change.macrophage_compartment, self.mac_original)
        self.assertEqual(self.event_both_change.macrophage_change_compartment, self.mac_new)
        self.assertEqual(self.event_both_change.bacteria_change_compartment, self.bac_new)

    def test_increment_from_node(self):
        node = Patch(0, [self.bac_original, self.bac_new, self.mac_original, self.mac_new])
        self.assertEqual(self.event_no_change.increment_from_node(node, None), 0)
        node.update_subpopulation(self.bac_original, 13)
        self.assertEqual(self.event_no_change.increment_from_node(node, None), 0)
        node.update_subpopulation(self.mac_original, 5)
        self.assertEqual(self.event_no_change.increment_from_node(node, None), 13*5)

    def test_update_node(self):
        node = Patch(0, [self.bac_original, self.bac_new, self.mac_original, self.mac_new])
        node.update_subpopulation(self.bac_original, 2)
        node.update_subpopulation(self.mac_original, 2)
        self.event_no_change.update_node(node, None)
        self.assertEqual(node.subpopulations[self.bac_original], 1)
        self.assertEqual(node.subpopulations[self.mac_original], 2)
        self.assertEqual(node.subpopulations[self.bac_new], 0)
        self.assertEqual(node.subpopulations[self.mac_new], 0)

        node = Patch(0, [self.bac_original, self.bac_new, self.mac_original, self.mac_new])
        node.update_subpopulation(self.bac_original, 2)
        node.update_subpopulation(self.mac_original, 2)
        self.event_bac_change.update_node(node, None)
        self.assertEqual(node.subpopulations[self.bac_original], 1)
        self.assertEqual(node.subpopulations[self.mac_original], 2)
        self.assertEqual(node.subpopulations[self.bac_new], 1)
        self.assertEqual(node.subpopulations[self.mac_new], 0)

        node = Patch(0, [self.bac_original, self.bac_new, self.mac_original, self.mac_new])
        node.update_subpopulation(self.bac_original, 2)
        node.update_subpopulation(self.mac_original, 2)
        self.event_mac_change.update_node(node, None)
        self.assertEqual(node.subpopulations[self.bac_original], 1)
        self.assertEqual(node.subpopulations[self.mac_original], 1)
        self.assertEqual(node.subpopulations[self.bac_new], 0)
        self.assertEqual(node.subpopulations[self.mac_new], 1)

        node = Patch(0, [self.bac_original, self.bac_new, self.mac_original, self.mac_new])
        node.update_subpopulation(self.bac_original, 2)
        node.update_subpopulation(self.mac_original, 2)
        self.event_both_change.update_node(node, None)
        self.assertEqual(node.subpopulations[self.bac_original], 1)
        self.assertEqual(node.subpopulations[self.mac_original], 1)
        self.assertEqual(node.subpopulations[self.bac_new], 1)
        self.assertEqual(node.subpopulations[self.mac_new], 1)


class MacrophageDestroyInternalBacteriaTestCase(unittest.TestCase):

    def setUp(self):
        self.mac_inf = 'm_i'
        self.bac = 'bac'
        self.mac_heal = 'm_h'
        self.event = MacrophageDestroyInternalBacteria(None, 0.1, self.mac_inf, self.bac, self.mac_heal)

    def test_initialise(self):
        self.assertEqual(self.event.macrophage_compartment, self.mac_inf)
        self.assertEqual(self.event.healed_macrophage_compartment, self.mac_heal)

    def test_increment_from_node(self):
        node = Patch(0, [self.mac_heal, self.mac_inf, self.bac])
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.bac, 4)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.mac_inf, 5)
        node.update_subpopulation(self.bac, -4)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.bac, 4)
        self.assertEqual(self.event.increment_from_node(node, None), 5)

    def test_update_node(self):
        node = Patch(0, [self.mac_heal, self.mac_inf, self.bac])
        node.update_subpopulation(self.bac, 20)
        node.update_subpopulation(self.mac_inf, 4)
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.mac_inf], 4)
        self.assertEqual(node.subpopulations[self.bac], 19)
        self.assertEqual(node.subpopulations[self.mac_heal], 0)

        node = Patch(0, [self.mac_heal, self.mac_inf, self.bac])
        node.update_subpopulation(self.bac, 4)
        node.update_subpopulation(self.mac_inf, 4)
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.mac_inf], 3)
        self.assertEqual(node.subpopulations[self.bac], 3)
        self.assertEqual(node.subpopulations[self.mac_heal], 1)


if __name__ == '__main__':
    unittest.main()
