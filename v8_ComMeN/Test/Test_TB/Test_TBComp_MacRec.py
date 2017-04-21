import unittest

from v8_ComMeN.ComMeN.TB.EventsWithCompartments.MacrophageRecruitment import *


class RegularMacrophageRecruitmentBronchialTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageRecruitmentBronchial(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, MACROPHAGE_REGULAR)
        self.assertTrue(self.event.based_on_perfusion)


class RegularMacrophageRecruitmentBronchialByInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageRecruitmentBronchialByInfection(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchialByExternals))
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])
        self.assertEqual(self.event.compartment_created, MACROPHAGE_REGULAR)
        self.assertTrue(self.event.based_on_perfusion)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])


class RegularMacrophageRecruitmentLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageRecruitmentLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, MACROPHAGE_REGULAR)


class RegularMacrophageRecruitmentLymphByInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.event = RegularMacrophageRecruitmentLymphByInfection(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymphByExternals))
        self.assertItemsEqual(self.event.node_types, [LymphNode])
        self.assertEqual(self.event.compartment_created, MACROPHAGE_REGULAR)
        self.assertItemsEqual(self.event.external_compartments, [MACROPHAGE_INFECTED])


if __name__ == '__main__':
    unittest.main()
