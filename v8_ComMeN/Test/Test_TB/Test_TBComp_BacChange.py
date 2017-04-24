import unittest
from v8_ComMeN.ComMeN.TB.Events.BacteriaChange import *


class BacteriaFastToSlow(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaChangeByOxygenFastToSlow(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOxygen))
        self.assertEqual(self.event.compartment_from, BACTERIA_FAST)
        self.assertEqual(self.event.compartment_to, BACTERIA_SLOW)
        self.assertFalse(self.event.oxygen_high_to_change)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])


class BacteriaSlowToFast(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaChangeByOxygenSlowToFast(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOxygen))
        self.assertEqual(self.event.compartment_from, BACTERIA_SLOW)
        self.assertEqual(self.event.compartment_to, BACTERIA_FAST)
        self.assertTrue(self.event.oxygen_high_to_change)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])

if __name__ == '__main__':
    unittest.main()
