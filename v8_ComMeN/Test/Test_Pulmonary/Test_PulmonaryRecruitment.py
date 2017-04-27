import unittest

from v8_ComMeN.ComMeN.Pulmonary.Events.PulmonaryRecruitment import *
from v8_ComMeN.ComMeN.Pulmonary.Node.BronchopulmonarySegment import *
from v8_ComMeN.ComMeN.Pulmonary.Node.LymphNode import *


class RecruitmentBronchialTestCase(unittest.TestCase):
    def setUp(self):
        self.comp_from = 'a'
        self.event = RecruitmentBronchial(None, 0.1, self.comp_from)
        self.event_not_perfusion = RecruitmentBronchial(0.1, self.comp_from, False)

    def test_initialise(self):
        self.assertTrue(self.event.based_on_perfusion)
        self.assertFalse(self.event_not_perfusion.based_on_perfusion)
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode])

    def test_increment_from_node(self):
        node = BronchopulmonarySegment(0, [self.comp_from], 0.0, 0.5, (8, 8))

        self.assertEqual(self.event.increment_state_variable_from_node(node, None), node.perfusion)
        self.assertEqual(self.event_not_perfusion.increment_state_variable_from_node(node, None), 1)


class RecruitmentBronchialByInfectionTestCase(unittest.TestCase):

    def setUp(self):
        self.comp = 'comp'
        self.infect_comps = ['inf_1', 'inf_2']
        self.event = RecruitmentBronchialByExternals(0.1, self.comp, self.infect_comps)
        self.event_not_perfusion = RecruitmentBronchialByExternals(0.1, self.comp, self.infect_comps, False)

    def test_increment_from_node(self):
        node = BronchopulmonarySegment(0, [self.comp] + self.infect_comps, 0.0, 0.5, (8, 8))
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)
        self.assertEqual(self.event_not_perfusion.increment_state_variable_from_node(node, None), 0)

        node.update_subpopulation(self.infect_comps[0], 2)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), node.perfusion * 2)
        self.assertEqual(self.event_not_perfusion.increment_state_variable_from_node(node, None), 1 * 2)

        node.update_subpopulation(self.infect_comps[1], 3)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), node.perfusion * (2 + 3))
        self.assertEqual(self.event_not_perfusion.increment_state_variable_from_node(node, None), 1 * (2 + 3))


class RecruitmentLymphTestCase(unittest.TestCase):

    def setUp(self):
        self.event = RecruitmentLymph(0.1, 'a')

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Create))
        self.assertItemsEqual(self.event.node_types, [LymphNode])


class RecruitmentLymphByInfectionTestCase(unittest.TestCase):

    def setUp(self):
        self.comp = 'comp'
        self.infect_comps = ['inf_1', 'inf_2']
        self.event = RecruitmentLymphByExternals(0.1, self.comp, self.infect_comps)

    def test_increment_from_node(self):
        node = LymphNode(0, [self.comp] + self.infect_comps, (8, 8))
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)

        node.update_subpopulation(self.infect_comps[0], 2)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 2)

        node.update_subpopulation(self.infect_comps[1], 3)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), (2 + 3))


if __name__ == '__main__':
    unittest.main()
