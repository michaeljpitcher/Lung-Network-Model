import unittest

from v7_Modular_events.Models.Base.Events.Create import *
from v7_Modular_events.Models.Base.Patch import *


class NodeType1(Patch):
    def __init__(self, keys):
        Patch.__init__(self, 0, keys)


class NodeType2(Patch):
    def __init__(self, keys):
        Patch.__init__(self, 0, keys)


class CreateTestCase(unittest.TestCase):
    def setUp(self):
        self.keys = ['a']
        self.event = Create(self.keys[0], 0.1)

    def test_initialise(self):
        self.assertEqual(self.event.class_to_create, self.keys[0])

    def test_increment_from_node(self):
        self.assertEqual(self.event.increment_from_node(None, None), 1)

    def test_update_network(self):
        node = Patch(0, self.keys)
        self.assertEqual(node.subpopulations[self.keys[0]], 0)

        self.event.update_network(node, None)
        self.assertEqual(node.subpopulations[self.keys[0]], 1)

class CreateAtNodeTypeTestCase(unittest.TestCase):

    def setUp(self):
        self.keys = ['a']

        self.node1 = NodeType1(self.keys)
        self.node2 = NodeType2(self.keys)
        self.event = CreateAtNodeType(self.keys[0], NodeType1, 0.1)

    def test_initialise(self):
        self.assertEqual(self.event.node_type, NodeType1)

    def test_increment_from_node(self):
        # Correct type
        self.assertEqual(self.event.increment_from_node(self.node1, None), 1)
        # Incorrect type
        self.assertEqual(self.event.increment_from_node(self.node2, None), 0)


class ReplicateTestCase(unittest.TestCase):

    def setUp(self):
        self.keys = ['a']
        self.event = Replication(self.keys[0], 0.1)

    def test_increment_from_node(self):
        node = Patch(0, self.keys)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.subpopulations[self.keys[0]] = 15
        self.assertEqual(self.event.increment_from_node(node, None), 15)


if __name__ == '__main__':
    unittest.main()
