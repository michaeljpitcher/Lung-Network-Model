import unittest

from v8_ComMeN.ComMeN.TBIndividual.Events.TCellActivatesMacrophage import *


class RegularMacrophageActivationByTCellsTestCase(unittest.TestCase):
    def setUp(self):
        self.event = MacrophageRegularActivationByTCellHelper(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.influencing_compartments, [T_CELL_HELPER])
        self.assertFalse(self.event.internals_to_destroy)


class InfectedMacrophageActivationByTCellsTestCase(unittest.TestCase):
    def setUp(self):
        self.event = MacrophageInfectedActivationByTCellHelper(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.influencing_compartments, [T_CELL_HELPER])
        self.assertEqual(self.event.internals_to_destroy, [BACTERIA_INTRACELLULAR])


if __name__ == '__main__':
    unittest.main()
