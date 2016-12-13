import unittest
from v3_Metapop_patch_weight import v3_metapop_patch_weighted as v3
import numpy as np


class MetapopulationPatchWeightedNetworkTestCase(unittest.TestCase):
    def setUp(self):
        node_count = 10
        self.edges = {(0, 1):1, (1, 2):1, (2, 3):1, (3, 4):1, (4, 5):1, (5, 6):1, (6, 7):1, (7, 8):1, (8, 9):10,
                      (0, 5):1, (0, 6):1}
        self.p_transmit = 0.2
        self.p_growth = 0.1
        self.time_limit = 100
        self.initial_loads = {0: 50, 8: 100}
        self.node_positions = {}
        for i in range(10):
            self.node_positions[i] = (i / 2.0, i / 2.0)
        self.network = v3.MetapopulationPatchWeightedNetwork(node_count, self.edges, self.p_transmit, self.p_growth,
                                                               self.time_limit, self.initial_loads, self.node_positions)

    def test_initialise(self):
        # Nodes
        self.assertEqual(len(self.network.node_list), 10)
        self.assertItemsEqual(self.network.node_list.keys(), range(10))
        for i in range(10):
            self.assertTrue(isinstance(self.network.node_list[i], v3.Patch))
        self.assertEqual(len(self.network.nodes()), 10)
        for i in range(10):
            self.assertTrue(isinstance(self.network.nodes()[i], v3.Patch))
            id = self.network.nodes()[i].id
            self.assertEqual(self.network.nodes()[i], self.network.node_list[id])
        # Edges & weights
        for n1,n2 in self.edges.keys():
            node1 = self.network.node_list[n1]
            node2 = self.network.node_list[n2]
            self.assertTrue((node1,node2) in self.network.edges() or (node2,node1) in self.network.edges())
            expected_weight = self.edges[(n1, n2)]
            self.assertEqual(expected_weight, self.network.edge[node1][node2]['weight'])
        # Rates
        self.assertItemsEqual(self.network.rates.keys(), ['p_transmit', 'p_growth'])
        self.assertEqual(self.p_transmit, self.network.rates['p_transmit'])
        self.assertEqual(self.p_growth, self.network.rates['p_growth'])
        # Initial infections
        for n in range(10):
            patch = self.network.node_list[n]
            if n in self.initial_loads.keys():
                self.assertEqual(patch.count, self.initial_loads[n])
                self.assertTrue(patch in self.network.infected_nodes)
            else:
                self.assertEqual(patch.count, 0.0)
        self.assertEqual(self.network.max_count, max(self.initial_loads.values()))
        # Time
        self.assertEqual(self.network.timestep, 0.0)
        self.assertEqual(self.network.time_limit, self.time_limit)
        # Data
        self.assertItemsEqual(self.network.data.keys(), [0.0])
        self.assertItemsEqual(self.network.data[0.0].keys(), range(10))
        for n in self.network.data[0.0]:
            if n in self.initial_loads:
                self.assertEqual(self.network.data[0.0][n], self.initial_loads[n])
            else:
                self.assertEqual(self.network.data[0.0][n], 0.0)

    def test_record_data(self):
        self.network.node_list[5].count = 66
        self.network.timestep = 0.5
        self.network.record_data()
        self.assertItemsEqual(self.network.data.keys(), [0.0, 0.5])
        # t = 0.0
        self.assertItemsEqual(self.network.data[0.0].keys(), range(10))
        for n in self.network.data[0.0]:
            if n in self.initial_loads:
                self.assertEqual(self.network.data[0.0][n], self.initial_loads[n])
            else:
                self.assertEqual(self.network.data[0.0][n], 0.0)
        # t = 0.5
        self.assertItemsEqual(self.network.data[0.5].keys(), range(10))
        for n in self.network.data[0.5]:
            if n in self.initial_loads:
                self.assertEqual(self.network.data[0.5][n], self.initial_loads[n])
            elif n == 5:
                self.assertEqual(self.network.data[0.5][n], 66)
            else:
                self.assertEqual(self.network.data[0.5][n], 0.0)

    def test_update_node_acceptable(self):
        # Make infected
        node = self.network.node_list[7]
        self.network.update_node(node, 1)
        self.assertEqual(node.count, 1)
        self.assertTrue(node in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, 100)
        # Stay infected
        node = self.network.node_list[8]
        self.network.update_node(node, 1)
        self.assertEqual(node.count, 101)
        self.assertTrue(node in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, 101)
        # Max count doesn't increase
        node = self.network.node_list[0]
        self.network.update_node(node, 1)
        self.assertEqual(node.count, 51)
        self.assertTrue(node in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, 101)
        # Max count decreases
        node = self.network.node_list[8]
        self.network.update_node(node, -1)
        self.assertEqual(node.count, 100)
        self.assertTrue(node in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, 100)
        # Make susceptible
        node = self.network.node_list[7]
        self.network.update_node(node, -1)
        self.assertEqual(node.count, 0)
        self.assertTrue(node not in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, 100)

    def test_update_node_unacceptable(self):
        node = self.network.node_list[5]
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(node, -1)
        self.assertTrue('update_node: Count cannot drop below zero' in context.exception)

    def test_calculate_totals(self):
        self.network.calculate_totals()
        self.assertEqual(self.network.total_transmit, 50 * 3 + 100 * 2)
        self.assertEqual(self.network.total_growth, 100 + 50)

    def test_transitions(self):
        self.network.calculate_totals()
        t = self.network.transitions()
        self.assertEqual(t[0][0], (50 * 3 + 100 * 2) * self.p_transmit)
        self.assertEqual(t[1][0], (100 + 50) * self.p_growth)

    def test_transmit(self):
        self.network.calculate_totals()
        np.random.seed(100)
        self.network.transmit()
        self.assertEqual(self.network.node_list[8].count, 99)
        self.assertEqual(self.network.node_list[9].count, 1)

    def test_weights(self):
        # From test above, swap the edge weights of 7-8 and 8-9
        node7 = self.network.node_list[7]
        node8 = self.network.node_list[8]
        node9 = self.network.node_list[9]
        self.network.edge[node8][node9]['weight'] = 1
        self.network.edge[node8][node7]['weight'] = 10
        self.network.calculate_totals()
        np.random.seed(100)
        self.network.transmit()
        self.assertEqual(self.network.node_list[8].count, 99)
        self.assertEqual(self.network.node_list[7].count, 1)

    def test_growth(self):
        np.random.seed(100)
        self.network.growth()
        self.assertEqual(self.network.node_list[0].count, 51)


if __name__ == '__main__':
    unittest.main()
