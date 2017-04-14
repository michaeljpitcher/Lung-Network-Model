import unittest

from v8_ComMeN.ComMeN.Pulmonary.Events.PulmonaryChange import *
from v8_ComMeN.ComMeN.Pulmonary.Node.BronchopulmonarySegment import *


class PulmonaryChangeTestCase(unittest.TestCase):

    def setUp(self):
        self.comp_from = 'a'
        self.comp_to = 'b'
        self.event_high = ChangeByOxygen(None, 0.1, self.comp_from, self.comp_to, True)
        self.event_low = ChangeByOxygen(None, 0.1, self.comp_from, self.comp_to, False)

    def test_initialise(self):
        high_node = BronchopulmonarySegment(0, [self.comp_from, self.comp_to], 0.3, 0.1, (8, 8))
        low_node = BronchopulmonarySegment(0, [self.comp_from, self.comp_to], 0.85, 0.8, (8, 8))

        high_node.update_subpopulation(self.comp_from, 2)
        low_node.update_subpopulation(self.comp_from, 2)

        # High event should get more from the high node
        self.assertTrue(self.event_high.increment_from_node(high_node, None) >
                        self.event_high.increment_from_node(low_node, None))
        # Low event should get more from the low node
        self.assertTrue(self.event_low.increment_from_node(low_node, None) >
                        self.event_low.increment_from_node(high_node, None))

        # TODO - more tests when oxygen tension method confirmed


if __name__ == '__main__':
    unittest.main()
