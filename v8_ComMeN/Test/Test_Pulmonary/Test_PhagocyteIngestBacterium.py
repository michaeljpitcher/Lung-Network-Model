import unittest

from v8_ComMeN.ComMeN.Base.Node.Patch import *
from v8_ComMeN.ComMeN.Pulmonary.Events.Phagocytosis import *


class MacrophageIngestBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        self.mac_original = 'mac_o'
        self.mac_new = 'mac_n'
        self.bac_original = 'bac_o'
        self.bac_new = 'bac_n'

        self.event_no_change = Phagocytosis(None, 0.1, self.mac_original, self.bac_original)
        self.event_bac_change = Phagocytosis(None, 0.1, self.mac_original, self.bac_original,
                                             compartment_to_change_ingested_to=self.bac_new)
        self.event_mac_change = Phagocytosis(None, 0.1, self.mac_original, self.bac_original,
                                             compartment_to_change_phagocyte_to=self.mac_new)
        self.event_both_change = Phagocytosis(None, 0.1, self.mac_original, self.bac_original,
                                              compartment_to_change_ingested_to=self.bac_new,
                                              compartment_to_change_phagocyte_to=self.mac_new)

    def test_initialise(self):
        self.assertEqual(self.event_no_change.phagocyte_compartment, self.mac_original)
        self.assertEqual(self.event_no_change.compartment_to_change_phagocyte_to, None)
        self.assertEqual(self.event_no_change.compartment_to_change_ingested_to, None)
        self.assertEqual(self.event_bac_change.phagocyte_compartment, self.mac_original)
        self.assertEqual(self.event_bac_change.compartment_to_change_phagocyte_to, None)
        self.assertEqual(self.event_bac_change.compartment_to_change_ingested_to, self.bac_new)
        self.assertEqual(self.event_mac_change.phagocyte_compartment, self.mac_original)
        self.assertEqual(self.event_mac_change.compartment_to_change_phagocyte_to, self.mac_new)
        self.assertEqual(self.event_mac_change.compartment_to_change_ingested_to, None)
        self.assertEqual(self.event_both_change.phagocyte_compartment, self.mac_original)
        self.assertEqual(self.event_both_change.compartment_to_change_phagocyte_to, self.mac_new)
        self.assertEqual(self.event_both_change.compartment_to_change_ingested_to, self.bac_new)

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
        self.event = PhagocyteDestroyInternals(None, 0.1, self.mac_inf, self.bac, self.mac_heal)

    def test_initialise(self):
        self.assertEqual(self.event.phagocyte_compartment, self.mac_inf)
        self.assertEqual(self.event.healed_phagocyte_compartment, self.mac_heal)

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
