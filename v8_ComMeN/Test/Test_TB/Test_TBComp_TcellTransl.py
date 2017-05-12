import unittest

from v8_ComMeN.ComMeN.TBIndividual.Events.TCellTranslocate import *


class TCellHelperTranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperTranslocateBronchus(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL_HELPER)
        self.assertTrue(self.event.edge_choice_based_on_weight)


class TCellHelperTranslocateLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperTranslocateLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL_HELPER)
        self.assertTrue(self.event.flow_based)
        self.assertTrue(self.event.direction_only)


class TCellHelperTranslocateBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperTranslocateBlood(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL_HELPER)
        self.assertTrue(self.event.direction_only)


class TCellCytotoxicTranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicTranslocateBronchus(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL_CYTOTOXIC)
        self.assertTrue(self.event.edge_choice_based_on_weight)


class TCellCytotoxicTranslocateLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicTranslocateLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL_CYTOTOXIC)
        self.assertTrue(self.event.flow_based)
        self.assertTrue(self.event.direction_only)


class TCellCytotoxicTranslocateBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicTranslocateBlood(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.translocate_compartment, T_CELL_CYTOTOXIC)
        self.assertTrue(self.event.direction_only)


if __name__ == '__main__':
    unittest.main()
