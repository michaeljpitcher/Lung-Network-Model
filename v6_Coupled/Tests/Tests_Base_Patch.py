import unittest
import networkx

from ..Models.Base.MetapopulationNetwork import *
from ..Models.Base.Patch import Patch


class PatchTestCase(unittest.TestCase):

    def setUp(self):

        self.keys = ['a','b','c']
        self.loads = {'a':1,'b':2}
        self.position = (8,8)
        self.patch = Patch(0, self.keys, self.loads, self.position)

    def test_initialise(self):
        self.assertEqual(self.patch.id, 0)
        self.assertItemsEqual(self.patch.subpopulations.keys(), ['a','b','c'])
        self.assertEqual(self.patch.subpopulations['a'], self.loads['a'])
        self.assertEqual(self.patch.subpopulations['b'], self.loads['b'])
        self.assertEqual(self.patch.subpopulations['c'], 0)
        self.assertSequenceEqual(self.patch.position, self.position)

if __name__ == '__main__':
    unittest.main()
