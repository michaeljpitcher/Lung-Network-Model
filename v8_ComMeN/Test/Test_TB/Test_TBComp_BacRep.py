import unittest
from v8_ComMeN.ComMeN.TB.Events.BacteriaReplication import *


class BacteriaReplicationFastTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaReplicationFast(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Replication))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_created, BACTERIA_FAST)


class BacteriaReplicationSlowTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaReplicationSlow(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Replication))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_created, BACTERIA_SLOW)


class BacteriaReplicationIntracellularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaReplicationIntracellular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Replication))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_created, BACTERIA_INTRACELLULAR)



if __name__ == '__main__':
    unittest.main()
