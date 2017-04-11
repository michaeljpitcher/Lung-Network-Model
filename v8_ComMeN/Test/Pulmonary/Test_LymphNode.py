import unittest

from v8_ComMeN.ComMeN.Pulmonary.Node.LymphNode import *


class LymphNodeTestCase(unittest.TestCase):
    def setUp(self):
        self.node_id = 0
        self.compartments = ['a', 'b', 'c']
        self.position = (5, 6)
        self.node = LymphNode(self.node_id, self.compartments, self.position)

    def test_initialise(self):
        self.assertTrue(isinstance(self.node, Patch))


if __name__ == '__main__':
    unittest.main()
