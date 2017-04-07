import unittest

from v8_ComMeN.ComMeN.Pulmonary.Network.PulmonaryAnatomyNetwork import *


class PulmonaryAnatomyNetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a']
        self.nodes_event_types = {}
        self.network_bronchial = PulmonaryAnatomyNetwork(self.compartments, self.nodes_event_types, True, STAHLER,
                                                         False, False)
        self.network_bronchial_lymphatic = PulmonaryAnatomyNetwork(self.compartments, self.nodes_event_types, True,
                                                                   STAHLER, True, False)
        self.network_bronchial_lymph_haem = PulmonaryAnatomyNetwork(self.compartments, self.nodes_event_types, True,
                                                                    STAHLER, True, True)

    def test_initialise(self):

        # BRONCHIAL ONLY
        self.assertItemsEqual([n.node_id for n in self.network_bronchial.nodes()],
                              Data_BronchialTree.BRONCHIAL_TREE_IDS)

        for node_id in Data_BronchialTree.BRONCHIAL_TREE_IDS:
            node = [n for n in self.network_bronchial.nodes() if n.node_id == node_id][0]
            self.assertTrue(isinstance(node, BronchialTreeNode))
            self.assertEqual(node.position, Data_BronchialTree.BRONCHIAL_TREE_POSITIONS[node_id])
            self.assertEqual(node.ventilation, Data_BronchialTree.ventilation_from_position(node.position))
            self.assertEqual(node.perfusion, Data_BronchialTree.perfusion_from_position(node.position))

        actual_edges = [(u.node_id,v.node_id) for (u,v,data) in self.network_bronchial.edges(data=True) if
                        data[EDGE_TYPE] == BRONCHUS]
        self.assertEqual(len(actual_edges), len(Data_BronchialTree.BRONCHIAL_TREE_EDGES))

        for (u, v) in actual_edges:
            self.assertTrue((u, v) in Data_BronchialTree.BRONCHIAL_TREE_EDGES or (v, u) in
                            Data_BronchialTree.BRONCHIAL_TREE_EDGES)

        for (u, v) in Data_BronchialTree.BRONCHIAL_TREE_EDGES:
            self.assertTrue((u,v) in actual_edges or (v,u) in actual_edges)

        # LYMPHATIC INCLUDED

        self.assertEqual(len(self.network_bronchial_lymphatic.nodes()), len(Data_BronchialTree.BRONCHIAL_TREE_IDS) +
                         len(Data_Lymphatic.LYMPH_NODE_IDS))

        actual_bronch_edges = [(u.node_id, v.node_id) for (u, v, data) in
                               self.network_bronchial_lymphatic.edges(data=True) if data[EDGE_TYPE] == BRONCHUS]
        self.assertEqual(len(actual_bronch_edges), len(Data_BronchialTree.BRONCHIAL_TREE_EDGES))

        for (u, v) in actual_bronch_edges:
            self.assertTrue((u, v) in Data_BronchialTree.BRONCHIAL_TREE_EDGES or (v, u) in
                            Data_BronchialTree.BRONCHIAL_TREE_EDGES)

        for (u, v) in Data_BronchialTree.BRONCHIAL_TREE_EDGES:
            self.assertTrue((u, v) in actual_bronch_edges or (v, u) in actual_bronch_edges)

        actual_lymph_edges = [(u.node_id, v.node_id) for (u, v, data) in
                              self.network_bronchial_lymphatic.edges(data=True) if data[EDGE_TYPE] == LYMPHATIC_VESSEL]
        self.assertEqual(len(actual_lymph_edges), len(Data_Lymphatic.LYMPH_EDGES))

        for (u, v) in actual_lymph_edges:
            self.assertTrue((u, v) in Data_Lymphatic.LYMPH_EDGES or (v, u) in Data_Lymphatic.LYMPH_EDGES)

        for (u, v) in Data_Lymphatic.LYMPH_EDGES:
            self.assertTrue((u, v) in actual_lymph_edges or (v, u) in actual_lymph_edges)

        # TODO: Haematogenous tests

if __name__ == '__main__':
    unittest.main()
