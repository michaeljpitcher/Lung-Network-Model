import unittest

from v8_ComMeN.ComMeN.Base.Events.Change import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class ChangeTestCase(unittest.TestCase):
    def setUp(self):
        self.comp_from = 'a'
        self.comp_to = 'b'
        self.event = Change(None, 0.1, self.comp_from, self.comp_to)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_from, self.comp_from)
        self.assertEqual(self.event.compartment_to, self.comp_to)

    def test_increment_from_node(self):
        node = Patch(0, [self.comp_from, self.comp_to])
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.comp_from, 6)
        self.assertEqual(self.event.increment_from_node(node, None), 6)

    def test_update_node(self):
        node = Patch(0, [self.comp_from, self.comp_to])
        node.update_subpopulation(self.comp_from, 6)
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.comp_from], 5)
        self.assertEqual(node.subpopulations[self.comp_to], 1)


class ChangeDestroyInternalsTestCase(unittest.TestCase):
    def setUp(self):
        self.comp_from = 'a'
        self.comp_to = 'b'
        self.internal_comps = ['c','d']
        self.event = ChangeDestroyInternals(None, 0.1, self.comp_from, self.comp_to, self.internal_comps)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_from, self.comp_from)
        self.assertEqual(self.event.compartment_to, self.comp_to)
        self.assertItemsEqual(self.event.internal_compartments, self.internal_comps)

    def test_update_node(self):
        node = Patch(0, [self.comp_from, self.comp_to, self.internal_comps[0], self.internal_comps[1]])
        node.update_subpopulation(self.comp_from, 6)
        node.update_subpopulation(self.internal_comps[0], 12)
        node.update_subpopulation(self.internal_comps[1], 33)
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.comp_from], 5)
        self.assertEqual(node.subpopulations[self.comp_to], 1)
        self.assertEqual(node.subpopulations[self.internal_comps[0]], 10)
        self.assertEqual(node.subpopulations[self.internal_comps[1]], 28)

if __name__ == '__main__':
    unittest.main()
