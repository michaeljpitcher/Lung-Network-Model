import unittest

from ....Models.PulmonaryAnatomy.PulmonaryEvents.PulmonaryChange import *
from ....Models.PulmonaryAnatomy.BronchopulmonarySegment import *
from ....Models.PulmonaryAnatomy.LymphNode import *


class ChangeByOxygenTestCase(unittest.TestCase):

    def setUp(self):
        self.class_from = 'a'
        self.class_to = 'b'
        self.event_high = ChangeByOxygenBPS(self.class_from, self.class_to, 0.1, True)
        self.event_low = ChangeByOxygenBPS(self.class_from, self.class_to, 0.1, False)

    def test_initialise(self):
        self.assertTrue(self.event_high.oxygen_high)
        self.assertFalse(self.event_low.oxygen_high)

    def test_increment_from_node(self):
        node = BronchopulmonarySegment(0, [self.class_from, self.class_to], (5, 10))
        self.assertEqual(node.oxygen_tension, 2.0)
        # No class from
        self.assertEqual(self.event_high.increment_from_node(node, None), 0)
        self.assertEqual(self.event_low.increment_from_node(node, None), 0)
        # Has class from
        node.subpopulations[self.class_from] = 10
        self.assertEqual(self.event_high.increment_from_node(node, None), 10.0 * 2.0)
        self.assertEqual(self.event_low.increment_from_node(node, None), 10.0 * (1/2.0))
        # Wrong node type
        node = LymphNode(1, [self.class_from, self.class_to], (6,6))
        node.subpopulations[self.class_from] = 10
        self.assertEqual(self.event_high.increment_from_node(node, None), 0.0)
        self.assertEqual(self.event_low.increment_from_node(node, None), 0.0)


