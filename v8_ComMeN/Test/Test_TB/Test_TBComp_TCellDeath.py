import unittest

from v8_ComMeN.ComMeN.TB.Events.TCellDeath import *


class SpontaneousTCellNaiveHelperDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = SpontaneousTCellNaiveHelperDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, T_CELL_NAIVE_HELPER)


class SpontaneousTCellNaiveCytotoxicDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = SpontaneousTCellNaiveCytotoxicDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, T_CELL_NAIVE_CYTOTOXIC)


class SpontaneousTCellHelperDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = SpontaneousTCellHelperDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, T_CELL_HELPER)


class SpontaneousTCellCytotoxicDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = SpontaneousTCellCytotoxicDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, T_CELL_CYTOTOXIC)

if __name__ == '__main__':
    unittest.main()
