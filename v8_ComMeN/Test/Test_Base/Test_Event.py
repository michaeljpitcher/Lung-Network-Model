import unittest

from v8_ComMeN.ComMeN.Base.Events.Event import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class EventTestCase(unittest.TestCase):
    def setUp(self):
        self.prob = 0.1
        self.node_types = ['type_a', 'type_b']
        self.event = Event(self.node_types, self.prob)

        class NAEvent(Event):
            def __init__(self, node_types, prob, value):
                self.value = value
                Event.__init__(self, node_types, prob)

            def increment_state_variable_from_node(self, node, network):
                return node.subpopulations[self.value]

            def update_node(self, node, network):
                node.update_subpopulation(self.value, 1)

        self.value = 'a'
        self.non_abstract_event = NAEvent(self.node_types, self.prob, self.value)

    def test_initialise(self):
        self.assertEqual(self.event.probability, self.prob)
        self.assertEqual(self.event.state_variable, 0)
        self.assertEqual(self.event.rate, 0)
        self.assertEqual(len(self.event.nodes_impacted), 0)
        self.assertItemsEqual(self.event.node_types, self.node_types)

    def test_attach_nodes(self):
        nodes = [Patch(0, ['a']), Patch(1, ['b'])]
        self.event.attach_nodes(nodes)
        self.assertItemsEqual(self.event.nodes_impacted, nodes)

    def test_update_rate(self):
        nodes = [Patch(0, ['a']), Patch(1, ['a'])]

        nodes[0].update_subpopulation('a', 1)
        nodes[1].update_subpopulation('a', 2)

        self.non_abstract_event.attach_nodes(nodes)
        self.non_abstract_event.update_rate(None)
        self.assertEqual(self.non_abstract_event.state_variable, 3)
        self.assertEqual(self.non_abstract_event.rate, 3 * self.prob)

    def test_update_network(self):
        np.random.seed(101)

        nodes = [Patch(0, ['a']), Patch(1, ['a'])]

        nodes[0].update_subpopulation('a', 1)
        nodes[1].update_subpopulation('a', 2)

        self.non_abstract_event.attach_nodes(nodes)
        self.non_abstract_event.update_rate(None)
        self.non_abstract_event.update_network(None)

        self.assertEqual(nodes[0].subpopulations['a'], 1)
        self.assertEqual(nodes[1].subpopulations['a'], 3)

    def test_destroy_internals_functions(self):
        node = Patch(0, ['a','b','c'])
        node.subpopulations['a'] = 5
        node.subpopulations['b'] = 10
        node.subpopulations['c'] = 18

        destroy_internals(['b','c'],'a',node)

        self.assertEqual(node.subpopulations['a'], 5)
        self.assertEqual(node.subpopulations['b'], 8)
        self.assertEqual(node.subpopulations['c'], 15)


if __name__ == '__main__':
    unittest.main()
