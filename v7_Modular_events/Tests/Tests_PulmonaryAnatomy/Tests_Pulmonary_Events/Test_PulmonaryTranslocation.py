import unittest

from ....Models.PulmonaryAnatomy.PulmonaryEvents.PulmonaryTranslocate import *
from ....Models.PulmonaryAnatomy.BronchopulmonarySegment import *
from ....Models.PulmonaryAnatomy.LymphNode import *
from ....Models.Base.BaseClasses import *
from ....Models.PulmonaryAnatomy.PulmonaryAnatomyClasses import *


class TranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.keys = ['a']
        self.event_weighted = TranslocateBronchus(self.keys[0], 0.1, True)
        self.event_non_weighted = TranslocateBronchus(self.keys[0], 0.1, False)

    def test_initialise(self):
        self.assertTrue(self.event_weighted.move_by_edge_weight)
        self.assertFalse(self.event_non_weighted.move_by_edge_weight)

    def test_pick_a_neighbour(self):
        np.random.seed(101)
        neighbour1 = BronchopulmonarySegment(1, self.keys, (6, 6))
        neighbour2 = BronchopulmonarySegment(2, self.keys, (7, 7))

        edges = [(neighbour1, {EDGE_TYPE: BRONCHUS, WEIGHT: 10}), (neighbour2, {EDGE_TYPE: BRONCHUS, WEIGHT: 1})]
        # Non-weighted
        self.assertEqual(self.event_non_weighted.pick_a_neighbour(edges), edges[1][0])

        # Weighted
        self.assertEqual(self.event_weighted.pick_a_neighbour(edges), edges[0][0])

class TranslocateLymphaticTestCase(unittest.TestCase):
    def setUp(self):
        self.keys = ['a']
        self.event_weighted = TranslocateLymphatic(self.keys[0], 0.1)

    def test_pick_a_neighbour(self):
        np.random.seed(101)
        neighbour1 = LymphNode(1, self.keys, (6, 6))
        neighbour2 = BronchopulmonarySegment(2, self.keys, (7, 7))
        node = LymphNode(3, self.keys, (5, 5))

        edges = [(neighbour1, {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: neighbour1}),
                 (neighbour2, {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: node})]

        self.assertEqual(self.event_weighted.pick_a_neighbour(edges), edges[0][0])


if __name__ == '__main__':
    unittest.main()
