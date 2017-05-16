import unittest
from v8_ComMeN.ComMeN.Epidemiology.BaseEpidemic.Model.SinglePatchEpidemicModel import *


class SinglePatchEpidemicModelTestCase(unittest.TestCase):

    def setUp(self):

        self.comps = ['a','b','c']
        self.events = [Event([Patch], 0.1)]

        self.model = SinglePatchEpidemicModel(self.comps, self.events)

    def test_initialise(self):
        self.assertTrue(isinstance(self.model, MetapopulationNetwork))
        self.assertEqual(len(self.model.nodes()), 1)
        self.assertItemsEqual(self.model.nodes()[0].subpopulations.keys(), self.comps)
        self.assertItemsEqual(self.model.events, self.events)

if __name__ == '__main__':
    unittest.main()
