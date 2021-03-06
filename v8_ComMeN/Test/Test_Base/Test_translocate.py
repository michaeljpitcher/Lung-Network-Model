import unittest
from v8_ComMeN.ComMeN.Base.Events.Translocate import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *
from v8_ComMeN.ComMeN.Base.Network.MetapopulationNetwork import *


class TranslocateTestCase(unittest.TestCase):
    def setUp(self):
        self.probability = 0.1
        self.compartment = 'a'
        self.internal_compartment = 'b'
        self.edge_type = 'edge1'
        EDGE_ID = 'edgeid'
        self.event_no_internals = Translocate([Patch], self.probability, self.compartment, self.edge_type)
        self.event_with_internals = Translocate([Patch], self.probability, self.compartment, self.edge_type,
                                                internal_compartments=[self.internal_compartment])
        self.event_not_affected_by_degree = Translocate([Patch], self.probability, self.compartment, self.edge_type,
                                                        probability_increases_with_edges=False)

        self.nodes = [Patch(0, [self.compartment]), Patch(1, [self.compartment]),
                      Patch(2, [self.compartment]), Patch(3, [self.compartment])]
        self.edges = [(self.nodes[0], self.nodes[1], {EDGE_TYPE: self.edge_type, EDGE_ID:1}),
                 (self.nodes[0], self.nodes[2], {EDGE_TYPE: self.edge_type, EDGE_ID:2}),
                 (self.nodes[2], self.nodes[3], {EDGE_TYPE: 'edge2', EDGE_ID:3})]
        events = [self.event_no_internals]

        self.network = MetapopulationNetwork([self.compartment], self.nodes, self.edges, events)

    def test_initialise(self):
        self.assertEqual(self.event_no_internals.translocate_compartment, self.compartment)
        self.assertEqual(self.event_no_internals.edge_type, self.edge_type)
        self.assertFalse(self.event_no_internals.internal_compartments)
        self.assertItemsEqual(self.event_with_internals.internal_compartments, [self.internal_compartment])

    def test_increment_from_node(self):
        # Node 0 - none in compartment
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[0], self.network), 0)
        # Node 0 - some in compartment
        self.nodes[0].update_subpopulation(self.compartment, 5)
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[0], self.network), 5 * 2)
        # Node 1 - none in compartment
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[1], self.network), 0)
        # Node 1 - some in compartment
        self.nodes[1].update_subpopulation(self.compartment, 7)
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[1], self.network), 7)
        # Node 2 - none in compartment
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[2], self.network), 0)
        # Node 2 - some in compartment
        self.nodes[2].update_subpopulation(self.compartment, 3)
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[2], self.network), 3)
        # Node 3 - none in compartment
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[3], self.network), 0)
        # Node 3 - some in compartment (no edges though)
        self.nodes[3].update_subpopulation(self.compartment, 8)
        self.assertEqual(self.event_no_internals.increment_state_variable_from_node(self.nodes[3], self.network), 0)

        # Prob not affected by degree
        self.assertEqual(self.event_not_affected_by_degree.increment_state_variable_from_node(self.nodes[0],
                                                                                              self.network), 5)
        self.assertEqual(self.event_not_affected_by_degree.increment_state_variable_from_node(self.nodes[1],
                                                                                              self.network), 7)
        self.assertEqual(self.event_not_affected_by_degree.increment_state_variable_from_node(self.nodes[2],
                                                                                              self.network), 3)
        self.assertEqual(self.event_not_affected_by_degree.increment_state_variable_from_node(self.nodes[3],
                                                                                              self.network), 0)

    def test_viable_edges(self):
        ids = [data['edgeid'] for (neighbour, data) in self.event_no_internals.viable_edges(self.nodes[0], self.network)]
        self.assertItemsEqual(ids, [1,2])

        ids = [data['edgeid'] for (neighbour, data) in self.event_no_internals.viable_edges(self.nodes[2], self.network)]
        self.assertItemsEqual(ids, [2])

    def test_choose_neighbour(self):
        np.random.seed(101)
        edges = self.event_no_internals.viable_edges(self.nodes[0], self.network)
        # Need to sort to ensure same result for unit testing - this and numpy random seed should produce edge 2
        edges = sorted(edges)
        neighbour = self.event_no_internals.choose_neighbour(edges)
        self.assertEqual(neighbour, self.nodes[2])

    def test_move(self):
        self.nodes[0].subpopulations[self.compartment] = 5
        self.nodes[0].subpopulations[self.internal_compartment] = 15
        self.nodes[1].subpopulations[self.compartment] = 0
        self.nodes[1].subpopulations[self.internal_compartment] = 0

        self.event_no_internals.move(self.nodes[0], self.nodes[1])
        self.assertEqual(self.nodes[0].subpopulations[self.compartment], 4)
        self.assertEqual(self.nodes[0].subpopulations[self.internal_compartment], 15)
        self.assertEqual(self.nodes[1].subpopulations[self.compartment], 1)
        self.assertEqual(self.nodes[1].subpopulations[self.internal_compartment], 0)

        self.nodes[0].subpopulations[self.compartment] = 5
        self.nodes[0].subpopulations[self.internal_compartment] = 15
        self.nodes[1].subpopulations[self.compartment] = 0
        self.nodes[1].subpopulations[self.internal_compartment] = 0

        self.event_with_internals.move(self.nodes[0], self.nodes[1])
        self.assertEqual(self.nodes[0].subpopulations[self.compartment], 4)
        self.assertEqual(self.nodes[0].subpopulations[self.internal_compartment], 12)
        self.assertEqual(self.nodes[1].subpopulations[self.compartment], 1)
        self.assertEqual(self.nodes[1].subpopulations[self.internal_compartment], 3)

    def test_update_node(self):
        np.random.seed(101)
        self.nodes[0].update_subpopulation(self.compartment, 10)
        self.event_no_internals.update_node(self.nodes[0], self.network)
        self.assertEqual(self.nodes[0].subpopulations[self.compartment], 9)
        self.assertEqual(self.nodes[2].subpopulations[self.compartment], 1)


