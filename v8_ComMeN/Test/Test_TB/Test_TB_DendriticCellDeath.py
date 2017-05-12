import unittest

from v8_ComMeN.ComMeN.TBIndividual.Events.DendriticCellDeath import *


class DendriticImmatureDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = DendriticImmatureDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, DENDRITIC_CELL_IMMATURE)


class DendriticMatureDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = DendriticMatureDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, DENDRITIC_CELL_MATURE)


if __name__ == '__main__':
    unittest.main()
