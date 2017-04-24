import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.MacrophageActivation import *


class RegularMacrophageSpontaneousActivationTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageSpontaneousActivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageActivation))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertFalse(self.event.bacteria_compartment_destroy)


class InfectedMacrophageSpontaneousActivationTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageSpontaneousActivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageActivation))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.bacteria_compartment_destroy, BACTERIA_INTRACELLULAR)


class RegularMacrophageActivationByChemokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageActivationByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageActivationByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])
        self.assertFalse(self.event.bacteria_compartment_destroy)


class InfectedMacrophageActivationByChemokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageActivationByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageActivationByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])
        self.assertEqual(self.event.bacteria_compartment_destroy, BACTERIA_INTRACELLULAR)


class ActivatedMacrophageSpontaneousDeactivationTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageSpontaneousDeactivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Change))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_REGULAR)


class ActivatedMacrophageDeactivationByLackOfInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageDeactivationByLackOfCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, MacrophageDeactivationByLackOfExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_REGULAR)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])


if __name__ == '__main__':
    unittest.main()
