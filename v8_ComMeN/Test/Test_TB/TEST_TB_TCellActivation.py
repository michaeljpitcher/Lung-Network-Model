import unittest

from v8_ComMeN.ComMeN.TB.Events.TCellActivation import *


class TCellActivationHelperTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellActivationHelper(0.1)

    def test_something(self):
        self.assertEqual(self.event.compartment_from, T_CELL_NAIVE_HELPER)
        self.assertEqual(self.event.compartment_to, T_CELL_HELPER)
        self.assertItemsEqual(self.event.influencing_compartments, [MACROPHAGE_INFECTED])


class TCellActivationCytotoxicTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellActivationCytotoxic(0.1)

    def test_something(self):
        self.assertEqual(self.event.compartment_from, T_CELL_NAIVE_CYTOTOXIC)
        self.assertEqual(self.event.compartment_to, T_CELL_CYTOTOXIC)
        self.assertItemsEqual(self.event.influencing_compartments, [MACROPHAGE_INFECTED])


if __name__ == '__main__':
    unittest.main()
