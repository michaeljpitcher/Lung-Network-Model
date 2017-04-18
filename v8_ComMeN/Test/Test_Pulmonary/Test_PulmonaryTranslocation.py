import unittest

from v8_ComMeN.ComMeN.Pulmonary.Events.PulmonaryTranslocate import *
from v8_ComMeN.ComMeN.Pulmonary.Node.BronchopulmonarySegment import *
from v8_ComMeN.ComMeN.Base.BaseClasses import *
from v8_ComMeN.ComMeN.Base.Network.MetapopulationNetwork import *


class TranslocateBronchusTestCase(unittest.TestCase):

    def setUp(self):
        self.comp = 'a'
        self.event = TranslocateBronchus([BronchopulmonarySegment], 0.1, self.comp)
        self.event_weighted = TranslocateBronchus([BronchopulmonarySegment], 0.1, self.comp, True)

    def test_initialise(self):
        self.assertFalse(self.event.edge_choice_based_on_weight)
        self.assertTrue(self.event_weighted.edge_choice_based_on_weight)

    def test_choose_neighbour(self):
        nodes = []
        for a in range(10):
            nodes.append(BronchopulmonarySegment(a, [self.comp], 0, 0, (0, 0)))

        edges = [(nodes[0], nodes[1], {EDGE_TYPE: BRONCHUS, WEIGHT: 100})]
        for b in range(2, 10):
            edges.append((nodes[0], nodes[b], {EDGE_TYPE: BRONCHUS, WEIGHT: 1}))

        events = [self.event, self.event_weighted]

        network = MetapopulationNetwork([self.comp], nodes, edges, events)

        np.random.seed(101)
        edges = self.event_weighted.viable_edges(nodes[0], network)
        self.assertEqual(self.event_weighted.choose_neighbour(edges), nodes[1])


class TranslocateLymphTestCase(unittest.TestCase):

    def setUp(self):
        self.comp = 'a'
        self.event = TranslocateLymph([BronchopulmonarySegment], 0.1, self.comp)
        self.event_no_direction = TranslocateLymph([BronchopulmonarySegment], 0.1, self.comp, False)
        self.event_no_flow = TranslocateLymph([BronchopulmonarySegment], 0.1, self.comp, False, False)

    def test_initialise(self):
        self.assertTrue(self.event.direction_only)
        self.assertFalse(self.event_no_direction.direction_only)
        self.assertTrue(self.event.flow_based)
        self.assertFalse(self.event_no_flow.flow_based)

    def test_viable_edges(self):
        nodes = []
        for a in range(10):
            nodes.append(BronchopulmonarySegment(a, [self.comp], 0, 0, (0, 0)))

        edges = [(nodes[0], nodes[1], {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[0], 'edgeid': 0})]
        edges.append((nodes[0], nodes[2], {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[0], 'edgeid': 1}))
        edges.append((nodes[2], nodes[3], {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[3], 'edgeid': 2}))
        edges.append((nodes[0], nodes[3], {EDGE_TYPE: HAEMATOGENOUS, DIRECTION: nodes[3], 'edgeid': 3}))
        events = [self.event, self.event_no_direction]

        network = MetapopulationNetwork([self.comp], nodes, edges, events)

        self.assertEqual(len(self.event.viable_edges(nodes[0], network)), 0)
        self.assertEqual(len(self.event.viable_edges(nodes[1], network)), 1)
        self.assertItemsEqual([data['edgeid'] for (_,data) in self.event.viable_edges(nodes[1], network)], [0])
        self.assertEqual(len(self.event.viable_edges(nodes[2], network)), 2)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event.viable_edges(nodes[2], network)], [1, 2])
        self.assertEqual(len(self.event.viable_edges(nodes[3], network)), 0)

        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[0], network)), 2)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[0], network)],
                              [0, 1])
        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[1], network)), 1)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[1], network)],
                              [0])
        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[2], network)), 2)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[2], network)],
                              [1, 2])
        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[3], network)), 1)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[3], network)],
                              [2])

    def test_increment_from_nodes(self):
        nodes = []
        for a in range(10):
            nodes.append(BronchopulmonarySegment(a, [self.comp], 0, 0, (0, 0)))

        edges = [(nodes[0], nodes[1], {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[0], 'edgeid': 0, FLOW_RATE: 0.9})]
        edges.append((nodes[0], nodes[2], {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[0], 'edgeid': 1, FLOW_RATE: 0.7}))
        edges.append((nodes[2], nodes[3], {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[3], 'edgeid': 2, FLOW_RATE: 0.5}))
        edges.append((nodes[0], nodes[3], {EDGE_TYPE: HAEMATOGENOUS, DIRECTION: nodes[3], 'edgeid': 3}))
        events = [self.event, self.event_no_direction]

        network = MetapopulationNetwork([self.comp], nodes, edges, events)

        nodes[0].update_subpopulation(self.comp, 2)
        nodes[1].update_subpopulation(self.comp, 3)
        nodes[2].update_subpopulation(self.comp, 5)
        nodes[3].update_subpopulation(self.comp, 7)

        self.assertEqual(self.event.increment_from_node(nodes[0], network), 2*0)
        self.assertEqual(self.event.increment_from_node(nodes[1], network), 3*0.9)
        self.assertEqual(self.event.increment_from_node(nodes[2], network), 5*(0.7+0.5))
        self.assertEqual(self.event.increment_from_node(nodes[3], network), 7*0)


