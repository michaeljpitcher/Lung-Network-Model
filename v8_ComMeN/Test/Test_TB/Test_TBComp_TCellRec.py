import unittest

from v8_ComMeN.ComMeN.TB.Events.TCellRecruitment import *


class TCellHelperRecruitmentBronchialRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveHelperRecruitmentBronchialRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_HELPER)
        self.assertTrue(self.event.based_on_perfusion)


class TCellHelperRecruitmentLymphRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveHelperRecruitmentLymphRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_HELPER)


class TCellCytotoxicRecruitmentBronchialRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicRecruitmentBronchialRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_CYTOTOXIC)
        self.assertTrue(self.event.based_on_perfusion)


class TCellCytotoxicRecruitmentLymphRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicRecruitmentLymphRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_CYTOTOXIC)



if __name__ == '__main__':
    unittest.main()
