import unittest

from ....Models.Base.Events.Change import *
from ....Models.Base.Patch import *


class ChangeTestCase(unittest.TestCase):
    def setUp(self):
        self.keys = ['a', 'b']
        self.class_from = self.keys[0]
        self.class_to = self.keys[1]
        self.probability = 0.1
        self.event = Change(self.class_from, self.class_to, self.probability)

    def test_initialise(self):
        self.assertEqual(self.event.class_from, self.class_from)
        self.assertEqual(self.event.class_to, self.class_to)

    def test_increment_from_node(self):
        node = Patch(0, self.keys)
        node.update(self.event.class_from, 1)
        self.assertEqual(self.event.increment_from_node(node, None), 1)
        node.update(self.event.class_from, 13)
        self.assertEqual(self.event.increment_from_node(node, None), 14)
        node2 = Patch(2, self.keys)
        node2.update(self.event.class_to, 13)
        self.assertEqual(self.event.increment_from_node(node2, None), 0)

    def test_update_network(self):
        node = Patch(0, self.keys)
        node.update(self.event.class_from, 1)
        self.event.update_network(node, None)
        self.assertEqual(node.subpopulations[self.class_from], 0)
        self.assertEqual(node.subpopulations[self.class_to], 1)

class ChangeThroughOtherClassTestCase(unittest.TestCase):

    def setUp(self):
        self.keys = ['a', 'b', 'c']
        self.class_from = self.keys[0]
        self.class_to = self.keys[1]
        self.influencing_class = self.keys[2]
        self.probability = 0.1
        self.event = ChangeThroughOtherClass(self.class_from, self.class_to, self.influencing_class, self.probability)

    def test_initialise(self):
        self.assertEqual(self.event.influencing_class, self.influencing_class)

    def test_increment_from_node(self):
        node = Patch(0, self.keys)
        # Has a, no c
        node.subpopulations[self.keys[0]] = 1
        node.subpopulations[self.keys[2]] = 0
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        # Has c, no a
        node.subpopulations[self.keys[0]] = 0
        node.subpopulations[self.keys[2]] = 1
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        # Has both a and c
        node.subpopulations[self.keys[0]] = 3
        node.subpopulations[self.keys[2]] = 4
        self.assertEqual(self.event.increment_from_node(node, None), 12)
        # Has neither a nor c
        node.subpopulations[self.keys[0]] = 0
        node.subpopulations[self.keys[2]] = 0
        self.assertEqual(self.event.increment_from_node(node, None), 0)


if __name__ == '__main__':
    unittest.main()
