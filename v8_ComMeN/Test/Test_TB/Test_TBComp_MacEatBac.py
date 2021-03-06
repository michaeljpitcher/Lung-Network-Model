import unittest

from v8_ComMeN.ComMeN.TBIndividual.Events.MacrophageIngestBacteria import *


class RestingMacrophageIngestFastBacteriaRetainTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageIngestFastBacteriaRetain(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_FAST)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_REGULAR)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_to_change_phagocyte_to, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to_change_ingested_to, BACTERIA_INTRACELLULAR)


class RestingMacrophageIngestFastBacteriaDestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageIngestFastBacteriaDestroy(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_FAST)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_REGULAR)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertFalse(self.event.compartment_to_change_ingested_to)


class RestingMacrophageIngestSlowBacteriaRetainTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageIngestSlowBacteriaRetain(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_SLOW)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_REGULAR)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.compartment_to_change_phagocyte_to, MACROPHAGE_INFECTED)
        self.assertEqual(self.event.compartment_to_change_ingested_to, BACTERIA_INTRACELLULAR)


class RestingMacrophageIngestSlowBacteriaDestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageIngestSlowBacteriaDestroy(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_SLOW)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_REGULAR)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertFalse(self.event.compartment_to_change_ingested_to)


class InfectedMacrophageIngestFastBacteriaRetainTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageIngestFastBacteriaRetain(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_FAST)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_INFECTED)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertEqual(self.event.compartment_to_change_ingested_to, BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestFastBacteriaDestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageIngestFastBacteriaDestroy(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_FAST)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_INFECTED)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertFalse(self.event.compartment_to_change_ingested_to)


class InfectedMacrophageIngestSlowBacteriaRetainTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageIngestSlowBacteriaRetain(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_SLOW)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_INFECTED)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertEqual(self.event.compartment_to_change_ingested_to, BACTERIA_INTRACELLULAR)


class InfectedMacrophageIngestSlowBacteriaDestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageIngestSlowBacteriaDestroy(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_SLOW)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_INFECTED)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertFalse(self.event.compartment_to_change_ingested_to)


class ActivatedMacrophageIngestFastBacteriaDestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageIngestFastBacteriaDestroy(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_FAST)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertFalse(self.event.compartment_to_change_ingested_to)


class ActivatedMacrophageIngestSlowBacteriaDestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ActivatedMacrophageIngestSlowBacteriaDestroy(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_SLOW)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_ACTIVATED)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertFalse(self.event.compartment_to_change_phagocyte_to)
        self.assertFalse(self.event.compartment_to_change_ingested_to)


class InfectedMacrophageDestroyInternalBacteriaTestCase(unittest.TestCase):
    def setUp(self):
        self.event = InfectedMacrophageDestroyInternalBacteria(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, PhagocyteDestroyInternals))
        self.assertEqual(self.event.compartment_destroyed, BACTERIA_INTRACELLULAR)
        self.assertEqual(self.event.phagocyte_compartment, MACROPHAGE_INFECTED)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.healed_phagocyte_compartment, MACROPHAGE_REGULAR)


if __name__ == '__main__':
    unittest.main()
