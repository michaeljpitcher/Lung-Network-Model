import unittest

from v8_ComMeN.ComMeN.Pulmonary.Node.BronchialTreeNode import BronchialTreeNode


class BronchialTreeNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.node_id = 0
        self.compartments = ['a', 'b', 'c']
        self.ventilation = 19
        self.perfusion = 17
        self.position = (5,6)
        self.node = BronchialTreeNode(self.node_id, self.compartments, self.ventilation, self.perfusion, self.position)

    def test_initialise(self):
        self.assertEqual(self.node.ventilation, self.ventilation)
        self.assertEqual(self.node.perfusion, self.perfusion)
        self.assertEqual(self.node.oxygen_tension, self.ventilation / self.perfusion)


if __name__ == '__main__':
    unittest.main()
