import unittest

from ....Models.PulmonaryAnatomy.PulmonaryEvents.PulmonaryRecruitment import *
from ....Models.PulmonaryAnatomy.BronchopulmonarySegment import *
from ....Models.PulmonaryAnatomy.LymphNode import *


class ChangeByOxygenTestCase(unittest.TestCase):

    def setUp(self):
        self.class_recruited = 'a'
        self.event = RecruitmentThroughBloodBPS(self.class_recruited, 0.1)

    def test_increment_from_node(self):
        node1 = BronchopulmonarySegment(0, [self.class_recruited], (5, 5))
        node1.perfusion = 0.2
        self.assertEqual(self.event.increment_from_node(node1, None), 0.2)
        node1.perfusion = 0.5
        self.assertEqual(self.event.increment_from_node(node1, None), 0.5)

        node2 = LymphNode(1, [self.class_recruited], (6, 6))
        self.assertEqual(self.event.increment_from_node(node2, None), 0.0)
