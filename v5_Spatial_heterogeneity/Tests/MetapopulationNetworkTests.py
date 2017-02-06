import unittest
from v5_Spatial_heterogeneity import MetapopulationNetwork as mn
from v5_Spatial_heterogeneity import Patch
import numpy as np


class MetapopulationModelTestCase(unittest.TestCase):
    def setUp(self):
        node_count = 10
        self.edges = {(0, 1): 1, (1, 2): 1, (2, 3): 1, (3, 4): 1, (4, 5): 1, (5, 6): 1, (6, 7): 1, (7, 8): 1,
                      (8, 9): 10, (0, 5): 1, (0, 6): 1}
        self.species = ['F', 'S']
        self.initial_loads = dict()
        self.initial_loads[0] = {'F': 10, 'S': 2}
        self.initial_loads[3] = {'F': 1}
        self.initial_loads[9] = {'S': 1}
        self.node_positions = {}
        for i in range(10):
            self.node_positions[i] = (i / 2.0, i / 2.0)
        self.time_limit = 10
        self.network = mn.MetapopulationNetwork(node_count, self.edges, self.species, self.initial_loads,
                                                self.node_positions)

    def test_initialisation(self):
        # Nodes
        self.assertEqual(len(self.network.node_list), 10)
        self.assertItemsEqual(self.network.node_list.keys(), range(10))
        for i in range(10):
            self.assertTrue(isinstance(self.network.node_list[i], Patch.Patch))
        self.assertEqual(len(self.network.nodes()), 10)
        for i in range(10):
            self.assertTrue(isinstance(self.network.nodes()[i], Patch.Patch))
            id = self.network.nodes()[i].id
            self.assertEqual(self.network.nodes()[i], self.network.node_list[id])
        # Edges & weights
        for n1, n2 in self.edges.keys():
            node1 = self.network.node_list[n1]
            node2 = self.network.node_list[n2]
            self.assertTrue((node1, node2) in self.network.edges() or (node2, node1) in self.network.edges())
            expected_weight = self.edges[(n1, n2)]
            self.assertEqual(expected_weight, self.network.edge[node1][node2]['weight'])
        # Initial infections
        for n in range(10):
            patch = self.network.node_list[n]
            if n in self.initial_loads.keys():
                for c in self.species:
                    if c in self.initial_loads[n]:
                        self.assertEqual(patch.subpopulations[c], self.initial_loads[n][c])
                    else:
                        self.assertEqual(patch.subpopulations[c], 0.0)
            else:
                for c in self.species:
                    self.assertEqual(patch.subpopulations[c], 0.0)

        # Time
        self.assertEqual(self.network.time, 0.0)
        # Data
        self.assertItemsEqual(self.network.data.keys(), [0.0])
        self.assertItemsEqual(self.network.data[0.0].keys(), range(10))
        for n in self.network.data[0.0]:
            for c in self.species:
                if n in self.initial_loads and c in self.initial_loads[n]:
                    self.assertEqual(self.network.data[0.0][n][c], self.initial_loads[n][c])
                else:
                    self.assertEqual(self.network.data[0.0][n][c], 0.0)

    def test_record_data(self):
        self.network.node_list[5].subpopulations['F'] = 66
        self.network.time = 0.5
        self.network.record_data()
        self.assertItemsEqual(self.network.data.keys(), [0.0, 0.5])
        # t = 0.0
        self.assertItemsEqual(self.network.data[0.0].keys(), range(10))
        for n in self.network.data[0.0]:
            for c in self.species:
                if n in self.initial_loads and c in self.initial_loads[n]:
                    self.assertEqual(self.network.data[0.0][n][c], self.initial_loads[n][c])
                else:
                    self.assertEqual(self.network.data[0.0][n][c], 0.0)
        # t = 0.5
        self.assertItemsEqual(self.network.data[0.5].keys(), range(10))
        for n in self.network.data[0.5]:
            for c in self.species:
                if n in self.initial_loads and c in self.initial_loads[n]:
                    self.assertEqual(self.network.data[0.5][n][c], self.initial_loads[n][c])
                elif n == 5 and c == 'F':
                    self.assertEqual(self.network.data[0.5][n][c], 66)
                else:
                    self.assertEqual(self.network.data[0.5][n][c], 0.0)

    def test_update_node_acceptable(self):
        # Make infected
        node = self.network.node_list[7]
        self.network.update_node(node, 'F', 1)
        self.assertEqual(node.subpopulations['F'], 1)
        # Stay infected
        node = self.network.node_list[0]
        self.network.update_node(node, 'S', 1)
        self.assertEqual(node.subpopulations['S'], 3)
        # Max count doesn't increase
        node = self.network.node_list[9]
        self.network.update_node(node, 'S', 1)
        self.assertEqual(node.subpopulations['S'], 2)
        # Max count decreases
        node = self.network.node_list[0]
        self.network.update_node(node, 'F', -1)
        self.assertEqual(node.subpopulations['F'], 9)
        # Make susceptible
        node = self.network.node_list[3]
        self.network.update_node(node, 'F', -1)
        self.assertEqual(node.subpopulations['F'], 0)

    def test_update_node_unacceptable_wrong_species(self):
        node = self.network.node_list[5]
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(node, 'R', -1)
        self.assertTrue("update_node: Invalid species" in context.exception)

    def test_update_node_unacceptable_invalid_amount(self):
        node = self.network.node_list[5]
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(node, 'F', -1)
        self.assertTrue('update_node: Count cannot drop below zero' in context.exception)



if __name__ == '__main__':
    unittest.main()
