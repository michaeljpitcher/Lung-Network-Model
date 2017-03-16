import unittest

from v7_Modular_events.Models.Base.Events.Event import *
from ..Models.Base.Patch import *


class EventTestCase(unittest.TestCase):

    def setUp(self):
        self.prob = 0.1
        self.event = Event(self.prob)

        class NAEvent(Event):

            def __init__(self, prob):
                Event.__init__(self, prob)

            def increment_from_node(self, node, network):
                return node.subpopulations['a']

            def update_network(self, chosen_node, network):
                chosen_node.update('a', 1)

        self.chosen_node = Patch(1, ['a'])
        self.chosen_node.subpopulations['a'] = 12
        self.node_2 = Patch(2, ['a'])
        self.node_2.subpopulations['a'] = 15
        self.non_abstract_event = NAEvent(self.prob)

    def test_initialise(self):
        self.assertEqual(self.event.probability, self.prob)
        self.assertEqual(self.event.total, 0)

    def test_get_rate(self):
        self.assertEqual(self.event.get_rate(), 0)

        self.event.total = 16
        self.assertEqual(self.event.get_rate(), 16 * self.prob)

    # tests that need non-abstract methods
    def test_increment(self):
        self.assertEqual(self.non_abstract_event.increment_from_node(self.chosen_node, None), 12)
        self.assertEqual(self.non_abstract_event.increment_from_node(self.node_2, None), 15)

    def test_update_network(self):
        self.non_abstract_event.update_network(self.chosen_node, None)
        self.assertEqual(self.chosen_node.subpopulations['a'], 13)


if __name__ == '__main__':
    unittest.main()
