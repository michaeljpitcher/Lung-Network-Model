import unittest

from v7_Modular_events.Models.TB.TBClasses import *
from v7_Modular_events.Models.TB.TBEvents.TCellRecruitment import *


class TCellRecruitedRegularLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event_not_defined = TCellRecruitedRegularLymph(0.1)
        self.event_defined = TCellRecruitedRegularLymph(0.1, T_CELL_CYTOTOXIC)

    def test_initialise(self):
        self.assertEqual(self.event_not_defined.class_to_create, T_CELL)
        self.assertEqual(self.event_defined.class_to_create, T_CELL_CYTOTOXIC)
        self.assertTrue(isinstance(self.event_not_defined, CreateAtNodeType))


class TCellRecruitedThroughInfectionLymphTestCase(unittest.TestCase):

    def setUp(self):
        self.event_not_defined = TCellRecruitedThroughInfectionLymph(0.1)
        self.event_defined = TCellRecruitedThroughInfectionLymph(0.1, T_CELL_CYTOTOXIC)

    def test_initialise(self):
        self.assertEqual(self.event_not_defined.class_to_create, T_CELL)
        self.assertEqual(self.event_defined.class_to_create, T_CELL_CYTOTOXIC)
        self.assertTrue(isinstance(self.event_not_defined, CreateAtNodeType))

    def test_increment_from_node(self):
        node = LymphNode(0, [MACROPHAGE_INFECTED, T_CELL], (5,5))
        self.assertEqual(self.event_not_defined.increment_from_node(node, None), 0)
        node.update(MACROPHAGE_INFECTED, 10)
        self.assertEqual(self.event_not_defined.increment_from_node(node, None), 10)

        node = BronchopulmonarySegment(0, [MACROPHAGE_INFECTED, T_CELL], (5,5))
        node.update(MACROPHAGE_INFECTED, 10)
        self.assertEqual(self.event_not_defined.increment_from_node(node, None), 0)




if __name__ == '__main__':
    unittest.main()
