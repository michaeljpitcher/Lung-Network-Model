import unittest

from v8_ComMeN.ComMeN.Base.Events.Change import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class ChangeTestCase(unittest.TestCase):
    def setUp(self):
        self.comp_from = 'a'
        self.comp_to = 'b'
        self.internal_comps = ['c', 'd']
        self.event = Change(None, 0.1, self.comp_from, self.comp_to)
        self.event_with_internals = Change(None, 0.1, self.comp_from, self.comp_to, self.internal_comps)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_from, self.comp_from)
        self.assertEqual(self.event.compartment_to, self.comp_to)
        self.assertFalse(self.event.internals_to_destroy)
        self.assertItemsEqual(self.event_with_internals.internals_to_destroy, self.internal_comps)

    def test_increment_from_node(self):
        node = Patch(0, [self.comp_from, self.comp_to])
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)
        node.update_subpopulation(self.comp_from, 6)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 6)

    def test_update_node(self):
        node = Patch(0, [self.comp_from, self.comp_to])
        node.update_subpopulation(self.comp_from, 6)
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.comp_from], 5)
        self.assertEqual(node.subpopulations[self.comp_to], 1)

        node = Patch(0, [self.comp_from, self.comp_to, self.internal_comps[0], self.internal_comps[1]])
        node.update_subpopulation(self.comp_from, 6)
        node.update_subpopulation(self.internal_comps[0], 12)
        node.update_subpopulation(self.internal_comps[1], 33)
        self.event_with_internals.update_node(node, None)
        self.assertEqual(node.subpopulations[self.comp_from], 5)
        self.assertEqual(node.subpopulations[self.comp_to], 1)
        self.assertEqual(node.subpopulations[self.internal_comps[0]], 10)
        self.assertEqual(node.subpopulations[self.internal_comps[1]], 28)


class ChangeByExternalsTestCase(unittest.TestCase):

    def setUp(self):
        self.comp_from = 'mac_a'
        self.comp_to = 'mac_b'
        self.externals = ['inf_a', 'inf_b']
        self.new_external = 'new_external'
        self.externals_changed = [(self.externals[0], self.new_external)]
        self.event = ChangeByOtherCompartments(None, 0.1, self.comp_from, self.comp_to, self.externals)
        self.event_change_internals = ChangeByOtherCompartments(None, 0.1, self.comp_from, self.comp_to, self.externals,
                                                                influencing_compartments_to_change=self.externals_changed)

    def test_initialise(self):
        self.assertItemsEqual(self.event.influencing_compartments, self.externals)

    def test_increment_from_node(self):
        node = Patch(0, [self.comp_from, self.comp_to] + self.externals)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)
        node.update_subpopulation(self.comp_from, 10)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)
        node.update_subpopulation(self.externals[0], 1)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 10 * 1)
        node.update_subpopulation(self.externals[1], 2)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 10 * (1 + 2))

    def test_update_node(self):
        node = Patch(0, [self.comp_from, self.comp_to, self.new_external] + self.externals)
        node.update_subpopulation(self.comp_from, 10)
        node.update_subpopulation(self.externals[0], 5)
        node.update_subpopulation(self.externals[1], 3)
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.comp_from], 9)
        self.assertEqual(node.subpopulations[self.comp_to], 1)
        self.assertEqual(node.subpopulations[self.externals[0]], 5)
        self.assertEqual(node.subpopulations[self.externals[1]], 3)
        self.assertEqual(node.subpopulations[self.new_external], 0)

        node = Patch(0, [self.comp_from, self.comp_to, self.new_external] + self.externals)
        node.update_subpopulation(self.comp_from, 10)
        node.update_subpopulation(self.externals[0], 5)
        node.update_subpopulation(self.externals[1], 3)
        self.event_change_internals.update_node(node, None)
        self.assertEqual(node.subpopulations[self.comp_from], 9)
        self.assertEqual(node.subpopulations[self.comp_to], 1)
        self.assertEqual(node.subpopulations[self.externals[0]], 4)
        self.assertEqual(node.subpopulations[self.externals[1]], 3)
        self.assertEqual(node.subpopulations[self.new_external], 1)


class ChangeByLackOfExternalsTestCase(unittest.TestCase):

    def setUp(self):
        self.comp_from = 'mac_a'
        self.comp_to = 'mac_b'
        self.inf_comps = ['inf_a', 'inf_b']
        self.event = ChangeByLackOfOtherCompartments(None, 0.1, self.comp_from, self.comp_to, self.inf_comps)

    def test_initialise(self):
        self.assertItemsEqual(self.event.influencing_compartments, self.inf_comps)

    def test_increment_from_node(self):
        node = Patch(0, [self.comp_from, self.comp_to] + self.inf_comps)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)
        node.update_subpopulation(self.comp_from, 10)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 10 * (1 / 0.00000001))
        node.update_subpopulation(self.inf_comps[0], 1)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 10 * (1 / 1))
        node.update_subpopulation(self.inf_comps[1], 2)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 10 * (1 / (1 + 2)))


class InfectTestCase(unittest.TestCase):

    def setUp(self):
        self.comp_from = 'mac_a'
        self.comp_to = 'mac_b'
        self.inf_comps = ['inf_a', 'inf_b']
        self.event = Infect(None, 0.1, self.comp_from, self.comp_to, self.inf_comps)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Change))
        self.assertItemsEqual(self.event.infectious_compartments, self.inf_comps)

    def test_increment_from_node(self):
        node = Patch(0, [self.comp_from, self.comp_to] + self.inf_comps)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)
        node.update_subpopulation(self.comp_from, 10)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 0)
        node.update_subpopulation(self.inf_comps[0], 3)
        self.assertEqual(self.event.increment_state_variable_from_node(node, None), 10.0*3.0/13.0)


if __name__ == '__main__':
    unittest.main()