class TranslocateBloodTestCase(unittest.TestCase):

    def setUp(self):
        self.comp = 'a'
        self.event = TranslocateBlood([BronchopulmonarySegment], 0.1, self.comp)
        self.event_no_direction = TranslocateBlood([BronchopulmonarySegment], 0.1, self.comp, False)

    def test_initialise(self):
        self.assertTrue(self.event.direction_only)
        self.assertFalse(self.event_no_direction.direction_only)

    def test_viable_edges(self):
        nodes = []
        for a in range(10):
            nodes.append(BronchopulmonarySegment(a, [self.comp], 0, 0, (0, 0)))

        edges = [(nodes[0], nodes[1], {EDGE_TYPE: HAEMATOGENOUS, DIRECTION: nodes[0], 'edgeid': 0})]
        edges.append((nodes[0], nodes[2], {EDGE_TYPE: HAEMATOGENOUS, DIRECTION: nodes[0], 'edgeid': 1}))
        edges.append((nodes[2], nodes[3], {EDGE_TYPE: HAEMATOGENOUS, DIRECTION: nodes[3], 'edgeid': 2}))
        edges.append((nodes[0], nodes[3], {EDGE_TYPE: LYMPHATIC_VESSEL, DIRECTION: nodes[3], 'edgeid': 3}))
        events = [self.event, self.event_no_direction]

        network = MetapopulationNetwork([self.comp], nodes, edges, events)

        self.assertEqual(len(self.event.viable_edges(nodes[0], network)), 0)
        self.assertEqual(len(self.event.viable_edges(nodes[1], network)), 1)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event.viable_edges(nodes[1], network)], [0])
        self.assertEqual(len(self.event.viable_edges(nodes[2], network)), 2)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event.viable_edges(nodes[2], network)], [1, 2])
        self.assertEqual(len(self.event.viable_edges(nodes[3], network)), 0)

        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[0], network)), 2)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[0], network)],
                              [0, 1])
        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[1], network)), 1)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[1], network)],
                              [0])
        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[2], network)), 2)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[2], network)],
                              [1, 2])
        self.assertEqual(len(self.event_no_direction.viable_edges(nodes[3], network)), 1)
        self.assertItemsEqual([data['edgeid'] for (_, data) in self.event_no_direction.viable_edges(nodes[3], network)],
                              [2])

if __name__ == '__main__':
    unittest.main()
