import unittest

from v8_ComMeN.ComMeN.Pulmonary.Events.PulmonaryRecruitment import *
from v8_ComMeN.ComMeN.Pulmonary.Node.BronchopulmonarySegment import *


class RecruitmentBronchialTestCase(unittest.TestCase):
    def setUp(self):
        self.comp_from = 'a'
        self.event = RecruitmentBronchial(0.1, self.comp_from)
        self.event_not_perfusion = RecruitmentBronchial(0.1, self.comp_from, False)

    def test_initialise(self):
        self.assertTrue(self.event.based_on_perfusion)
        self.assertFalse(self.event_not_perfusion.based_on_perfusion)

    def test_increment_from_node(self):
        node = BronchopulmonarySegment(0, [self.comp_from], 0.0, 0.5, (8, 8))

        self.assertEqual(self.event.increment_from_node(node, None), node.perfusion)
        self.assertEqual(self.event_not_perfusion.increment_from_node(node, None), 1)


class RecruitmentLymphTestCase(unittest.TestCase):

    def setUp(self):
        self.event = RecruitmentLymph(0.1, 'a')

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Create))


if __name__ == '__main__':
    unittest.main()
