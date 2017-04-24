import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.TCellDestroyMacrophage import *


class InfectedMacrophageDeathByTCellTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellDestroysInfectedMacrophage(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageDeathByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.internal_bacteria_compartment, BACTERIA_INTRACELLULAR)
        self.assertFalse(self.event.bacteria_release_compartment_to)
        self.assertItemsEqual(self.event.external_compartments, [T_CELL_CYTOTOXIC])
        self.assertFalse(self.event.externals_to_destroy)


if __name__ == '__main__':
    unittest.main()
