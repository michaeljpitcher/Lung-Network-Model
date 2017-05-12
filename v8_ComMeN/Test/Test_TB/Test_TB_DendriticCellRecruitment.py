import unittest

from v8_ComMeN.ComMeN.TBIndividual.Events.DendriticCellRecruitment import *


class DendriticImmatureRecruitmentBronchialTestCase(unittest.TestCase):
    def setUp(self):
        self.event = DendriticImmatureRecruitmentBronchial(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentBronchial))
        self.assertEqual(self.event.compartment_created, DENDRITIC_CELL_IMMATURE)
        self.assertTrue(self.event.based_on_perfusion)


class DendriticImmatureRecruitmentLymphTestCase(unittest.TestCase):
    def setUp(self):
        self.event = DendriticImmatureRecruitmentLymph(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, RecruitmentLymph))
        self.assertEqual(self.event.compartment_created, DENDRITIC_CELL_IMMATURE)


if __name__ == '__main__':
    unittest.main()
