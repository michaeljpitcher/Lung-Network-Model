import unittest

from v8_ComMeN.ComMeN.Base.Events.Event import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class EventTestCase(unittest.TestCase):
    def setUp(self):
        self.prob = 0.1
        self.event = Event(self.prob)

        class NAEvent(Event):
            def __init__(self, prob, type):
                self.type = type
                Event.__init__(self, prob)

            def increment_from_node(self, node, network):
                return node.subpopulations[self.type]

            def update_node(self, node, network):
                node.update_subpopulation(self.type, 1)

        self.type = 'a'
        self.non_abstract_event = NAEvent(self.prob, self.type)

    def test_initialise(self):
        self.assertEqual(self.event.probability, self.prob)
        self.assertEqual(self.event.total, 0)
        self.assertEqual(self.event.rate, 0)
        self.assertEqual(len(self.event.nodes_impacted), 0)

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
        self.assertEqual(self.non_abstract_event.total, 3)
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

    def test_change(self):
        node = Patch(0, ['a', 'b'])
        node.update_subpopulation('a', 10)
        change(node, 'a', 'b')
        self.assertEqual(node.subpopulations['a'], 9)
        self.assertEqual(node.subpopulations['b'], 1)

        node = Patch(0, ['a', 'b'])
        node.update_subpopulation('a', 10)
        change(node, 'a', 'b', 4)
        self.assertEqual(node.subpopulations['a'], 6)
        self.assertEqual(node.subpopulations['b'], 4)

    def test_translocate(self):
        node1 = Patch(0, ['a'])
        node2 = Patch(1, ['a'])
        node1.update_subpopulation('a', 10)
        translocate(node1, node2, 'a')
        self.assertEqual(node1.subpopulations['a'], 9)
        self.assertEqual(node2.subpopulations['a'], 1)

        node1 = Patch(0, ['a'])
        node2 = Patch(1, ['a'])
        node1.update_subpopulation('a', 10)
        translocate(node1, node2, 'a', 4)
        self.assertEqual(node1.subpopulations['a'], 6)
        self.assertEqual(node2.subpopulations['a'], 4)


if __name__ == '__main__':
    unittest.main()
