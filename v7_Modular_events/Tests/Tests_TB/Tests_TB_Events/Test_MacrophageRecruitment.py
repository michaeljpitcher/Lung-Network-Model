import unittest

from v7_Modular_events.Models.TB.TBEvents.MacrophageRecruitment import *
from v7_Modular_events.Models.TB.TBClasses import *
from v7_Modular_events.Models.PulmonaryAnatomy.BronchopulmonarySegment import *


class MacrophageRecruitmentRegularBPSTestCase(unittest.TestCase):

    def setUp(self):
        self.event_mac_not_defined = MacrophageRecruitmentRegularBPS(0.1)
        self.event_mac_defined = MacrophageRecruitmentRegularBPS(0.1, macrophage_type=MACROPHAGE)

    def test_initialise(self):
        self.assertEqual(self.event_mac_not_defined.class_to_create, MACROPHAGE_REGULAR)
        self.assertEqual(self.event_mac_defined.class_to_create, MACROPHAGE)


class MacrophageRecruitmentThroughInfectionBPSTestCase(unittest.TestCase):

    def setUp(self):
        self.event_mac_not_defined = MacrophageRecruitmentThroughInfectionBPS(0.1)
        self.event_mac_defined = MacrophageRecruitmentThroughInfectionBPS(0.1, macrophage_type=MACROPHAGE)

    def test_initialise(self):
        self.assertEqual(self.event_mac_not_defined.class_to_create, MACROPHAGE_REGULAR)
        self.assertEqual(self.event_mac_defined.class_to_create, MACROPHAGE)

    def test_increment_from_node(self):
        node = BronchopulmonarySegment(0, [MACROPHAGE_INFECTED], (5,5))
        node.update(MACROPHAGE_INFECTED, 12)

        self.assertEqual(self.event_mac_not_defined.increment_from_node(node, None), 12*node.perfusion)


class MacrophageRecruitmentRegularLymphTestCase(unittest.TestCase):

    def setUp(self):
        self.event_mac_not_defined = MacrophageRecruitmentRegularLymph(0.1)
        self.event_mac_defined = MacrophageRecruitmentRegularLymph(0.1, macrophage_type=MACROPHAGE)

    def test_initialise(self):
        self.assertEqual(self.event_mac_not_defined.class_to_create, MACROPHAGE_REGULAR)
        self.assertEqual(self.event_mac_defined.class_to_create, MACROPHAGE)


class MacrophageRecruitmentThroughInfectionLymphTestCase(unittest.TestCase):

    def setUp(self):
        self.event_mac_not_defined = MacrophageRecruitmentThroughInfectionLymph(0.1)
        self.event_mac_defined = MacrophageRecruitmentThroughInfectionLymph(0.1, macrophage_type=MACROPHAGE)

    def test_initialise(self):
        self.assertEqual(self.event_mac_not_defined.class_to_create, MACROPHAGE_REGULAR)
        self.assertEqual(self.event_mac_defined.class_to_create, MACROPHAGE)

    def test_increment_from_node(self):
        node = BronchopulmonarySegment(0, [MACROPHAGE_INFECTED], (5,5))
        node.update(MACROPHAGE_INFECTED, 12)

        self.assertEqual(self.event_mac_not_defined.increment_from_node(node, None), 12)


if __name__ == '__main__':
    unittest.main()
