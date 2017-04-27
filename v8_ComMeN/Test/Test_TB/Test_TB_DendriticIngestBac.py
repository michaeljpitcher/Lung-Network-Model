import unittest

from v8_ComMeN.ComMeN.TB.Events.DendriticCellIngestBacteria import *


class ImmatureDendriticIngestFastBacteriaMaturateTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ImmatureDendriticIngestFastBacteriaMaturate(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.phagocyte_compartment, DENDRITIC_CELL_IMMATURE)
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_FAST)
        self.assertEqual(self.event.compartment_to_change_phagocyte_to, DENDRITIC_CELL_MATURE)
        self.assertFalse(self.event.compartment_to_change_ingested_to)


class ImmatureDendriticIngestSlowBacteriaMaturateTestCase(unittest.TestCase):
    def setUp(self):
        self.event = ImmatureDendriticIngestSlowBacteriaMaturate(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Phagocytosis))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment, LymphNode])
        self.assertEqual(self.event.phagocyte_compartment, DENDRITIC_CELL_IMMATURE)
        self.assertEqual(self.event.compartment_to_ingest, BACTERIA_SLOW)
        self.assertEqual(self.event.compartment_to_change_phagocyte_to, DENDRITIC_CELL_MATURE)
        self.assertFalse(self.event.compartment_to_change_ingested_to)



if __name__ == '__main__':
    unittest.main()
