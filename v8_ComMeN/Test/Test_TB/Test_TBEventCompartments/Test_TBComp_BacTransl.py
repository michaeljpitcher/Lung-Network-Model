import unittest
from v8_ComMeN.ComMeN.TB.EventsWithCompartments.BacteriaTranslocate import *


class BacteriaTranslocateBronchusFastTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaTranslocateBronchusFast(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertEqual(self.event.translocate_compartment, BACTERIA_FAST)
        self.assertTrue(self.event.edge_choice_based_on_weight)


class BacteriaTranslocateBronchusSlowTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaTranslocateBronchusSlow(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBronchus))
        self.assertEqual(self.event.translocate_compartment, BACTERIA_SLOW)
        self.assertTrue(self.event.edge_choice_based_on_weight)


class BacteriaTranslocateLymphFastTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaTranslocateLymphFast(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertEqual(self.event.translocate_compartment, BACTERIA_FAST)
        self.assertTrue(self.event.direction_only)


class BacteriaTranslocateLymphSlowTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaTranslocateLymphSlow(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertEqual(self.event.translocate_compartment, BACTERIA_SLOW)
        self.assertTrue(self.event.direction_only)


class BacteriaTranslocateBloodFastTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaTranslocateHaematogenousFast(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertEqual(self.event.translocate_compartment, BACTERIA_FAST)
        self.assertTrue(self.event.direction_only)


class BacteriaTranslocateBloodSlowTestCase(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaTranslocateHaematogenousSlow(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateBlood))
        self.assertEqual(self.event.translocate_compartment, BACTERIA_SLOW)
        self.assertTrue(self.event.direction_only)


if __name__ == '__main__':
    unittest.main()
