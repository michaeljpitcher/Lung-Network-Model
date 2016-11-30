import unittest
import V1_SIR.v1_Lung_network_SIS as SISNetwork
import numpy as np

class FirstTestCase(unittest.TestCase):

    def setUp(self):
        self.infected = [0,1,2]
        self.pinfect = 0.2
        self.precover = 0.1
        self.limit = 100
        self.network = SISNetwork.LungNetwork(self.infected,self.pinfect,self.precover,self.limit)

    def check_SI_edge(self, edge):
        return (edge in self.network.si_edges) or ((edge[1], edge[0]) in self.network.si_edges)

    def test_initialise(self):

        # Test topology
        self.assertItemsEqual(self.network.nodes(), range(0,36))
        self.assertItemsEqual(self.network.edges(), [(0,1), (1,2), (2,3), (1,4), (2, 5), (5, 6), (3, 7), (3, 8), (8, 9),
                                                     (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15), (15, 16),
                                                     (16, 17), (5, 18), (6, 19), (6, 20),(7, 21), (7, 22), (8, 23),
                                                     (9, 24), (10, 25), (11, 26), (11, 27), (13, 28), (13, 29),
                                                     (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)])

        self.assertItemsEqual(self.network.states, ['S','I'])
        self.assertItemsEqual(self.network.populations.keys(), ['S','I'])
        self.assertEqual(self.network.rates['p_infect'], self.pinfect)
        self.assertEqual(self.network.rates['p_recover'], self.precover)
        self.assertEqual(self.network.timestep, 0.0)
        self.assertEqual(self.network.time_limit, self.limit)

        # Infection
        for node, data in self.network.nodes(data=True):
            self.assertItemsEqual(data.keys(), ['state'])
            if node in self.infected:
                self.assertEqual(data['state'], 'I')
            else:
                self.assertEqual(data['state'], 'S')
        self.assertItemsEqual(self.network.populations['I'], self.infected)
        self.assertItemsEqual(self.network.populations['S'], range(3,36))
        self.assertItemsEqual(self.network.si_edges, [(1, 4), (2,3), (2,5)])

        # Test data recorded
        self.assertItemsEqual(self.network.data.keys(), [0.0])
        self.assertItemsEqual(self.network.data[0.0].keys(), range(0,36))
        for i in self.network.data[0.0]:
            if i in [0,1,2]:
                self.assertEqual(self.network.data[0.0][i], 'I')
            else:
                self.assertEqual(self.network.data[0.0][i], 'S')

    def test_record_data(self):
        # Update timestep and force a node change
        self.network.timestep += 1.0
        self.network.node[35]['state'] = 'I'
        # Record data
        self.network.record_data()
        self.assertItemsEqual(self.network.data.keys(), [0.0,1.0])
        # Check data at time = 0.0
        self.assertItemsEqual(self.network.data[0.0].keys(), range(0, 36))
        for i in self.network.data[0.0]:
            if i in [0, 1, 2]:
                self.assertEqual(self.network.data[0.0][i], 'I')
            else:
                self.assertEqual(self.network.data[0.0][i], 'S')
        # Check data at time = 1.0
        self.assertItemsEqual(self.network.data[1.0].keys(), range(0, 36))
        for i in self.network.data[1.0]:
            if i in [0, 1, 2, 35]:
                self.assertEqual(self.network.data[1.0][i], 'I')
            else:
                self.assertEqual(self.network.data[1.0][i], 'S')

    def test_update_node_correct(self):
        self.network.update_node(10,'I')
        self.assertEqual(self.network.node[10]['state'], 'I')
        self.assertTrue(10 in self.network.populations['I'])
        self.assertTrue(10 not in self.network.populations['S'])

        self.network.update_node(1, 'S')
        self.assertEqual(self.network.node[1]['state'], 'S')
        self.assertTrue(1 in self.network.populations['S'])
        self.assertTrue(1 not in self.network.populations['I'])

    def test_update_node_incorrect_not_new(self):
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(10, 'S')
        self.assertTrue('State has not been changed (already S)' in context.exception)

    def test_update_node_invalid_state(self):
        with self.assertRaises(AssertionError) as context:
            self.network.update_node(10, 'K')
        self.assertTrue('State K is not valid' in context.exception)

    def test_infect(self):
        np.random.seed(1989) # Picks (2,5) to infect
        self.network.infect()
        self.assertTrue(self.network.node[5]['state'], 'I')

        # Check new SI edges
        # Added (5, 18) and (5, 6)
        self.assertTrue(self.check_SI_edge((5, 18)))
        self.assertTrue(self.check_SI_edge((5, 6)))
        # Removed (2, 5)
        self.assertFalse(self.check_SI_edge((5, 2)))

    def test_recover(self):
        np.random.seed(1989)  # Picks 2 to recover
        self.network.recover()
        self.assertTrue(self.network.node[2]['state'], 'S')

        # Check SI edges
        # Removed (2, 5) and (2, 3)
        self.assertFalse(self.check_SI_edge((5, 2)))
        self.assertFalse(self.check_SI_edge((3, 2)))
        # Added (1, 2)
        self.assertTrue(self.check_SI_edge((1, 2)))

    def test_transitions(self):
        transitions = self.network.transitions()
        self.assertEqual(len(transitions), 2)
        self.assertEqual(len(transitions[0]), 2)
        self.assertEqual(len(transitions[1]), 2)

        # 3 SI edges * 0.2
        self.assertAlmostEqual(3 * self.pinfect, transitions[0][0])
        # 3 SI edges * 0.1
        self.assertAlmostEqual(3 * self.precover, transitions[1][0])

        # TODO: test that functions are right?


if __name__ == '__main__':
    unittest.main()
