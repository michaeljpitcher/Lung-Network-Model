import unittest
import V3_Metapop_edge_weighted.v3_Lung_network_metapop_edge_weight as MetapopNetwork
import numpy as np


class v3TestCase(unittest.TestCase):

    def setUp(self):
        self.infected = [2]
        self.load = 100
        self.ptransmit = 0.2
        self.pgrowth = -0.1
        self.limit = 1
        self.network = MetapopNetwork.LungNetwork(self.infected, self.load, self.ptransmit, self.pgrowth, self.limit)

    def test_initialise(self):

        # Test topology
        self.assertItemsEqual(self.network.nodes(), range(0, 36))
        self.assertItemsEqual(self.network.edges(),
                              [(0, 1), (1, 2), (2, 3), (1, 4), (2, 5), (5, 6), (3, 7), (3, 8), (8, 9),
                               (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15), (15, 16),
                               (16, 17), (5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23),
                               (9, 24), (10, 25), (11, 26), (11, 27), (13, 28), (13, 29),
                               (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)])

        self.assertItemsEqual(self.network.rates.keys(), ['p_growth', 'p_transmit'])
        self.assertEqual(self.network.rates['p_growth'], self.pgrowth)
        self.assertEqual(self.network.rates['p_transmit'], self.ptransmit)

        self.assertItemsEqual(self.network.infected_nodes, self.infected)

        for n, data in self.network.nodes(data=True):
            if n in self.infected:
                self.assertEqual(data['count'], self.load)
            else:
                self.assertEqual(data['count'], 0)

        self.assertEqual(self.network.timestep, 0.0)
        self.assertEqual(self.network.time_limit, self.limit)
        self.assertEqual(self.network.max_count, self.load)

        # Test data recorded
        self.assertItemsEqual(self.network.data.keys(), [0.0])
        self.assertItemsEqual(self.network.data[0.0].keys(), range(0, 36))
        for n in self.network.data[0.0]:
            if n in self.infected:
                self.assertEqual(self.network.data[0.0][n], self.load)
            else:
                self.assertEqual(self.network.data[0.0][n], 0.0)

        # Check all edges have a weight
        for n1, n2, data in self.network.edges(data=True):
            self.assertItemsEqual(data.keys(),['weight'])

    def test_tree_specifics(self):
        """
        Test for all tree-specific attributes (edge orders, origin, terminals). Not crucial to the actual dynamics.
        :return:
        """
        self.assertEqual(self.network.origin, 0)
        self.assertItemsEqual(self.network.terminal_nodes, range(18,36))
        for n in range(18,36):
            self.assertEqual(len(self.network.neighbors(n)), 1)
            neighbour = self.network.neighbors(n)[0]
            self.assertEqual(self.network.edge[n][neighbour]['weight'], 1)




if __name__ == '__main__':
    unittest.main()
