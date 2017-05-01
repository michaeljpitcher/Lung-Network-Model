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


class TCellNaiveHelperRecruitmentBronchialByCytokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveHelperRecruitmentBronchialByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchialByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_HELPER)
        self.assertItemsEqual(self.event.external_compartments, CYTOKINE_PRODUCING_COMPARTMENTS)
        self.assertTrue(self.event.based_on_perfusion)


class TCellNaiveHelperRecruitmentLymphRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveHelperRecruitmentLymphRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_HELPER)


class TCellNaiveHelperRecruitmentLymphByCytokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveHelperRecruitmentLymphByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymphByExternals))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertItemsEqual(self.event.external_compartments, CYTOKINE_PRODUCING_COMPARTMENTS)
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_HELPER)


class TCellCytotoxicRecruitmentBronchialRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveCytotoxicRecruitmentBronchialRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_CYTOTOXIC)
        self.assertTrue(self.event.based_on_perfusion)


class TCellNaiveCytotoxicRecruitmentBronchialByCytokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveCytotoxicRecruitmentBronchialByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchialByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_CYTOTOXIC)
        self.assertItemsEqual(self.event.external_compartments, CYTOKINE_PRODUCING_COMPARTMENTS)
        self.assertTrue(self.event.based_on_perfusion)


class TCellCytotoxicRecruitmentLymphRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveCytotoxicRecruitmentLymphRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_CYTOTOXIC)


class TCellNaiveCytotoxicRecruitmentLymphByCytokineTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellNaiveCytotoxicRecruitmentLymphByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymphByExternals))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_NAIVE_CYTOTOXIC)
        self.assertItemsEqual(self.event.external_compartments, CYTOKINE_PRODUCING_COMPARTMENTS)



if __name__ == '__main__':
    unittest.main()
