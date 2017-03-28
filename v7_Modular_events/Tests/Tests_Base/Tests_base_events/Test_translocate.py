import unittest

from v7_Modular_events.Models.Base.Events.Translocate import *
from v7_Modular_events.Models.Base.MetapopulationNetwork import *


class TranslocateTestCase(unittest.TestCase):

    def setUp(self):
        self.keys = ['a', 'b']
        self.edge_types = ['alpha', 'beta']
        self.event = Translocate(self.keys[0], self.edge_types[0], 0.1)

        self.nodes = []
        for a in range(3):
            self.nodes.append(Patch(a, self.keys))

        self.edges = [(self.nodes[0], self.nodes[1], {EDGE_TYPE: self.edge_types[0]})]
        self.edges.append((self.nodes[0], self.nodes[2], {EDGE_TYPE: self.edge_types[1]}))
        self.network = MetapopulationNetwork(self.keys, [self.event], self.nodes, self.edges)

    def test_initialise(self):
        self.assertEqual(self.event.class_translocating, self.keys[0])
        self.assertEqual(self.event.edge_type, self.edge_types[0])

    def test_increment_from_node(self):
        # Has edge & class
        self.nodes[0].subpopulations[self.keys[0]] = 4
        self.assertEqual(self.event.increment_from_node(self.nodes[0], self.network), 4)
        # Has edge no class
        self.assertEqual(self.event.increment_from_node(self.nodes[1], self.network), 0)
        # Doesn't have edge
        self.assertEqual(self.event.increment_from_node(self.nodes[2], self.network), 0)

    def test_update_network(self):
        self.nodes[0].subpopulations[self.keys[0]] = 4
        self.event.update_network(self.nodes[0], self.network)
        self.assertEqual(self.nodes[0].subpopulations[self.keys[0]], 3)
        self.assertEqual(self.nodes[1].subpopulations[self.keys[0]], 1)

    def test_pick_a_neighbour(self):
        np.random.seed(101)
        edges = [(self.nodes[0], {}), (self.nodes[1], {})]
        neighbour = self.event.pick_a_neighbour(edges)
        self.assertEqual(neighbour, edges[1][0])

    def test_amounts_to_move(self):
        self.nodes[0].subpopulations[self.keys[0]] = 13

        amounts_to_move = self.event.amounts_to_move(self.nodes[0])
        self.assertItemsEqual(amounts_to_move.keys(), [self.keys[0]])
        self.assertEqual(amounts_to_move[self.keys[0]], 1)


class TranslocateByDegreeTestCase(unittest.TestCase):

    def setUp(self):
        self.keys = ['a', 'b']
        self.edge_types = ['alpha', 'beta']
        self.event = TranslocateByDegree(self.keys[0], self.edge_types[0], 0.1)

        self.nodes = []
        for a in range(10):
            self.nodes.append(Patch(a, self.keys))

        self.edges = []
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (6, 7), (8, 9)]
        for (n1, n2) in edges:
            if n1 == 8:
                self.edges.append((self.nodes[n1], self.nodes[n2], {EDGE_TYPE: self.edge_types[1]}))
            else:
                self.edges.append((self.nodes[n1], self.nodes[n2], {EDGE_TYPE: self.edge_types[0]}))

        self.network = MetapopulationNetwork(self.keys, [self.event], self.nodes, self.edges)

    def test_increment_from_node(self):
        self.nodes[0].subpopulations[self.keys[0]] = 4
        self.assertEqual(self.event.increment_from_node(self.nodes[0], self.network), 4 * 6)
        self.nodes[1].subpopulations[self.keys[0]] = 8
        self.assertEqual(self.event.increment_from_node(self.nodes[1], self.network), 8)
        self.assertEqual(self.event.increment_from_node(self.nodes[2], self.network), 0)
        self.nodes[9].subpopulations[self.keys[0]] = 8
        self.assertEqual(self.event.increment_from_node(self.nodes[9], self.network), 0)
