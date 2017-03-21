import unittest

from ....Models.Base.Events.Die import *
from ....Models.Base.Patch import *


class DieTestCase(unittest.TestCase):
    def setUp(self):
        self.keys=['a','b']
        self.event = Die(self.keys[0], 0.1)

    def test_initialise(self):
        self.assertEqual(self.event.class_to_die, self.keys[0])

    def test_increment_from_node(self):
        node = Patch(0, self.keys)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.subpopulations[self.keys[0]] = 2
        self.assertEqual(self.event.increment_from_node(node, None), 2)

    def test_update_network(self):
        node = Patch(0, self.keys)
        node.subpopulations[self.keys[0]] = 3
        self.event.update_network(node, None)
        self.assertEqual(node.subpopulations[self.keys[0]], 2)


class DieByOtherClassTestCase(unittest.TestCase):

    def setUp(self):
        self.keys = ['a','b']
        self.event = DieByOtherClass(self.keys[0], self.keys[1], 0.1)

    def test_initialise(self):
        self.assertEqual(self.event.class_which_kills, self.keys[1])

    def test_increment_from_node(self):
        node = Patch(0, self.keys)
        # Has neither
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        # Has a, no b
        node.subpopulations[self.keys[0]] = 1
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        # Has b, no a
        node.subpopulations[self.keys[0]] = 0
        node.subpopulations[self.keys[1]] = 1
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        # Has both
        node.subpopulations[self.keys[0]] = 2
        node.subpopulations[self.keys[1]] = 3
        self.assertEqual(self.event.increment_from_node(node, None), 6)


if __name__ == '__main__':
    unittest.main()
