import unittest
from v8_ComMeN.ComMeN.TBIndividual.Events.BacteriaChange import *


class BacteriaFastToSlow(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaChangeByOxygenFastToSlow(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOxygen))
        self.assertEqual(self.event.compartment_from, BACTERIA_FAST)
        self.assertEqual(self.event.compartment_to, BACTERIA_SLOW)
        self.assertFalse(self.event.oxygen_high_to_change)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])

    def test_increment_from_node(self):
        btn_1 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.2, 0.1, (0, 0))
        btn_2 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.9, 0.1, (0, 0))
        self.assertTrue(btn_2.oxygen_tension > btn_1.oxygen_tension)

        self.assertEqual(self.event.increment_state_variable_from_node(btn_1, None), 0)

        btn_1.update_subpopulation(BACTERIA_FAST, 10)
        btn_2.update_subpopulation(BACTERIA_FAST, 10)
        # 2 has more oxygen, so should be more likely to change at 1
        self.assertTrue(self.event.increment_state_variable_from_node(btn_1, None) >
                        self.event.increment_state_variable_from_node(btn_2, None))

        bps_1 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.2, 0.1, (0, 0))
        bps_2 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.9, 0.1, (0, 0))
        self.assertTrue(bps_2.oxygen_tension > bps_1.oxygen_tension)

        self.assertEqual(self.event.increment_state_variable_from_node(bps_1, None), 0)

        bps_1.update_subpopulation(BACTERIA_FAST, 10)
        bps_2.update_subpopulation(BACTERIA_FAST, 10)
        # 2 has more oxygen, so should be more likely to change at 1
        self.assertTrue(self.event.increment_state_variable_from_node(bps_1, None) >
                        self.event.increment_state_variable_from_node(bps_2, None))

    def test_update_node(self):
        btn_1 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.2, 0.1, (0, 0))
        btn_1.update_subpopulation(BACTERIA_FAST, 10)
        self.event.update_node(btn_1, None)
        self.assertEqual(btn_1.subpopulations[BACTERIA_FAST], 9)
        self.assertEqual(btn_1.subpopulations[BACTERIA_SLOW], 1)


class BacteriaSlowToFast(unittest.TestCase):
    def setUp(self):
        self.event = BacteriaChangeByOxygenSlowToFast(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, ChangeByOxygen))
        self.assertEqual(self.event.compartment_from, BACTERIA_SLOW)
        self.assertEqual(self.event.compartment_to, BACTERIA_FAST)
        self.assertTrue(self.event.oxygen_high_to_change)
        self.assertItemsEqual(self.event.node_types, [BronchialTreeNode, BronchopulmonarySegment])

    def test_increment_from_node(self):
        btn_1 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.2, 0.1, (0, 0))
        btn_2 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.9, 0.1, (0, 0))
        self.assertTrue(btn_2.oxygen_tension > btn_1.oxygen_tension)

        self.assertEqual(self.event.increment_state_variable_from_node(btn_1, None), 0)

        btn_1.update_subpopulation(BACTERIA_SLOW, 10)
        btn_2.update_subpopulation(BACTERIA_SLOW, 10)
        # 2 has more oxygen, so should be more likely to change at 1
        self.assertTrue(self.event.increment_state_variable_from_node(btn_1, None) <
                        self.event.increment_state_variable_from_node(btn_2, None))

        bps_1 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.2, 0.1, (0, 0))
        bps_2 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.9, 0.1, (0, 0))
        self.assertTrue(bps_2.oxygen_tension > bps_1.oxygen_tension)

        self.assertEqual(self.event.increment_state_variable_from_node(bps_1, None), 0)

        bps_1.update_subpopulation(BACTERIA_SLOW, 10)
        bps_2.update_subpopulation(BACTERIA_SLOW, 10)
        # 2 has more oxygen, so should be more likely to change at 1
        self.assertTrue(self.event.increment_state_variable_from_node(bps_1, None) <
                        self.event.increment_state_variable_from_node(bps_2, None))

    def test_update_node(self):
        btn_1 = BronchialTreeNode(0, [BACTERIA_SLOW, BACTERIA_FAST], 0.2, 0.1, (0, 0))
        btn_1.update_subpopulation(BACTERIA_SLOW, 10)
        self.event.update_node(btn_1, None)
        self.assertEqual(btn_1.subpopulations[BACTERIA_SLOW], 9)
        self.assertEqual(btn_1.subpopulations[BACTERIA_FAST], 1)

if __name__ == '__main__':
    unittest.main()
