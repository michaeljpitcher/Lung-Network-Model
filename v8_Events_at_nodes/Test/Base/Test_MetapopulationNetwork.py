import unittest

from v8_Events_at_nodes.Models.Base.MetapopulationNetwork import *


class MetapopulationNetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a', 'b', 'c']

        class Patch_type1(Patch):
            def __init__(self, compartments):
                Patch.__init__(self, compartments)

        class Patch_type2(Patch):
            def __init__(self, compartments):
                Patch.__init__(self, compartments)

        self.nodes = []
        for a in range(5):
            self.nodes.append(Patch_type1(self.compartments))
        for a in range(5):
            self.nodes.append(Patch_type2(self.compartments))

        self.edge_types = ['edge1', 'edge2']
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 3), (0, 4)]
        self.edges = []
        for n1, n2 in edges:
            self.edges.append((self.nodes[n1], self.nodes[n2], {EDGE_TYPE: self.edge_types[0]}))
        self.edges.append((self.nodes[0], self.nodes[9], {EDGE_TYPE: self.edge_types[1]}))

        self.events_and_node_types = dict()
        class NAEvent(Event):
            def __init__(self, prob, type):
                self.type = type
                Event.__init__(self, prob)

            def increment_from_node(self, node, network):
                return node.subpopulations[self.type]

            def update_node(self, node):
                node.update_subpopulation(self.type, 1)

        self.event_node_type1 = NAEvent(0.1, 'a')
        self.event_node_type2 = NAEvent(0.2, 'a')
        self.event_node_type_both = NAEvent(0.3, 'a')

        self.events_and_node_types[self.event_node_type1] = [Patch_type1]
        self.events_and_node_types[self.event_node_type2] = [Patch_type2]
        self.events_and_node_types[self.event_node_type_both] = [Patch_type1, Patch_type2]
        self.network = MetapopulationNetwork(self.compartments, self.nodes, self.edges, self.events_and_node_types)

    def test_add_node(self):
        network = MetapopulationNetwork(['a'], [], [], {})
        node = Patch(['a'])
        network.add_node(node)
        self.assertTrue(network.has_node(node))

        # Fail not a patch
        with self.assertRaises(AssertionError) as context:
            network.add_node(9)
        self.assertEqual('Node 9 is not a Patch object', str(context.exception))

    def test_add_edge(self):
        network = MetapopulationNetwork(['a'], [], [], {})
        node = Patch(['a'])
        node2 = Patch(['a'])
        network.add_node(node)
        network.add_node(node2)
        edge_data = {EDGE_TYPE: 'edge'}
        network.add_edge(node, node2, edge_data)
        self.assertTrue(network.has_edge(node, node2))
        self.assertItemsEqual(network.edge[node][node2].keys(), edge_data.keys())
        self.assertEqual(network.edge[node][node2][EDGE_TYPE], 'edge')

        # Fail node not present
        node3 = Patch(['a'])
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
        self.assertItemsEqual(self.network.events, self.events_and_node_types.keys())

        self.assertItemsEqual(self.event_node_type1.nodes_impacted, self.nodes[0:5])
        self.assertItemsEqual(self.event_node_type2.nodes_impacted, self.nodes[5:10])
        self.assertItemsEqual(self.event_node_type_both.nodes_impacted, self.nodes)

        self.assertEqual(self.network.time, 0.0)

    def test_run(self):
        self.nodes[0].subpopulations['a'] = 10
        self.network.run(10)
        self.assertTrue(self.network.time > 10)


if __name__ == '__main__':
    unittest.main()
