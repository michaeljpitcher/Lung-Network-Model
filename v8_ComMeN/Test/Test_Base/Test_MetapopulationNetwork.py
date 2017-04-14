import unittest

from v8_ComMeN.ComMeN.Base.Network.MetapopulationNetwork import *


class MetapopulationNetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a', 'b', 'c']

        class Patch_type1(Patch):
            def __init__(self, id, compartments):
                Patch.__init__(self, id, compartments)

        class Patch_type2(Patch):
            def __init__(self, id, compartments):
                Patch.__init__(self, id, compartments)

        self.nodes = []
        for a in range(5):
            self.nodes.append(Patch_type1(a, self.compartments))
        for a in range(5, 10):
            self.nodes.append(Patch_type2(a, self.compartments))

        self.edge_types = ['edge1', 'edge2']
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 3), (0, 4)]
        self.edges = []
        for n1, n2 in edges:
            self.edges.append((self.nodes[n1], self.nodes[n2], {EDGE_TYPE: self.edge_types[0]}))
        self.edges.append((self.nodes[0], self.nodes[9], {EDGE_TYPE: self.edge_types[1]}))

        class NAEvent(Event):
            def __init__(self, node_types, prob, value):
                self.value = value
                Event.__init__(self, node_types, prob)

            def increment_from_node(self, node, network):
                return node.subpopulations[self.value]

            def update_node(self, node, network):
                node.update_subpopulation(self.value, 1)

        self.event_node_type1 = NAEvent([Patch_type1], 0.1, 'a')
        self.event_node_type2 = NAEvent([Patch_type2], 0.2, 'a')
        self.event_node_type_both = NAEvent([Patch_type1, Patch_type2], 0.3, 'a')

        self.events = [self.event_node_type1, self.event_node_type2, self.event_node_type_both]
        self.network = MetapopulationNetwork(self.compartments, self.nodes, self.edges, self.events)

    def test_add_node(self):
        network = MetapopulationNetwork(['a'], [self.nodes[0]], [], [self.event_node_type1])
        node = Patch(0, ['a'])
        network.add_node(node)
        self.assertTrue(network.has_node(node))

        # Fail not a patch
        with self.assertRaises(AssertionError) as context:
            network.add_node(9)
        self.assertEqual('Node 9 is not a Patch object', str(context.exception))

    def test_add_edge(self):
        node = self.nodes[0]
        node2 = self.nodes[1]

        network = MetapopulationNetwork(['a'], [node, node2], [], [self.event_node_type1])

        edge_data = {EDGE_TYPE: 'edge'}
        network.add_edge(node, node2, edge_data)
        self.assertTrue(network.has_edge(node, node2))
        self.assertItemsEqual(network.edge[node][node2].keys(), edge_data.keys())
        self.assertEqual(network.edge[node][node2][EDGE_TYPE], 'edge')

        # Fail node not present
        node3 = Patch(2, ['a'])
        # Fail not a patch
        with self.assertRaises(AssertionError) as context:
            network.add_edge(node, node3, edge_data)
        self.assertTrue('not present in network' in str(context.exception))
        with self.assertRaises(AssertionError) as context:
            network.add_edge(node3, node2, edge_data)
        self.assertTrue('not present in network' in str(context.exception))
        with self.assertRaises(AssertionError) as context:
            network.add_edge(node, node2, {})
        self.assertTrue('Edge type not specified for edge' in str(context.exception))

    def test_initialise(self):
        self.assertItemsEqual(self.compartments, self.network.compartments)
        self.assertItemsEqual(self.network.nodes(), self.nodes)
        self.assertEqual(len(self.network.edges()), len(self.edges))
        for (u, v, data) in self.edges:
            self.assertTrue(self.network.has_edge(u, v))
        self.assertItemsEqual(self.network.events, self.events)

        self.assertItemsEqual(self.event_node_type1.nodes_impacted, self.nodes[0:5])
        self.assertItemsEqual(self.event_node_type2.nodes_impacted, self.nodes[5:10])
        self.assertItemsEqual(self.event_node_type_both.nodes_impacted, self.nodes)

        self.assertEqual(self.network.time, 0.0)

    def test_run(self):
        np.random.seed(101)
        self.nodes[0].subpopulations['a'] = 10
        self.network.run(10)
        self.assertTrue(self.network.time > 10)
        # TODO - further testing for run


if __name__ == '__main__':
    unittest.main()
