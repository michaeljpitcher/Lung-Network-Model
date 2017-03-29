import unittest

from v7_Modular_events.Models.TB.TBEvents.MacrophageActivation import *


class MacrophageActivationTestCase(unittest.TestCase):

    def setUp(self):
        self.event = MacrophageActivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Change))
        self.assertEqual(self.event.class_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.class_to, MACROPHAGE_ACTIVATED)


class MacrophageActivationThroughInfectionTestCase(unittest.TestCase):

    def setUp(self):
        self.event = MacrophageActivationThroughInfection(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeThroughOtherClass))
        self.assertEqual(self.event.class_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.class_to, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.influencing_class, MACROPHAGE_INFECTED)


class MacrophageActivationThroughTCellTestCase(unittest.TestCase):

    def setUp(self):
        self.event = MacrophageActivationThroughTCell(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeThroughOtherClass))
        self.assertEqual(self.event.class_from, MACROPHAGE_REGULAR)
        self.assertEqual(self.event.class_to, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.influencing_class, T_CELL)


class MacrophageDeactivationTestCase(unittest.TestCase):

    def setUp(self):
        self.event = MacrophageDeactivation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Change))
        self.assertEqual(self.event.class_from, MACROPHAGE_ACTIVATED)
        self.assertEqual(self.event.class_to, MACROPHAGE_REGULAR)