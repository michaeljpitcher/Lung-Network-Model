import unittest

from v5_Spatial_heterogeneity.Lung_Models.LungLymphMetapopulationNetwork import *
from v5_Spatial_heterogeneity.Lung_Models.BronchopulmonarySegment import BronchopulmonarySegment
from v5_Spatial_heterogeneity.Lung_Models.LymphNode import LymphNode



class LungMetapopTestCase(unittest.TestCase):

    def setUp(self):

        self.species_bronch = ['a', 'b']
        self.species_lymph = ['c', 'd']

        self.load_bronch = dict()
        self.load_bronch[0] = dict()
        self.load_bronch[0]['a'] = 11
        self.load_bronch[10] = dict()
        self.load_bronch[10]['b'] = 3

        self.load_lymph = dict()
        self.load_lymph[39] = dict()
        self.load_lymph[39]['c'] = 7
        self.load_lymph[40] = dict()
        self.load_lymph[40]['c'] = 5

        self.network_s = LungLymphMetapopulationNetwork(self.species_bronch, self.load_bronch, self.species_lymph,
                                                        self.load_lymph, 'stahler')
        self.network_h = LungLymphMetapopulationNetwork(self.species_bronch, self.load_bronch, self.species_lymph,
                                                        self.load_lymph, 'horsfield')

    def ltest_initialise(self):
        self.assertEqual(len(self.network_h.nodes()), 36)

        for i in range(36):
            self.assertTrue(isinstance(self.network_h.node_list[i], BronchopulmonarySegment))
            self.assertTrue(isinstance(self.network_s.node_list[i], BronchopulmonarySegment))

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
            actual_weight = self.network_s.edge[self.network_s.node_list[n1]][self.network_s.node_list[n2]]['edge_object'].weight
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
            actual_weight = self.network_h.edge[self.network_h.node_list[n1]][self.network_h.node_list[n2]]['edge_object'].weight
            self.assertEqual(expected_weight, actual_weight)

        # Attributes - TODO: tests when realistic attributes

    def test_init(self):
        self.assertEqual(len(self.network_s.nodes()), 42)
        self.assertEqual(len(self.network_s.edges()), 57)

        self.assertEqual(len(self.network_s.node_list_bps), 36)
        self.assertEqual(len(self.network_s.node_list_lymph), 6)

        expected_bps_node_ids = range(0,36)
        actual_bps_node_ids = [n.id for n in self.network_s.node_list_bps]
        self.assertItemsEqual(actual_bps_node_ids, expected_bps_node_ids)

        expected_lymph_node_ids = range(36, 42)
        actual_lymph_node_ids = [n.id for n in self.network_s.node_list_lymph]
        self.assertItemsEqual(expected_lymph_node_ids, actual_lymph_node_ids)

        expected_alveoli_ids = range(18, 36)
        actual_alveoli_ids = [n.id for n in self.network_s.alveoli]
        self.assertItemsEqual(expected_alveoli_ids, actual_alveoli_ids)

        # Check object class, species, loads
        for id in self.network_s.node_list:
            node = self.network_s.node_list[id]
            if 0 >= id > 36:
                self.assertTrue(isinstance(node, BronchopulmonarySegment))
                self.assertItemsEqual(node.subpopulations.keys(), ['a', 'b'])
                if id != 0:
                    self.assertEqual(node.subpopulations['a'], 0)
                else:
                    self.assertEqual(node.subpopulations['a'], 11)
                if id != 10:
                    self.assertEqual(node.subpopulations['b'], 0)
                else:
                    self.assertEqual(node.subpopulations['b'], 3)

            elif 36 >= id > 42:
                self.assertTrue(isinstance(node, LymphNode))
                self.assertItemsEqual(node.subpopulations.keys(), ['c', 'd'])
                if id != 39:
                    self.assertEqual(node.subpopulations['c'], 0)
                else:
                    self.assertEqual(node.subpopulations['c'], 7)
                if id != 40:
                    self.assertEqual(node.subpopulations['d'], 0)
                else:
                    self.assertEqual(node.subpopulations['d'], 5)

        # Check edges
        expected_bronch_edges = [(0, 1), (1, 2), (2, 3), (1, 4), (2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10),
                                 (10, 11), (4, 12), (12, 13), (12, 14), (4, 15), (15, 16), (16, 17), (5, 18), (6, 19),
                                 (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28),
                                 (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]
        expected_lymph_edges = [(36, 37), (37, 38), (39, 40), (40, 41)]
        expected_drainage_edges = [(18, 37), (19, 37), (20, 37), (21, 37), (22, 37), (23, 36), (24, 36), (25, 36),
                                   (26, 36), (27, 36), (28, 40), (29, 40), (30, 40), (31, 40), (32, 39), (33, 39),
                                   (34, 39), (35, 39)]
        actual_bronch_edges = [(n1.id, n2.id) for (n1,n2,data) in self.network_s.edges(data=True) if
                               isinstance(data[EDGE_OBJECT], Bronchus)]
        actual_lymph_edges = [(n1.id, n2.id) for (n1,n2,data) in self.network_s.edges(data=True) if
                              isinstance(data[EDGE_OBJECT], LymphaticVessel)]
        actual_drainage_edges = [(n1.id, n2.id) for (n1, n2, data) in self.network_s.edges(data=True) if
                                 isinstance(data[EDGE_OBJECT], Drainage)]

        self.assertEqual(len(expected_bronch_edges), len(actual_bronch_edges))
        self.assertEqual(len(expected_lymph_edges), len(actual_lymph_edges))
        self.assertEqual(len(expected_drainage_edges), len(actual_drainage_edges))

        for (a,b) in expected_bronch_edges:
            self.assertTrue((a, b) in actual_bronch_edges or (b, a) in actual_bronch_edges)

        for (a, b) in expected_lymph_edges:
            self.assertTrue((a, b) in actual_lymph_edges or (b, a) in actual_lymph_edges)

        for (a, b) in expected_drainage_edges:
            self.assertTrue((a, b) in actual_drainage_edges or (b, a) in actual_drainage_edges)


if __name__ == '__main__':
    unittest.main()
