import unittest

from v8_ComMeN.ComMeN.TB.Events.TCellCloning import *


class TCellHelperCloningTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellHelperCloning(0.1)

    def test_something(self):
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_HELPER)


class TCellCytotoxicCloningTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellCytotoxicCloning(0.1)

    def test_something(self):
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment, BronchialTreeNode, LymphNode])
        self.assertEqual(self.event.compartment_created, T_CELL_CYTOTOXIC)


if __name__ == '__main__':
    unittest.main()
