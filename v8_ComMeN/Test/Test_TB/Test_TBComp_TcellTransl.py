import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.TCellTranslocate import *


class RegularTCellTranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularTCellTranslocateBronchus(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL)
        self.assertTrue(self.event.edge_choice_based_on_weight)


class RegularTCellTranslocateLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularTCellTranslocateLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL)
        self.assertTrue(self.event.flow_based)
        self.assertTrue(self.event.direction_only)


class RegularTCellTranslocateBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularTCellTranslocateBlood(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL)
        self.assertTrue(self.event.direction_only)


if __name__ == '__main__':
    unittest.main()
