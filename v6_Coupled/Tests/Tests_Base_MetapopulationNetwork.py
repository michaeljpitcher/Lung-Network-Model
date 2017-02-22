import unittest
import networkx

from ..Models.Base.MetapopulationNetwork import *
from ..Models.Base.Patch import Patch


class MetapopulationNetworkTestCase(unittest.TestCase):

    def setUp(self):

        self.nodes_ = []
        self.species = ['a','b','c']
        for n in range(7):
            load = {'a':n, 'b': n*2}
            node = Patch(n, self.species, load)
            self.nodes_.append(node)

        self.edges = []
        for n in range(6):
            self.edges.append((self.nodes_[n], self.nodes_[n + 1], {EDGE_TYPE: 'edge', "test_key":n}))

        self.network = MetapopulationNetwork(self.nodes_, self.edges, self.species)

    def test_initialise(self):
        self.assertTrue(isinstance(self.network, networkx.Graph))
        self.assertEqual(self.network.species, self.species)

        # Nodes
        self.assertEqual(len(self.network.node_list), 7)
        self.assertItemsEqual(self.network.node_list.keys(), range(7))
        self.assertItemsEqual(self.network.node_list.values(), self.nodes_)
        for n in range(7):
            self.assertEqual(self.network.node_list[n].id, n)

        # Edges - check all specified edges present
        for (node1,node2,edge_data) in self.edges:
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

class RunMetapopulationNetworkTestCase(unittest.TestCase):

    def setUp(self):
        # Need to sub-class
        class Test(MetapopulationNetwork):
            def __init__(self):
                nodes = []
                species = ['a', 'b', 'c']
                for n in range(7):
                    load = {'a': n, 'b': n * 2}
                    node = Patch(n, species, load)
                    nodes.append(node)

                edges = []
                for n in range(6):
                    edges.append((nodes[n], nodes[n + 1], {EDGE_TYPE: 'edge', "test_key": n}))

                MetapopulationNetwork.__init__(self, nodes, edges, species)

                self.rate_for_function_1 = 0.0
                self.rate_for_function_2 = 0.0

                self.counter_for_function_1 = 0
                self.counter_for_function_2 = 0

            def events(self):
                return [(self.rate_for_function_1, lambda f: self.function_1()),
                        (self.rate_for_function_2, lambda f: self.function_2())]

            def function_1(self):
                self.counter_for_function_1 += 1

            def function_2(self):
                self.counter_for_function_2 += 1

        self.network = Test()

    def test_run_0_prob(self):
        self.network.run(10)
        self.assertEqual(self.network.time, 0.0)

    def test_run(self):
        self.network.rate_for_function_1 = 1.0
        self.network.run(10)
        self.assertTrue(self.network.time >= 0.0)
        self.assertTrue(self.network.counter_for_function_1 > 0)
        self.assertEqual(self.network.counter_for_function_2, 0)


if __name__ == '__main__':
    unittest.main()
