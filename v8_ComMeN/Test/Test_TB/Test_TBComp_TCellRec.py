import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.TCellRecruitment import *


class TCellHelperRecruitmentBronchialRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperRecruitmentBronchialRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_HELPER)
        self.assertTrue(self.event.based_on_perfusion)


class TCellHelperRecruitmentBronchialThroughInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperRecruitmentBronchialByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchialByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_HELPER)
        self.assertTrue(self.event.based_on_perfusion)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])


class TCellHelperRecruitmentLymphRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperRecruitmentLymphRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_HELPER)


class TCellHelperRecruitmentLymphThroughInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperRecruitmentLymphByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymphByExternals))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_HELPER)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])


class TCellCytotoxicRecruitmentBronchialRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicRecruitmentBronchialRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_CYTOTOXIC)
        self.assertTrue(self.event.based_on_perfusion)


class TCellCytotoxicRecruitmentBronchialThroughInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicRecruitmentBronchialByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchialByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL_CYTOTOXIC)
        self.assertTrue(self.event.based_on_perfusion)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])


class TCellCytotoxicRecruitmentLymphRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicRecruitmentLymphRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_CYTOTOXIC)


class TCellCytotoxicRecruitmentLymphThroughInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicRecruitmentLymphByCytokine(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymphByExternals))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_CYTOTOXIC)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])



if __name__ == '__main__':
    unittest.main()
