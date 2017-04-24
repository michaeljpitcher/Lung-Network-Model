import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.TCellActivatesMacrophage import *


class RegularMacrophageActivationByTCellsTestCase(unittest.TestCase):
    def setUp(self):
        self.event = MacrophageRegularActivationByTCellHelper(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageActivationByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.external_compartments, [T_CELL_HELPER])
        self.assertFalse(self.event.bacteria_compartment_destroy)


class InfectedMacrophageActivationByTCellsTestCase(unittest.TestCase):
    def setUp(self):
        self.event = MacrophageInfectedActivationByTCellHelper(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageActivationByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.external_compartments, [T_CELL_HELPER])
        self.assertEqual(self.event.bacteria_compartment_destroy, BACTERIA_INTRACELLULAR)


if __name__ == '__main__':
    unittest.main()
