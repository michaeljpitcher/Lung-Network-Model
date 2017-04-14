import unittest
from v8_ComMeN.ComMeN.Base.Events.Creation import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class CreationTestCase(unittest.TestCase):
    def setUp(self):
        self.probability = 0.1
        self.compartment = 'a'
        self.event = Create(None, self.probability, self.compartment)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_created, self.compartment)

    def test_increment_from_node(self):
        self.assertEqual(self.event.increment_from_node(None, None), 1)

    def test_update_node(self):
        node = Patch(0, [self.compartment])
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.compartment], 1)


class ReplicationTestCase(unittest.TestCase):
    def setUp(self):
        self.probability = 0.1
        self.compartment = 'a'
        self.event = Replication(None, self.probability, self.compartment)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_created, self.compartment)

    def test_increment_from_node(self):
        node = Patch(0, [self.compartment])
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.compartment, 12)
        self.assertEqual(self.event.increment_from_node(node, None), 12)


if __name__ == '__main__':
    unittest.main()
