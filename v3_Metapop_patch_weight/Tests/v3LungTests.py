import unittest
from v3_Metapop_patch_weight import v3_metapop_patch_weighted as v3


class LungMetapopulationWeightedNetworkTestCaseStahler(unittest.TestCase):

    def setUp(self):
        self.p_transmit = 0.2
        self.p_growth = 0.1
        self.time_limit = 100
        self.initial_loads = {0: 50, 8: 100}
        self.network_stahler = v3.LungMetapopulationWeightedNetwork(self.p_transmit, self.p_growth, self.time_limit,
                                                                    self.initial_loads, 'stahler')

    def test_initialise(self):
        self.assertEqual(len(self.network_stahler.nodes()), 36)
        expected_edges = [(1, 2), (2, 3), (1, 4), (5, 6), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12),
                          (12, 13), (12, 14), (4, 15), (15, 16), (16, 17), (5, 18), (6, 19), (6, 20), (7, 21), (7, 22),
                          (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28), (13, 29), (14, 30), (14, 31),
                          (15, 32), (16, 33), (17, 34), (17, 35)]
        for e1,e2 in expected_edges:
            node1 = self.network_stahler.node_list[e1]
            node2 = self.network_stahler.node_list[e2]
            self.assertTrue((node1, node2) in self.network_stahler.edges() or
                            (node2, node1) in self.network_stahler.edges())
        self.assertEqual(self.network_stahler.origin, 0)
        expected_non_terminal_patches = [self.network_stahler.node_list[i] for i in range(1, 18)]
        expected_terminal_patches = [self.network_stahler.node_list[i] for i in range(18,36)]
        expected_terminal_patches.append(self.network_stahler.node_list[self.network_stahler.origin])

        self.assertItemsEqual(self.network_stahler.non_terminal_nodes, expected_non_terminal_patches)
        self.assertItemsEqual(self.network_stahler.terminal_nodes, expected_terminal_patches)

        # STAHLER WEIGHTS
        self.expected_weights = {}
        for i1,i2 in [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27),
                      (13, 28), (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]:
            node1 = self.network_stahler.node_list[i1]
            node2 = self.network_stahler.node_list[i2]
            self.assertEqual(self.network_stahler.edge[node1][node2]['weight'], 1)
        for i1,i2 in [(5, 6), (2, 5), (3,7), (3,8), (8,9), (9,10), (10,11), (12,13), (12,14), (4,15), (15,16), (16,17)]:
            node1 = self.network_stahler.node_list[i1]
            node2 = self.network_stahler.node_list[i2]
            self.assertEqual(self.network_stahler.edge[node1][node2]['weight'], 2)
        for i1,i2 in [(1, 2), (2, 3), (1,4), (4,12)]:
            node1 = self.network_stahler.node_list[i1]
            node2 = self.network_stahler.node_list[i2]
            self.assertEqual(self.network_stahler.edge[node1][node2]['weight'], 3)
        node1 = self.network_stahler.node_list[0]
        node2 = self.network_stahler.node_list[1]
        self.assertEqual(self.network_stahler.edge[node1][node2]['weight'], 4)


class LungMetapopulationWeightedNetworkTestCaseHorsfield(unittest.TestCase):

    def setUp(self):
        self.p_transmit = 0.2
        self.p_growth = 0.1
        self.time_limit = 100
        self.initial_loads = {0: 50, 8: 100}
        self.network_horsfield = v3.LungMetapopulationWeightedNetwork(self.p_transmit, self.p_growth, self.time_limit,
                                                                      self.initial_loads, 'horsfield')

    def test_initialise(self):
        self.assertEqual(len(self.network_horsfield.nodes()), 36)
        expected_edges = [(1, 2), (2, 3), (1, 4), (5, 6), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12),
                          (12, 13), (12, 14), (4, 15), (15, 16), (16, 17), (5, 18), (6, 19), (6, 20), (7, 21), (7, 22),
                          (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28), (13, 29), (14, 30), (14, 31),
                          (15, 32), (16, 33), (17, 34), (17, 35)]
        for e1,e2 in expected_edges:
            node1 = self.network_horsfield.node_list[e1]
            node2 = self.network_horsfield.node_list[e2]
            self.assertTrue((node1, node2) in self.network_horsfield.edges() or
                            (node2, node1) in self.network_horsfield.edges())
        self.assertEqual(self.network_horsfield.origin, 0)
        expected_non_terminal_patches = [self.network_horsfield.node_list[i] for i in range(1, 18)]
        expected_terminal_patches = [self.network_horsfield.node_list[i] for i in range(18, 36)]
        expected_terminal_patches.append(self.network_horsfield.node_list[self.network_horsfield.origin])

        self.assertItemsEqual(self.network_horsfield.non_terminal_nodes, expected_non_terminal_patches)
        self.assertItemsEqual(self.network_horsfield.terminal_nodes, expected_terminal_patches)

        # HORSFIELD WEIGHTS
        self.expected_weights = {}
        for i1,i2 in [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27),
                      (13, 28), (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]:
            node1 = self.network_horsfield.node_list[i1]
            node2 = self.network_horsfield.node_list[i2]
            self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 1)
        for i1,i2 in [(5, 6), (3,7), (10,11), (12,13), (12,14),   (16,17)]:
            node1 = self.network_horsfield.node_list[i1]
            node2 = self.network_horsfield.node_list[i2]
            self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 2)
        for i1,i2 in [(9,10), (15,16), (4,12), (2, 5)]:
            node1 = self.network_horsfield.node_list[i1]
            node2 = self.network_horsfield.node_list[i2]
            self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 3)
        for i1,i2 in [(4,15), (8,9)]:
            node1 = self.network_horsfield.node_list[i1]
            node2 = self.network_horsfield.node_list[i2]
            self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 4)
        for i1,i2 in [(1,4), (3,8)]:
            node1 = self.network_horsfield.node_list[i1]
            node2 = self.network_horsfield.node_list[i2]
            self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 5)
        for i1, i2 in [(2, 3)]:
            node1 = self.network_horsfield.node_list[i1]
            node2 = self.network_horsfield.node_list[i2]
            self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 6)
        for i1,i2 in [(1, 2)]:
            node1 = self.network_horsfield.node_list[i1]
            node2 = self.network_horsfield.node_list[i2]
            self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 7)
        node1 = self.network_horsfield.node_list[0]
        node2 = self.network_horsfield.node_list[1]
        self.assertEqual(self.network_horsfield.edge[node1][node2]['weight'], 8)


if __name__ == '__main__':
    unittest.main()