class TranslocateAndChangeTestCase(unittest.TestCase):

    def setUp(self):
        self.probability = 0.1
        self.compartment = 'a'
        self.new_compartment = 'z'
        self.edge_type = 'edge1'
        EDGE_ID = 'edgeid'
        self.event = TranslocateAndChange([Patch], self.probability, self.compartment, self.edge_type,
                                          self.new_compartment)

        self.nodes = [Patch(0, [self.compartment]), Patch(1, [self.compartment]),
                      Patch(2, [self.compartment]), Patch(3, [self.compartment])]
        self.edges = [(self.nodes[0], self.nodes[1], {EDGE_TYPE: self.edge_type, EDGE_ID: 1}),
                      (self.nodes[0], self.nodes[2], {EDGE_TYPE: self.edge_type, EDGE_ID: 2}),
                      (self.nodes[2], self.nodes[3], {EDGE_TYPE: 'edge2', EDGE_ID: 3})]

        self.network = MetapopulationNetwork([self.compartment], self.nodes, self.edges, [self.event])

    def test_move(self):
        self.nodes[0].subpopulations[self.compartment] = 5
        self.nodes[0].subpopulations[self.new_compartment] = 0
        self.nodes[1].subpopulations[self.compartment] = 0
        self.nodes[1].subpopulations[self.new_compartment] = 0

        self.event.move(self.nodes[0], self.nodes[1])
        self.assertEqual(self.nodes[0].subpopulations[self.compartment], 4)
        self.assertEqual(self.nodes[0].subpopulations[self.new_compartment], 0)
        self.assertEqual(self.nodes[1].subpopulations[self.compartment], 0)
        self.assertEqual(self.nodes[1].subpopulations[self.new_compartment], 1)


if __name__ == '__main__':
    unittest.main()
