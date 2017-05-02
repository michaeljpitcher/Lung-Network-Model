import unittest

from v8_ComMeN.ComMeN.TB.Events.PhagocytePrimesTCell import *


class TCellHelperActivationDendriticTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperActivationDendriticMature(0.1)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_from, T_CELL_NAIVE_HELPER)
        self.assertEqual(self.event.compartment_to, T_CELL_HELPER)
        self.assertItemsEqual(self.event.influencing_compartments, [DENDRITIC_CELL_MATURE])


class TCellHelperActivationMacrophageTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperActivationMacrophageInfected(0.1)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_from, T_CELL_NAIVE_HELPER)
        self.assertEqual(self.event.compartment_to, T_CELL_HELPER)
        self.assertItemsEqual(self.event.influencing_compartments, [MACROPHAGE_INFECTED])


class TCellCytotoxicActivationDendriticTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicActivationDendriticMature(0.1)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_from, T_CELL_NAIVE_CYTOTOXIC)
        self.assertEqual(self.event.compartment_to, T_CELL_CYTOTOXIC)
        self.assertItemsEqual(self.event.influencing_compartments, [DENDRITIC_CELL_MATURE])


class TCellCytotoxicActivationMacrophageTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicActivationMacrophageInfected(0.1)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_from, T_CELL_NAIVE_CYTOTOXIC)
        self.assertEqual(self.event.compartment_to, T_CELL_CYTOTOXIC)
        self.assertItemsEqual(self.event.influencing_compartments, [MACROPHAGE_INFECTED])


if __name__ == '__main__':
    unittest.main()
