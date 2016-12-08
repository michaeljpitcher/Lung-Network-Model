import unittest
import numpy as np
import v2_Metapop_Patch.v2_metapopulation_patch as MetapopPatch


class MetapopulationTestCase(unittest.TestCase):

    def setUp(self):
        node_count = 10
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 5), (0, 6)]
        self.p_transmit = 0.2
        self.p_growth = 0.1
        self.time_limit = 100
        self.initial_loads = {0: 100, 8: 50}
        self.node_positions = {}
        for i in range(10):
            self.node_positions[i] = (i/2.0,i/2.0)
        self.network = MetapopPatch.MetapopulationPatchNetwork(node_count, self.edges, self.p_transmit, self.p_growth,
                                                               self.time_limit, self.initial_loads, self.node_positions)

    def test_initialise(self):
        # Nodes
        self.assertEqual(len(self.network.nodes()), 10)
        for n in self.network.nodes():
            self.assertTrue(isinstance(n, MetapopPatch.Patch))
        for n in range(10):
            self.assertTrue(n in self.network.node_list)
            self.assertTrue(isinstance(self.network.node_list[n], MetapopPatch.Patch))
            self.assertEqual(self.network.node_list[n].id, n)
            self.assertEqual(self.network.node_list[n].position, self.node_positions[n])

        # Edges
        self.assertEqual(len(self.network.edges()), len(self.edges))
        for e1, e2 in self.edges:
            node1 = self.network.node_list[e1]
            node2 = self.network.node_list[e2]
            self.assertTrue((node1, node2) in self.network.edges() or (node2, node1) in self.network.edges())

        # Rates
        self.assertItemsEqual(self.network.rates.keys(), ['p_growth', 'p_transmit'])
        self.assertEqual(self.network.rates['p_growth'], self.p_growth)
        self.assertEqual(self.network.rates['p_transmit'], self.p_transmit)

        # Loads
        for n in range(10):
            if n in self.initial_loads:
                self.assertEqual(self.network.node_list[n].count, self.initial_loads[n])
            else:
                self.assertEqual(self.network.node_list[n].count, 0.0)
            self.assertEqual(self.network.max_count, max(self.initial_loads.values()))

        self.assertEqual(len(self.initial_loads), len(self.network.infected_nodes))
        for n in self.network.infected_nodes:
            self.assertTrue(n.id in self.initial_loads)

        self.assertEqual(self.network.timestep, 0.0)
        self.assertEqual(self.network.time_limit, self.time_limit)

        # Test data recorded
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
        self.assertEqual(node.count, 51)
        self.assertTrue(node in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, 100)
        # Max count increases
        node = self.network.node_list[0]
        self.network.update_node(node, 1)
        self.assertEqual(node.count, 101)
        self.assertTrue(node in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, 101)
        # Max count decreases
        node = self.network.node_list[0]
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
        self.assertEqual(self.network.total_transmit, 100 * 3 + 50 * 2)
        self.assertEqual(self.network.total_growth, 100 + 50)

    def test_transitions(self):
        self.network.calculate_totals()
        t = self.network.transitions()
        self.assertEqual(t[0][0], (100 * 3 + 50 * 2) * self.p_transmit)
        self.assertEqual(t[1][0], (100 + 50) * self.p_growth)

    def test_transmit(self):
        self.network.calculate_totals()
        np.random.seed(100) # r= 217.361976716, Picks second neighbour (0 -> 5)
        self.network.transmit()
        self.assertEqual(self.network.node_list[0].count, 99)
        self.assertEqual(self.network.node_list[5].count, 1)

    def test_growth(self):
        np.random.seed(100)  # Picks node 0
        self.network.growth()
        self.assertEqual(self.network.node_list[0].count, 101)

if __name__ == '__main__':
    unittest.main()
