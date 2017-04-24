import unittest

from v8_ComMeN.ComMeN.TB.Events.TCellDestroyMacrophage import *


class InfectedMacrophageDeathByTCellTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicDestroysInfectedMacrophage(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, PhagocyteDeathByOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.internal_bacteria_compartment, BACTERIA_INTRACELLULAR)
        self.assertFalse(self.event.bacteria_release_compartment_to)
        self.assertItemsEqual(self.event.death_causing_compartments, [T_CELL_CYTOTOXIC])
        self.assertFalse(self.event.extra_compartments_to_destroy)


if __name__ == '__main__':
    unittest.main()
