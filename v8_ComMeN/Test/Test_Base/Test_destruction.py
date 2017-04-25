import unittest
from v8_ComMeN.ComMeN.Base.Events.Destruction import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class DestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.compartment = 'a'
        self.internal_comp_destroy = 'b'
        self.internal_comp_from = 'c'
        self.internal_comp_to = 'd'
        self.event = Destroy(None, 0.1, self.compartment)
        self.event_with_internals_destroyed = Destroy(None, 0.1, self.compartment,
                                                      internals_to_destroy=[self.internal_comp_destroy])
        self.event_with_internals_changed = Destroy(None, 0.1, self.compartment,
                                                internals_changed=[(self.internal_comp_from, self.internal_comp_to)])

    def test_initialise(self):
        self.assertEqual(self.event.compartment_destroyed, self.compartment)
        self.assertFalse(self.event.internals_to_destroy)
        self.assertFalse(self.event.internals_changed)
        self.assertEqual(self.event_with_internals_destroyed.compartment_destroyed, self.compartment)
        self.assertItemsEqual(self.event_with_internals_destroyed.internals_to_destroy, [self.internal_comp_destroy])
        self.assertFalse(self.event_with_internals_destroyed.internals_changed)
        self.assertEqual(self.event_with_internals_changed.compartment_destroyed, self.compartment)
        self.assertFalse(self.event_with_internals_changed.internals_to_destroy)
        self.assertItemsEqual(self.event_with_internals_changed.internals_changed,
                              [(self.internal_comp_from, self.internal_comp_to)])

    def test_increment_from_node(self):
        node = Patch(0, [self.compartment])
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.compartment, 12)
        self.assertEqual(self.event.increment_from_node(node, None), 12)

    def test_update_node(self):
        node = Patch(0, [self.compartment, self.internal_comp_destroy, self.internal_comp_from, self.internal_comp_to])
        node.update_subpopulation(self.compartment, 5)
        node.update_subpopulation(self.internal_comp_destroy, 10)
        node.update_subpopulation(self.internal_comp_from, 18)
        node.update_subpopulation(self.internal_comp_to, 0)
        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.compartment], 4)
        self.assertEqual(node.subpopulations[self.internal_comp_destroy], 10)
        self.assertEqual(node.subpopulations[self.internal_comp_from], 18)
        self.assertEqual(node.subpopulations[self.internal_comp_to], 0)

        node = Patch(0, [self.compartment, self.internal_comp_destroy, self.internal_comp_from, self.internal_comp_to])
        node.update_subpopulation(self.compartment, 5)
        node.update_subpopulation(self.internal_comp_destroy, 10)
        node.update_subpopulation(self.internal_comp_from, 18)
        node.update_subpopulation(self.internal_comp_to, 0)
        self.event_with_internals_destroyed.update_node(node, None)
        self.assertEqual(node.subpopulations[self.compartment], 4)
        self.assertEqual(node.subpopulations[self.internal_comp_destroy], 8)
        self.assertEqual(node.subpopulations[self.internal_comp_from], 18)
        self.assertEqual(node.subpopulations[self.internal_comp_to], 0)

        node = Patch(0, [self.compartment, self.internal_comp_destroy, self.internal_comp_from, self.internal_comp_to])
        node.update_subpopulation(self.compartment, 5)
        node.update_subpopulation(self.internal_comp_destroy, 10)
        node.update_subpopulation(self.internal_comp_from, 18)
        node.update_subpopulation(self.internal_comp_to, 0)
        self.event_with_internals_changed.update_node(node, None)
        self.assertEqual(node.subpopulations[self.compartment], 4)
        self.assertEqual(node.subpopulations[self.internal_comp_destroy], 10)
        self.assertEqual(node.subpopulations[self.internal_comp_from], 15)
        self.assertEqual(node.subpopulations[self.internal_comp_to], 3)


