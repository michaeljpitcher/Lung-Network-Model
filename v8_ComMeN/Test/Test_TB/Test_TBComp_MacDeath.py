import unittest

from v8_ComMeN.ComMeN.TB.Events.MacrophageDeath import *


class RegularMacrophageSpontaneousDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageSpontaneousDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_REGULAR)
        self.assertFalse(self.event.internals_to_destroy)
        self.assertFalse(self.event.internals_changed)


class InfectedMacrophageSpontaneousDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageSpontaneousDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertFalse(self.event.internals_to_destroy)
        self.assertItemsEqual(self.event.internals_changed, [(BACTERIA_INTRACELLULAR, BACTERIA_SLOW)])


class ActivatedMacrophageSpontaneousDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageSpontaneousDeath(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Destroy))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_ACTIVATED)
        self.assertFalse(self.event.internals_to_destroy)
        self.assertFalse(self.event.internals_changed)


class InfectedMacrophageDeathByIntracellularBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageDeathByIntracellularBacteria(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, DestroyByOtherCompartments))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_destroyed, MACROPHAGE_INFECTED)
        self.assertFalse(self.event.internals_to_destroy)
        self.assertItemsEqual(self.event.internals_changed, [(BACTERIA_INTRACELLULAR, BACTERIA_SLOW)])
        self.assertItemsEqual(self.event.influencing_compartments, [BACTERIA_INTRACELLULAR])
        self.assertFalse(self.event.influencers_changed)
        self.assertFalse(self.event.influencers_to_destroy)


if __name__ == '__main__':
    unittest.main()
