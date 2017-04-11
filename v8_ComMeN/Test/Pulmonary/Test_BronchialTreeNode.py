import unittest

from v8_ComMeN.ComMeN.Pulmonary.Node.BronchialTreeNode import BronchialTreeNode


class BronchialTreeNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.comps = ['a','b']
        self.node_high_O2 = BronchialTreeNode(0, self.comps, 0.3, 0.01, (0, 0))
        self.node_low_O2 = BronchialTreeNode(0, self.comps, 0.9, 0.89, (0, 0))
        self.node_zero_O2 = BronchialTreeNode(0, self.comps, 0.9, 0.9, (0, 0))

    def test_initialise(self):
        self.assertEqual(self.node_high_O2.ventilation, 0.3)
        self.assertEqual(self.node_high_O2.perfusion, 0.01)

        self.assertEqual(self.node_high_O2.oxygen_tension, 0.3 - 0.01)
        self.assertEqual(self.node_low_O2.oxygen_tension, 0.9 - 0.89)
        self.assertEqual(self.node_zero_O2.oxygen_tension, 0.0000000001)


if __name__ == '__main__':
    unittest.main()
