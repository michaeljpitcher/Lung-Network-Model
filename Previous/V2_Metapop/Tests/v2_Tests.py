import unittest

import numpy as np

import Previous.V2_Metapop.v2_Lung_network_metapopulation as MetapopNetwork


class v2TestCase(unittest.TestCase):

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

    def test_record_data(self):
        self.network.node[10]['count'] = 66
        self.network.timestep = 0.5
        self.network.record_data()

        self.assertItemsEqual(self.network.data.keys(), [0.0, 0.5])

        # t = 0.0
        self.assertItemsEqual(self.network.data[0.0].keys(), range(0, 36))
        for n in self.network.data[0.0]:
            if n in self.infected:
                self.assertEqual(self.network.data[0.0][n], self.load)
            else:
                self.assertEqual(self.network.data[0.0][n], 0.0)

        # t = 0.5
        self.assertItemsEqual(self.network.data[0.5].keys(), range(0, 36))
        for n in self.network.data[0.5]:
            if n in self.infected:
                self.assertEqual(self.network.data[0.5][n], self.load)
            elif n == 10:
                self.assertEqual(self.network.data[0.5][n], 66)
            else:
                self.assertEqual(self.network.data[0.5][n], 0.0)


    def test_update_node_acceptable(self):
        self.network.update_node(10, 1)
        self.assertEqual(self.network.node[10]['count'], 1)
        self.assertTrue(10 in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, self.load)

        self.network.update_node(15, self.load+2)
        self.assertEqual(self.network.node[15]['count'], self.load+2)
        self.assertTrue(15 in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, self.load+2)

        self.network.update_node(15, -1)
        self.assertEqual(self.network.node[15]['count'], self.load+1)
        self.assertTrue(15 in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, self.load+1)

        self.network.update_node(10, -1)
        self.assertEqual(self.network.node[10]['count'], 0)
        self.assertTrue(10 not in self.network.infected_nodes)
        self.assertEqual(self.network.max_count, self.load+1)

    def test_update_node_unacceptable(self):
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(9, -1)
        self.assertTrue('update_node: Count cannot drop below zero' in context.exception)

    def test_transitions(self):
        transitions = self.network.transitions()
        self.assertEqual(self.load * self.network.degree(self.infected[0]) * self.ptransmit, transitions[0][0])
        self.assertEqual(self.load * len(self.infected) * abs(self.pgrowth), transitions[1][0])
        # Test with positive p growth
        self.network.rates['p_growth'] = 0.9
        transitions = self.network.transitions()
        self.assertEqual(self.load * len(self.infected) * 0.9, transitions[1][0])

    def test_transmit(self):
        np.random.seed(100) # Picks second neighbour (2 -> 3)
        self.network.transmit()
        self.assertEqual(self.network.node[2]['count'], 99)
        self.assertEqual(self.network.node[3]['count'], 1)

    def test_growth(self):
        self.network.update_node(10, 100)
        np.random.seed(100)  # Picks node 10
        self.network.growth()
        self.assertEqual(self.network.node[10]['count'], 99)


if __name__ == '__main__':
    unittest.main()
