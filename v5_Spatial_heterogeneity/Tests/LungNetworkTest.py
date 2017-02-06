import unittest
from v5_Spatial_heterogeneity import LungMetapopulationNetwork
from v5_Spatial_heterogeneity import Patch

class LungMetapopTestCase(unittest.TestCase):

    def setUp(self):

        species = ['a', 'b']

        loads = dict()
        loads[0] = dict()
        loads[0]['a'] = 11
        loads[10] = dict()
        loads[10]['b'] = 3

        self.network_s = LungMetapopulationNetwork.LungMetapopulationNetwork(species, loads, 'stahler')
        self.network_h = LungMetapopulationNetwork.LungMetapopulationNetwork(species, loads, 'horsfield')

    def test_initialise(self):
        self.assertEqual(len(self.network_h.nodes()), 36)
        self.assertEqual(len(self.network_h.edges()), 35)

        expected_edges = [(0, 1), (1, 2), (2, 3), (1, 4), (2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11),
                          (4, 12), (12, 13), (12, 14), (4, 15), (15, 16), (16, 17), (5, 18), (6, 19), (6, 20), (7, 21),
                          (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28), (13, 29), (14, 30),
                          (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]

        actual_edges_h = [(n1.id, n2.id) for (n1,n2) in self.network_h.edges()]
        actual_edges_s = [(n1.id, n2.id) for (n1, n2) in self.network_s.edges()]

        for (n1,n2) in expected_edges:
            self.assertTrue((n1, n2) in actual_edges_h or (n2, n1) in actual_edges_h)
            self.assertTrue((n1, n2) in actual_edges_s or (n2, n1) in actual_edges_s)

        for (n1, n2) in actual_edges_h:
            self.assertTrue((n1, n2) in expected_edges or (n2, n1) in expected_edges)

        for (n1, n2) in actual_edges_s:
            self.assertTrue((n1, n2) in expected_edges or (n2, n1) in expected_edges)


        # Weights - STAHLER
        expected_weights_s = {(0, 1): 4, (1, 2): 3, (2, 3): 3, (1, 4): 3, (2, 5): 2, (5, 6): 2, (3, 7): 2,
                                  (3, 8): 2, (8, 9): 2, (9, 10): 2, (10, 11): 2, (4, 12): 3, (12, 13): 2, (12, 14): 2,
                                  (4, 15): 2, (15, 16): 2, (16, 17): 2, (5, 18): 1, (6, 19): 1, (6, 20): 1, (7, 21): 1,
                                  (7, 22): 1, (8, 23): 1, (9, 24): 1, (10, 25): 1, (11, 26): 1, (11, 27): 1,
                                  (13, 28): 1, (13, 29): 1, (14, 30): 1, (14, 31): 1, (15, 32): 1, (16, 33): 1,
                                  (17, 34): 1, (17, 35): 1}

        for (n1,n2) in expected_weights_s:
            expected_weight = expected_weights_s[(n1,n2)]
            actual_weight = self.network_s.edge[self.network_s.node_list[n1]][self.network_s.node_list[n2]]['weight']
            self.assertEqual(expected_weight, actual_weight)

        # HORSFIELD
        expected_weights_h = {(0, 1): 8, (1, 2): 7, (2, 3): 6, (1, 4): 5, (2, 5): 3, (5, 6): 2, (3, 7): 2, (3, 8): 5,
                              (8, 9): 4, (9, 10): 3, (10, 11): 2,
                              (4, 12): 3, (12, 13): 2, (12, 14): 2, (4, 15): 4, (15, 16): 3, (16, 17): 2, (5, 18): 1,
                              (6, 19): 1, (6, 20): 1, (7, 21): 1,
                              (7, 22): 1, (8, 23): 1, (9, 24): 1, (10, 25): 1, (11, 26): 1, (11, 27): 1, (13, 28): 1,
                              (13, 29): 1, (14, 30): 1,
                              (14, 31): 1, (15, 32): 1, (16, 33): 1, (17, 34): 1, (17, 35): 1}

        for (n1, n2) in expected_weights_h:
            expected_weight = expected_weights_h[(n1, n2)]
            actual_weight = self.network_h.edge[self.network_h.node_list[n1]][self.network_h.node_list[n2]]['weight']
            self.assertEqual(expected_weight, actual_weight)

        # Attributes - TODO: tests when realistic attributes




if __name__ == '__main__':
    unittest.main()
