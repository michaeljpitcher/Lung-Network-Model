import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.TCellRecruitment import *


class TCellRecruitmentBronchialRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellRecruitmentBronchialRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL)
        self.assertTrue(self.event.based_on_perfusion)


class TCellRecruitmentBronchialThroughInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellRecruitmentBronchialThroughInfection(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchialByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, T_CELL)
        self.assertTrue(self.event.based_on_perfusion)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])


class TCellRecruitmentLymphRegularTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellRecruitmentLymphRegular(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL)


class TCellRecruitmentLymphThroughInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellRecruitmentLymphThroughInfection(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymphByExternals))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])



if __name__ == '__main__':
    unittest.main()
