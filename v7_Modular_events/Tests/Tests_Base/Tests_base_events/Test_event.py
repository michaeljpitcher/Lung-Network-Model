__author__ = "Michael J. Pitcher"

from unittest import TestCase
from v7_Modular_events.Models.Base.Events.Event import *
from v7_Modular_events.Models.Base.Patch import *
from v7_Modular_events.Models.Base.MetapopulationNetwork import *


class EventTestCase(TestCase):

    def setUp(self):
        self.probability = 0.1
        self.event = Event(self.probability)

        class NAEvent(Event):

            def __init__(self, prob, type):
                self.type = type
                Event.__init__(self, prob)

            def increment_from_node(self, node, network):
                return node.subpopulations[self.type]

            def update_network(self, chosen_node, network):
                chosen_node.update(self.type, 1)

        self.type = 'a'
        self.non_abstract_event = NAEvent(self.probability, self.type)

        self.events = [self.non_abstract_event]
        self.keys = ['a']
        node1 = Patch(1, self.keys)
        node2 = Patch(2, self.keys)
        self.nodes = [node1, node2]
        self.edges = [(node1, node2, {EDGE_TYPE:'edge'})]
        self.network = MetapopulationNetwork(self.keys, self.events, self.nodes, self.edges)

    def test_initialise(self):
        self.assertEqual(self.event.probability, self.probability)
        self.assertEqual(self.event.total, 0)

    def test_get_rate(self):
        self.event.total = 10
        self.assertEqual(self.event.get_rate(), self.event.total * self.probability)

    # tests that need non-abstract methods
    def test_increment(self):
        self.nodes[0].update(self.keys[0], 2)
        self.nodes[1].update(self.keys[0], 3)
        self.assertEqual(self.non_abstract_event.increment_from_node(self.nodes[0], None), 2)
        self.assertEqual(self.non_abstract_event.increment_from_node(self.nodes[1], None), 3)

    def test_update_network(self):
        self.non_abstract_event.update_network(self.nodes[0], None)
        self.assertEqual(self.nodes[0].subpopulations['a'], 1)

    def test_perform(self):
        self.nodes[0].update(self.keys[0], 2)
        self.non_abstract_event.total = 2
        self.non_abstract_event.perform(self.network)
        self.assertEqual(self.nodes[0].subpopulations['a'], 3)

        np.random.seed(101)
        self.nodes[1].update(self.keys[0], 9)
        self.non_abstract_event.total = 12
        self.non_abstract_event.perform(self.network)
        self.assertEqual(self.nodes[1].subpopulations['a'], 10)

        np.random.seed(5)
        self.non_abstract_event.total = 13
        self.non_abstract_event.perform(self.network)
        self.assertEqual(self.nodes[0].subpopulations['a'], 4)


