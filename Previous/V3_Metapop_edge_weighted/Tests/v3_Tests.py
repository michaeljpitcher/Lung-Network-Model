import math
import unittest

import numpy as np

from Previous import V3_Metapop_edge_weighted as MWN


class v3BasicTestCase(unittest.TestCase):

    def setUp(self):

        self.edges = [(0,1), (1,2), (1,3), (1,4), (4,5), (5,0)]
        self.weights = dict()
        count = 10
        for edge in self.edges:
            self.weights[edge] = count
            count -= 1
        self.pos = [(1,1), (2,2), (2,3), (3,3), (3,2), (2,1)]

        self.infections = dict()
        self.infections[1] = 30
        self.infections[5] = 10

        self.ptransmit = 0.5
        self.pgrowth = - 0.1
        self.timelimit = 1
        self.network = MWN.MetapopulationWeightedNetwork(self.edges, self.weights, self.pos, self.infections,
                                                         self.ptransmit, self.pgrowth, self.timelimit)

    def test_initialise(self):
        self.assertItemsEqual(self.network.nodes(), range(0,6))
        for e1, e2 in self.edges:
            self.assertTrue((e1,e2) in self.network.edges() or (e2,e1) in self.network.edges())
        self.assertEqual(self.network.edge[0][1]['weight'], 10)
        self.assertEqual(self.network.edge[1][2]['weight'], 9)
        self.assertEqual(self.network.edge[1][3]['weight'], 8)
        self.assertEqual(self.network.edge[1][4]['weight'], 7)
        self.assertEqual(self.network.edge[4][5]['weight'], 6)
        self.assertEqual(self.network.edge[5][0]['weight'], 5)
        self.assertSequenceEqual(self.network.positioning, self.pos)

        self.assertItemsEqual(self.network.infected_nodes, self.infections.keys())
        for n in range(0,6):
            if n in self.infections:
                self.assertEqual(self.network.node[n]['count'], self.infections[n])
            else:
                self.assertEqual(self.network.node[n]['count'], 0.0)

        self.assertEqual(self.network.rates['p_transmit'], self.ptransmit)
        self.assertEqual(self.network.rates['p_growth'], self.pgrowth)

        self.assertEqual(self.network.timestep, 0.0)
        self.assertEqual(self.network.time_limit, self.timelimit)

        self.assertItemsEqual(self.network.data.keys(), [0.0])
        self.assertItemsEqual(self.network.data[0.0].keys(), range(0,6))
        for n in range(0, 6):
            if n in self.infections:
                self.assertEqual(self.network.data[0.0][n], self.infections[n])
            else:
                self.assertEqual(self.network.data[0.0][n], 0.0)

        self.assertEqual(self.network.max_count, max(self.infections.values()))
        self.assertEqual(self.network.total_possible_transmission, 0.0)
        self.assertEqual(self.network.total_bacteria, 0.0)

    def test_record_data(self):
        self.network.timestep = 1.0
        self.network.node[3]['count'] = 99
        self.network.record_data()

        self.assertEqual(self.network.data.keys(), [0.0, 1.0])
        for n in range(0,6):
            # at t = 0.0
            if n in self.infections:
                self.assertEqual(self.network.data[0.0][n], self.infections[n])
            else:
                self.assertEqual(self.network.data[0.0][n], 0.0)

            # at t = 1.0
            if n in self.infections:
                self.assertEqual(self.network.data[1.0][n], self.infections[n])
            elif n == 3:
                self.assertEqual(self.network.data[1.0][n], 99)
            else:
                self.assertEqual(self.network.data[1.0][n], 0.0)

    def test_update_node(self):
        # Positive - already infected
        self.network.update_node(1, 1)
        self.assertEqual(self.network.node[1]['count'], 31)
        self.assertItemsEqual(self.network.infected_nodes, [1, 5])
        self.assertEqual(self.network.max_count, 31)

        # Positive - newly infected
        self.network.update_node(0, 1)
        self.assertEqual(self.network.node[0]['count'], 1)
        self.assertItemsEqual(self.network.infected_nodes, [0, 1, 5])
        self.assertEqual(self.network.max_count, 31)

        # Negative - stays infected
        self.network.update_node(5,-1)
        self.assertEqual(self.network.node[5]['count'], 9)
        self.assertItemsEqual(self.network.infected_nodes, [0, 1, 5])
        self.assertEqual(self.network.max_count, 31)

        # Negative - become susceptible
        self.network.update_node(1, -31)
        self.assertEqual(self.network.node[1]['count'], 0)
        self.assertItemsEqual(self.network.infected_nodes, [0, 5])
        self.assertEqual(self.network.max_count, 9)

    def test_update_node_fails(self):
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(1, -99)
        self.assertTrue('update_node: Count cannot drop below zero' in context.exception)

    def test_update_totals(self):
        self.network.update_totals()
        # Sum of (Count at infected node * sum of weights of edges from infected node)
        self.assertEqual(self.network.total_possible_transmission, 30 * (4) + 10 * (2))
        # Sum of count at all infected node
        self.assertEqual(self.network.total_bacteria, 30 + 10)

    def test_calculate_dt(self):
        np.random.seed(100) # x = 0.543404941791
        dt = self.network.calculate_dt(100.0)
        self.assertAlmostEqual(dt, (1.0 / 100.0) * math.log(1.0 / 0.543404941791))

    def test_choose_transition(self):
        # Picks a transmit
        self.network.update_totals()
        transitions = self.network.transitions()
        total = transitions[0][0] + transitions[1][0]
        np.random.seed(100) # x = 370.05876536
        function = self.network.choose_transition(total, transitions)
        self.assertEqual(function,0)

        # Picks a growth
        # Alter network - easier to get a growth
        growth_network = MWN.MetapopulationWeightedNetwork(self.edges, self.weights, self.pos, self.infections, 0.001,
                                                           0.5, self.timelimit)
        growth_network.update_totals()
        transitions = growth_network.transitions()
        total = transitions[0][0] + transitions[1][0]
        np.random.seed(100)  # x = 17.0357449251
        function = growth_network.choose_transition(total, transitions)
        self.assertEqual(function, 1)

    def test_transmit(self):
        self.network.update_totals()
        np.random.seed(100)  # r = 97.8128895224, r2=9.46455909319 - should pick edge 1 -> 0
        self.network.transmit()
        self.assertEqual(self.network.node[1]['count'], 29)
        self.assertEqual(self.network.node[0]['count'], 1)

        self.network.update_totals()
        np.random.seed(2135) # r = 154.801986527, r2 = 8.31990523483 - should pick edge 5 -> 4
        self.network.transmit()
        self.assertEqual(self.network.node[5]['count'], 9)
        self.assertEqual(self.network.node[4]['count'], 1)

    def test_growth(self):
        self.network.update_totals()
        np.random.seed(100) # r = 21.7361976716 - picks node 1
        self.network.growth()
        self.assertEqual(self.network.node[1]['count'], 29)

        self.network.update_totals()
        np.random.seed(65765)  # r = 37.9819896608 - picks node 5
        self.network.growth()
        self.assertEqual(self.network.node[5]['count'], 9)



if __name__ == '__main__':
    unittest.main()
