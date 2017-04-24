import unittest

from v8_ComMeN.ComMeN.TB.Models.TB_Model_Full import *


class TBModelFullTestCase(unittest.TestCase):
    def setUp(self):
        self.init_mac_bps = 10
        self.init_mac_btn = 7
        self.init_mac_lymph = 3
        self.init_bac_fast = {10:15, 30:5}
        self.init_bac_slow = {7:1, 29:99}
        self.probabilities = {'BacteriaChangeByOxygenFastToSlow': 0.8}
        self.model = TBModelFull(initial_macrophages_bps=self.init_mac_bps, initial_macrophages_btn=self.init_mac_btn,
                                 initial_macrophages_lymph=self.init_mac_lymph, initial_bacteria_fast=self.init_bac_fast,
                                 initial_bacteria_slow=self.init_bac_slow, probabilities=self.probabilities,
                                 include_bronchials=True, include_lymphatics=True, include_bloodstream=True)

    def test_fail_no_events(self):
        with self.assertRaises(AssertionError) as context:
            TBModelFull(self.init_mac_bps, self.init_mac_btn, self.init_mac_lymph, self.init_bac_fast,
                        self.init_bac_slow, [], True, True, True)
        self.assertEqual("No events supplied", str(context.exception))

    def test_differing_events(self):
        all_events = ['BacteriaChangeByOxygenFastToSlow', 'BacteriaReplicationFast', 'RegularMacrophageSpontaneousDeath']
        probabilities = {}
        expected_events = []
        for e in all_events:
            probabilities[e] = 0.1
            expected_events.append(e)
            model = TBModelFull(initial_macrophages_bps=self.init_mac_bps, initial_macrophages_btn=self.init_mac_btn,
                                 initial_macrophages_lymph=self.init_mac_lymph,
                                 initial_bacteria_fast=self.init_bac_fast,
                                 initial_bacteria_slow=self.init_bac_slow, probabilities=probabilities,
                                 include_bronchials=True, include_lymphatics=True, include_bloodstream=True)
            self.assertItemsEqual([n.__class__.__name__ for n in model.events], expected_events)

    def test_initialise(self):
        self.assertItemsEqual(self.model.compartments, [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR,
                                                        MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED,
                                                        T_CELL_HELPER, T_CELL_CYTOTOXIC])

if __name__ == '__main__':
    unittest.main()
