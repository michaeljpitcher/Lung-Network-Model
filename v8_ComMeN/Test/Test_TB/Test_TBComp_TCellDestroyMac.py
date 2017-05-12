import unittest

from v8_ComMeN.ComMeN.TBIndividual.Events.TCellDestroyMacrophage import *


class InfectedMacrophageDeathByTCellTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicDestroysInfectedMacrophage(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, DestroyByOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertItemsEqual(self.event.internals_to_destroy, [BACTERIA_INTRACELLULAR])
        self.assertFalse(self.event.internals_changed)
        self.assertItemsEqual(self.event.influencing_compartments, [T_CELL_CYTOTOXIC])
        self.assertFalse(self.event.influencers_to_destroy)
        self.assertFalse(self.event.influencers_changed)


if __name__ == '__main__':
    unittest.main()
