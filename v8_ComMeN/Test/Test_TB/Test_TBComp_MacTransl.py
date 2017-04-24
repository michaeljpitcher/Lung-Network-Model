import unittest

from v8_ComMeN.ComMeN.TB.Events.MacrophageTranslocate import *


class RegularMacrophageTranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageTranslocateBronchus(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_REGULAR)
        self.assertTrue(self.event.edge_choice_based_on_weight)
        self.assertFalse(self.event.internal_compartments)


class InfectedMacrophageTranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageTranslocateBronchus(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_INFECTED)
        self.assertTrue(self.event.edge_choice_based_on_weight)
        self.assertItemsEqual(self.event.internal_compartments, [BACTERIA_INTRACELLULAR])


class ActivatedMacrophageTranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageTranslocateBronchus(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_ACTIVATED)
        self.assertTrue(self.event.edge_choice_based_on_weight)
        self.assertFalse(self.event.internal_compartments)


class RegularMacrophageTranslocateLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageTranslocateLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_REGULAR)
        self.assertTrue(self.event.flow_based)
        self.assertTrue(self.event.direction_only)
        self.assertFalse(self.event.internal_compartments)


class InfectedMacrophageTranslocateLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageTranslocateLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_INFECTED)
        self.assertTrue(self.event.flow_based)
        self.assertTrue(self.event.direction_only)
        self.assertItemsEqual(self.event.internal_compartments, [BACTERIA_INTRACELLULAR])


class ActivatedMacrophageTranslocateLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageTranslocateLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_ACTIVATED)
        self.assertTrue(self.event.flow_based)
        self.assertTrue(self.event.direction_only)
        self.assertFalse(self.event.internal_compartments)


class RegularMacrophageTranslocateBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageTranslocateBlood(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_REGULAR)
        self.assertTrue(self.event.direction_only)
        self.assertFalse(self.event.internal_compartments)


class InfectedMacrophageTranslocateBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageTranslocateBlood(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_INFECTED)
        self.assertTrue(self.event.direction_only)
        self.assertItemsEqual(self.event.internal_compartments, [BACTERIA_INTRACELLULAR])


class ActivatedMacrophageTranslocateBloodTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageTranslocateBlood(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.translocate_compartment, MACROPHAGE_ACTIVATED)
        self.assertTrue(self.event.direction_only)
        self.assertFalse(self.event.internal_compartments)


if __name__ == '__main__':
    unittest.main()
