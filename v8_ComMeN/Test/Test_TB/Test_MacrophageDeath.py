import unittest

from v8_ComMeN.ComMeN.TB.Events.MacrophageDeath import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class MacrophageDeathRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.mac = 'mac'
        self.bac_int = "bac_i"
        self.bac_ext = 'bac_e'
        self.event_bac_release = MacrophageDeathRegular(0.1, self.mac, self.bac_int, self.bac_ext)
        self.event_no_bac_release = MacrophageDeathRegular(0.1, self.mac)

    def test_initialise(self):
        self.assertEqual(self.event_bac_release.internal_bacteria_compartment, self.bac_int)
        self.assertEqual(self.event_bac_release.bacteria_release_compartment_to, self.bac_ext)
        self.assertEqual(self.event_no_bac_release.internal_bacteria_compartment, None)
        self.assertEqual(self.event_no_bac_release.bacteria_release_compartment_to, None)

        with self.assertRaises(AssertionError) as context:
            event = MacrophageDeathRegular(0.1, self.mac, bacteria_release_compartment_to=self.bac_ext)
        self.assertEqual('Cannot release bacteria without providing a compartment for them to be released from',
                         str(context.exception))

    def test_update_node(self):
        node = Patch(0, [self.mac, self.bac_int, self.bac_ext])
        node.update_subpopulation(self.mac, 11)
        node.update_subpopulation(self.bac_int, 99)
        self.event_bac_release.update_node(node, None)
        self.assertEqual(node.subpopulations[self.mac], 10)
        self.assertEqual(node.subpopulations[self.bac_int], 90)
        self.assertEqual(node.subpopulations[self.bac_ext], 9)

        node = Patch(0, [self.mac, self.bac_int, self.bac_ext])
        node.update_subpopulation(self.mac, 11)
        node.update_subpopulation(self.bac_int, 99)
        self.event_no_bac_release.update_node(node, None)
        self.assertEqual(node.subpopulations[self.mac], 10)
        self.assertEqual(node.subpopulations[self.bac_int], 99)
        self.assertEqual(node.subpopulations[self.bac_ext], 0)


class MacrophageDeathByTCellTestCase(unittest.TestCase):

    def setUp(self):
        self.mac = 'mac'
        self.tcell = 'tcell'
        self.event_destroy = MacrophageDeathByTCell(0.1, self.mac, self.tcell)
        self.event_not_destroy = MacrophageDeathByTCell(0.1, self.mac, self.tcell, False)

    def test_initialise(self):
        self.assertTrue(self.event_destroy.destroy_t_cell)
        self.assertFalse(self.event_not_destroy.destroy_t_cell)

    def test_increment_from_node(self):
        node = Patch(0, [self.mac, self.tcell])
        self.assertEqual(self.event_destroy.increment_from_node(node, None), 0)
        node.update_subpopulation(self.mac, 11)
        self.assertEqual(self.event_destroy.increment_from_node(node, None), 0)
        node.update_subpopulation(self.tcell, 5)
        self.assertEqual(self.event_destroy.increment_from_node(node, None), 11*5)

    def test_update_node(self):
        node = Patch(0, [self.mac, self.tcell])
        node.update_subpopulation(self.mac, 11)
        node.update_subpopulation(self.tcell, 9)
        self.event_destroy.update_node(node, None)
        self.assertEqual(node.subpopulations[self.mac], 10)
        self.assertEqual(node.subpopulations[self.tcell], 8)

        node = Patch(0, [self.mac, self.tcell])
        node.update_subpopulation(self.mac, 11)
        node.update_subpopulation(self.tcell, 9)
        self.event_not_destroy.update_node(node, None)
        self.assertEqual(node.subpopulations[self.mac], 10)
        self.assertEqual(node.subpopulations[self.tcell], 9)


class MacrophageDeathByInfectionTestCase(unittest.TestCase):

    def setUp(self):
        self.mac = 'mac'
        self.infection_comps = ['inf_1', 'inf_2']
        self.event = MacrophageDeathByInfection(0.1, self.mac, self.infection_comps)

    def test_initialise(self):
        self.assertItemsEqual(self.event.infection_compartments, self.infection_comps)

    def test_increment_from_node(self):
        node = Patch(0, [self.mac] + self.infection_comps)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.mac, 11)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.infection_comps[0], 5)
        self.assertEqual(self.event.increment_from_node(node, None), 11 * 5)
        node.update_subpopulation(self.infection_comps[1], 7)
        self.assertEqual(self.event.increment_from_node(node, None), 11 * (5 + 7))


if __name__ == '__main__':
    unittest.main()
