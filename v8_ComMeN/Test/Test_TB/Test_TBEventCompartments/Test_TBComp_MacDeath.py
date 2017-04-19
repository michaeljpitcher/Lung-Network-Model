import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.MacrophageDeath import *


class RegularMacrophageSpontaneousDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageSpontaneousDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageDeath))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_REGULAR)
        self.assertFalse(self.event.internal_bacteria_compartment)
        self.assertFalse(self.event.bacteria_release_compartment_to)


class InfectedMacrophageSpontaneousDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageSpontaneousDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageDeath))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.internal_bacteria_compartment, BACTERIA_INTRACELLULAR)
        self.assertEqual(self.event.bacteria_release_compartment_to, BACTERIA_SLOW)


class ActivatedMacrophageSpontaneousDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageSpontaneousDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageDeath))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_ACTIVATED)
        self.assertFalse(self.event.internal_bacteria_compartment)
        self.assertFalse(self.event.bacteria_release_compartment_to)


class InfectedMacrophageDeathByTCellTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageDeathByTCell(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageDeathByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.internal_bacteria_compartment, BACTERIA_INTRACELLULAR)
        self.assertFalse(self.event.bacteria_release_compartment_to)
        self.assertItemsEqual(self.event.external_compartments, [T_CELL])
        self.assertItemsEqual(self.event.externals_to_destroy, [T_CELL])


class InfectedMacrophageDeathByIntracellularBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageDeathByIntracellularBacteria(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageDeathByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.internal_bacteria_compartment, BACTERIA_INTRACELLULAR)
        self.assertEqual(self.event.bacteria_release_compartment_to, BACTERIA_SLOW)
        self.assertItemsEqual(self.event.external_compartments, [BACTERIA_INTRACELLULAR])
        self.assertFalse(self.event.externals_to_destroy)


if __name__ == '__main__':
    unittest.main()
