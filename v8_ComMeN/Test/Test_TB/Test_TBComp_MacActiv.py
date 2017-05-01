import unittest

from v8_ComMeN.ComMeN.TB.Events.MacrophageActivation import *


class RegularMacrophageSpontaneousActivationTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageSpontaneousActivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Change))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertFalse(self.event.internals_to_destroy)


class InfectedMacrophageSpontaneousActivationTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageSpontaneousActivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Change))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.internals_to_destroy, [BACTERIA_INTRACELLULAR])


class RegularMacrophageActivationByCytokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageActivationByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.influencing_compartments, CYTOKINE_PRODUCING_COMPARTMENTS)
        self.assertFalse(self.event.internals_to_destroy)


class InfectedMacrophageActivationByCytokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageActivationByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.influencing_compartments, CYTOKINE_PRODUCING_COMPARTMENTS)
        self.assertItemsEqual(self.event.internals_to_destroy, [BACTERIA_INTRACELLULAR])


class ActivatedMacrophageSpontaneousDeactivationTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageSpontaneousDeactivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Change))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_REGULAR)


class ActivatedMacrophageDeactivationByLackOfCytokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageDeactivationByLackOfCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByLackOfOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_from, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.compartment_to, MACROPHAGE_REGULAR)
        self.assertItemsEqual(self.event.influencing_compartments, CYTOKINE_PRODUCING_COMPARTMENTS)


if __name__ == '__main__':
    unittest.main()
