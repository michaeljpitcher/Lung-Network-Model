import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.TCellDeath import *


class SpontaneousTCellDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = SpontaneousTCellDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, T_CELL)


if __name__ == '__main__':
    unittest.main()
