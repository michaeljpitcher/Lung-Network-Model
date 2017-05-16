import unittest
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Model.MultiPatchFullConnectedEpidemicModel import *


class MultiPatchFullConnectedEpidemicModelTestCase(unittest.TestCase):
    def setUp(self):
        self.number_patches = 5
        self.comps = ['a','b','c']
        self.events = [Event([Patch], 0.1)]
        self.model = MultiPatchFullConnectedEpidemicModel(self.number_patches, self.comps, self.events)

    def test_initialise(self):
        self.assertTrue(isinstance(self.model, MetapopulationNetwork))
        self.assertEqual(len(self.model.nodes()), self.number_patches)
        self.assertItemsEqual([n.node_id for n in self.model.nodes()], range(0, self.number_patches))
        nodes = self.model.node_list
        for n in range(self.number_patches):
            for k in range(self.number_patches):
                if n != k:
                    self.assertTrue(self.model.has_edge(nodes[n], nodes[k]))
                    data = self.model.edge[nodes[n]][nodes[k]]
                    self.assertEqual(data[EDGE_TYPE], 'edge')

if __name__ == '__main__':
    unittest.main()
