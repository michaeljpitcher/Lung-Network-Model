import unittest
import networkx
from v6_Coupled.Base.MetapopulationNetwork import *


class PatchTestCase(unittest.TestCase):

    def setUp(self):

        self.keys = ['a','b','c']
        self.loads = {'a':1,'b':2}
        self.position = (8,8)
        self.patch = Patch(0, self.keys, self.loads, self.position)

    def test_initialise(self):
        self.assertEqual(self.patch.id, 0)
        self.assertItemsEqual(self.patch.subpopulations.keys(), ['a','b','c'])
        self.assertEqual(self.patch.subpopulations['a'], self.loads['a'])
        self.assertEqual(self.patch.subpopulations['b'], self.loads['b'])
        self.assertEqual(self.patch.subpopulations['c'], 0)
        self.assertSequenceEqual(self.patch.position, self.position)

class MetapopulationNetworkTestCase(unittest.TestCase):

    def setUp(self):

        self.nodes = []
        self.species = ['a','b','c']
        for n in range(7):
            load = {'a':n, 'b': n*2}
            node = Patch(n, self.species, load)
            self.nodes.append(node)

        self.edges = []
        for n in range(6):
            self.edges.append((n, n+1, {EDGE_TYPE:'edge',"test_key":n}))

        self.network = MetapopulationNetwork(self.nodes, self.edges, self.species)

    def test_initialise(self):
        self.assertTrue(isinstance(self.network, networkx.Graph))
        self.assertEqual(self.network.species, self.species)

        # Nodes
        self.assertEqual(len(self.network.node_list), 7)
        self.assertItemsEqual(self.network.node_list.keys(), range(7))
        self.assertItemsEqual(self.network.node_list.values(), self.nodes)
        for n in range(7):
            self.assertEqual(self.network.node_list[n].id, n)

        # Edges - check all specified edges present
        for (id_1,id_2,edge_data) in self.edges:
            node1 = self.network.node_list[id_1]
            node2 = self.network.node_list[id_2]
            self.assertTrue(self.network.has_edge(node1, node2))
            self.assertItemsEqual(self.network.edge[node1][node2].keys(), edge_data.keys())
            for key in self.network.edge[node1][node2].keys():
                self.assertEqual(self.network.edge[node1][node2][key], edge_data[key])

        self.assertEqual(len(self.network.edges()), len(self.edges))

        # Time
        self.assertEqual(self.network.time, 0.0)
        # Data
        self.assertItemsEqual(self.network.data.keys(), [0.0])
        self.assertItemsEqual(self.network.data[0.0].keys(), range(7))
        for n in self.network.data[0.0]:
            self.assertEqual(self.network.data[0.0][n]['a'], n)
            self.assertEqual(self.network.data[0.0][n]['b'], n * 2)
            self.assertEqual(self.network.data[0.0][n]['c'], 0)

    def test_record_data(self):
        self.network.node_list[5].subpopulations['c'] = 66
        self.network.time = 0.5
        self.network.record_data()

        self.assertItemsEqual(self.network.data.keys(), [0.0, 0.5])
        # t = 0.0
        self.assertItemsEqual(self.network.data[0.0].keys(), range(7))
        for n in range(7):
            self.assertEqual(self.network.data[0.0][n]['a'], n)
            self.assertEqual(self.network.data[0.0][n]['b'], n * 2)
            self.assertEqual(self.network.data[0.0][n]['c'], 0)
        # t = 0.5
        self.assertItemsEqual(self.network.data[0.5].keys(), range(7))
        for n in range(7):
            self.assertEqual(self.network.data[0.5][n]['a'], n)
            self.assertEqual(self.network.data[0.5][n]['b'], n * 2)
            if n == 5:
                self.assertEqual(self.network.data[0.5][n]['c'], 66)
            else:
                self.assertEqual(self.network.data[0.5][n]['c'], 0)

    def test_update_node_acceptable(self):

        node = self.network.node_list[0]
        self.network.update_node(node, 'a', 1)
        self.assertEqual(node.subpopulations['a'], 0+1)

        node = self.network.node_list[1]
        self.network.update_node(node, 'b', 2)
        self.assertEqual(node.subpopulations['b'], 1*2 + 2)

        node = self.network.node_list[2]
        self.network.update_node(node, 'c', 3)
        self.assertEqual(node.subpopulations['c'], 3)

    def test_update_node_unacceptable_wrong_species(self):
        node = self.network.node_list[5]
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(node, 'd', -1)
        self.assertTrue("update_node: Invalid species d" in context.exception)

    def test_update_node_unacceptable_invalid_amount(self):
        node = self.network.node_list[5]
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(node, 'c', -1)
        self.assertTrue('update_node: Count cannot drop below zero' in context.exception)



if __name__ == '__main__':
    unittest.main()