class DestroyByOtherCompartmentTestCase(unittest.TestCase):
    def setUp(self):
        self.compartment = 'a'
        self.influencing_comps = ['b','c']
        self.new_comp = 'd'
        self.event = DestroyByOtherCompartments(None, 0.1, self.compartment, self.influencing_comps)
        self.event_destroy_influencer = DestroyByOtherCompartments(None, 0.1, self.compartment, self.influencing_comps,
                                                                   influencers_to_destroy=[self.influencing_comps[0]])
        self.event_change_influencer = DestroyByOtherCompartments(None, 0.1, self.compartment, self.influencing_comps,
                                                                  influencers_changed=[(self.influencing_comps[1],
                                                                                       self.new_comp)])

    def test_initialise(self):
        self.assertItemsEqual(self.event.influencing_compartments, self.influencing_comps)
        self.assertFalse(self.event.influencers_to_destroy)
        self.assertFalse(self.event.influencers_changed)

        self.assertItemsEqual(self.event_destroy_influencer.influencing_compartments, self.influencing_comps)
        self.assertFalse(self.event_destroy_influencer.influencers_changed)
        self.assertItemsEqual(self.event_destroy_influencer.influencers_to_destroy, [self.influencing_comps[0]])

        self.assertItemsEqual(self.event_change_influencer.influencing_compartments, self.influencing_comps)
        self.assertFalse(self.event_change_influencer.influencers_to_destroy)
        self.assertItemsEqual(self.event_change_influencer.influencers_changed, [(self.influencing_comps[1],
                                                                                  self.new_comp)])

    def test_increment_from_node(self):
        node = Patch(0, [self.compartment, self.influencing_comps[0], self.influencing_comps[1], self.new_comp])
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.subpopulations[self.compartment] = 12
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.subpopulations[self.compartment] = 0
        node.subpopulations[self.influencing_comps[0]] = 12
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.subpopulations[self.compartment] = 3
        node.subpopulations[self.influencing_comps[0]] = 4
        self.assertEqual(self.event.increment_from_node(node, None), 12)
        node.subpopulations[self.influencing_comps[1]] = 2
        self.assertEqual(self.event.increment_from_node(node, None), 18)

    def test_update_node(self):
        node = Patch(0, [self.compartment, self.influencing_comps[0], self.influencing_comps[1], self.new_comp])
        node.subpopulations[self.compartment] = 5
        node.subpopulations[self.influencing_comps[0]] = 3
        node.subpopulations[self.influencing_comps[1]] = 8

        self.event.update_node(node, None)
        self.assertEqual(node.subpopulations[self.compartment], 4)
        self.assertEqual(node.subpopulations[self.influencing_comps[0]], 3)
        self.assertEqual(node.subpopulations[self.influencing_comps[1]], 8)
        self.assertEqual(node.subpopulations[self.new_comp], 0)

        node = Patch(0, [self.compartment, self.influencing_comps[0], self.influencing_comps[1], self.new_comp])
        node.subpopulations[self.compartment] = 5
        node.subpopulations[self.influencing_comps[0]] = 3
        node.subpopulations[self.influencing_comps[1]] = 8

        self.event_destroy_influencer.update_node(node, None)
        self.assertEqual(node.subpopulations[self.compartment], 4)
        self.assertEqual(node.subpopulations[self.influencing_comps[0]], 2)
        self.assertEqual(node.subpopulations[self.influencing_comps[1]], 8)
        self.assertEqual(node.subpopulations[self.new_comp], 0)

        node = Patch(0, [self.compartment, self.influencing_comps[0], self.influencing_comps[1], self.new_comp])
        node.subpopulations[self.compartment] = 5
        node.subpopulations[self.influencing_comps[0]] = 3
        node.subpopulations[self.influencing_comps[1]] = 8

        self.event_change_influencer.update_node(node, None)
        self.assertEqual(node.subpopulations[self.compartment], 4)
        self.assertEqual(node.subpopulations[self.influencing_comps[0]], 3)
        self.assertEqual(node.subpopulations[self.influencing_comps[1]], 7)
        self.assertEqual(node.subpopulations[self.new_comp], 1)

if __name__ == '__main__':
    unittest.main()
