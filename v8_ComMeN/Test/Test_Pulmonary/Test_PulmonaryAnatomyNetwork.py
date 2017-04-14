import unittest

from v8_ComMeN.ComMeN.Pulmonary.Network.PulmonaryAnatomyNetwork import *


class PulmonaryAnatomyNetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a']
        self.events = [Event([BronchopulmonarySegment], 0.1)]
        self.network_bronchial = PulmonaryAnatomyNetwork(self.compartments, self.events, True, STRAHLER,
                                                         False, False)
        self.network_bronchial_lymphatic = PulmonaryAnatomyNetwork(self.compartments, self.events, True,
                                                                   STRAHLER, True, False)
        self.network_bronchial_lymph_haem = PulmonaryAnatomyNetwork(self.compartments, self.events, True,
                                                                    STRAHLER, True, True)

    def test_initialise(self):

        # BRONCHIAL ONLY
        self.assertItemsEqual([n.node_id for n in self.network_bronchial.nodes()], BRONCHIAL_TREE_NODE_IDS + BRONCHOPULMONARY_SEGMENT_IDS)

        for node_id in BRONCHIAL_TREE_NODE_IDS:
            node = [n for n in self.network_bronchial.nodes() if n.node_id == node_id][0]
            self.assertTrue(isinstance(node, BronchialTreeNode))
            self.assertEqual(node.position, BRONCHIAL_TREE_NODE_POSITIONS[node_id])
            self.assertEqual(node.ventilation, ventilation_from_position(node.position))
            self.assertEqual(node.perfusion, perfusion_from_position(node.position))

        for node_id in BRONCHOPULMONARY_SEGMENT_IDS:
            node = [n for n in self.network_bronchial.nodes() if n.node_id == node_id][0]
            self.assertTrue(isinstance(node, BronchopulmonarySegment))
            self.assertEqual(node.position, BRONCHOPULMONARY_SEGMENT_POSITIONS[node_id])
            self.assertEqual(node.ventilation, ventilation_from_position(node.position))
            self.assertEqual(node.perfusion, perfusion_from_position(node.position))

        actual_edges = [(u.node_id,v.node_id) for (u,v,data) in self.network_bronchial.edges(data=True) if
                        data[EDGE_TYPE] == BRONCHUS]
        self.assertEqual(len(actual_edges), len(BRONCHIAL_TREE_EDGES))

        for (u, v) in actual_edges:
            self.assertTrue((u, v) in BRONCHIAL_TREE_EDGES or (v, u) in BRONCHIAL_TREE_EDGES)

        for (u, v) in BRONCHIAL_TREE_EDGES:
            self.assertTrue((u,v) in actual_edges or (v,u) in actual_edges)

        # LYMPHATIC INCLUDED

        self.assertEqual(len(self.network_bronchial_lymphatic.nodes()), len(BRONCHIAL_TREE_NODE_IDS) +
                         len(BRONCHOPULMONARY_SEGMENT_IDS) + len(LYMPH_NODE_IDS))

        actual_bronch_edges = [(u.node_id, v.node_id) for (u, v, data) in
                               self.network_bronchial_lymphatic.edges(data=True) if data[EDGE_TYPE] == BRONCHUS]
        self.assertEqual(len(actual_bronch_edges), len(BRONCHIAL_TREE_EDGES))

        for (u, v) in actual_bronch_edges:
            self.assertTrue((u, v) in BRONCHIAL_TREE_EDGES or (v, u) in
                            BRONCHIAL_TREE_EDGES)

        for (u, v) in BRONCHIAL_TREE_EDGES:
            self.assertTrue((u, v) in actual_bronch_edges or (v, u) in actual_bronch_edges)

        actual_lymph_edges = [(u.node_id, v.node_id) for (u, v, data) in
                              self.network_bronchial_lymphatic.edges(data=True) if data[EDGE_TYPE] == LYMPHATIC_VESSEL]
        self.assertEqual(len(actual_lymph_edges), len(LYMPH_EDGES))

        for (u, v) in actual_lymph_edges:
            self.assertTrue((u, v) in LYMPH_EDGES or (v, u) in LYMPH_EDGES)

        for (u, v) in LYMPH_EDGES:
            self.assertTrue((u, v) in actual_lymph_edges or (v, u) in actual_lymph_edges)

        # TODO: Haematogenous tests
        actual_bronch_edges = [(u.node_id, v.node_id) for (u, v, data) in
                               self.network_bronchial_lymph_haem.edges(data=True) if data[EDGE_TYPE] == BRONCHUS]
        self.assertEqual(len(actual_bronch_edges), len(BRONCHIAL_TREE_EDGES))

        for (u, v) in actual_bronch_edges:
            self.assertTrue((u, v) in BRONCHIAL_TREE_EDGES or (v, u) in
                            BRONCHIAL_TREE_EDGES)

        for (u, v) in BRONCHIAL_TREE_EDGES:
            self.assertTrue((u, v) in actual_bronch_edges or (v, u) in actual_bronch_edges)

        actual_lymph_edges = [(u.node_id, v.node_id) for (u, v, data) in
                              self.network_bronchial_lymph_haem.edges(data=True) if data[EDGE_TYPE] == LYMPHATIC_VESSEL]
        self.assertEqual(len(actual_lymph_edges), len(LYMPH_EDGES))

        for (u, v) in actual_lymph_edges:
            self.assertTrue((u, v) in LYMPH_EDGES or (v, u) in LYMPH_EDGES)

        for (u, v) in LYMPH_EDGES:
            self.assertTrue((u, v) in actual_lymph_edges or (v, u) in actual_lymph_edges)

        actual_haem_edges = [(u.node_id, v.node_id) for (u, v, data) in
                             self.network_bronchial_lymph_haem.edges(data=True) if data[EDGE_TYPE] == HAEMATOGENOUS]
        self.assertEqual(len(actual_haem_edges), len(HAEMATOGENOUS_EDGES))

        for (u, v) in actual_haem_edges:
            self.assertTrue((u, v) in HAEMATOGENOUS_EDGES or (v, u) in HAEMATOGENOUS_EDGES)

        for (u, v) in HAEMATOGENOUS_EDGES:
            self.assertTrue((u, v) in actual_haem_edges or (v, u) in actual_haem_edges)


if __name__ == '__main__':
    unittest.main()
