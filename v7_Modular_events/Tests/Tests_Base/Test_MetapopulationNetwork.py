__author__ = "Michael J. Pitcher"

from unittest import TestCase
from ...Models.Base.MetapopulationNetwork import *
from ...Models.Base.Events.Create import *

import os


class MetapopulationNetworkTestCase(TestCase):

    def setUp(self):

        self.keys = ['a','b','c']
        self.edge_types = ['edge1', 'edge2']
        self.events = []
        for a in range(3):
            self.events.append(Replication(self.keys[a], a/10.0))

        self.nodes = []
        self.edges = []
        for a in range(10):
            self.nodes.append(Patch(a, self.keys))
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 3), (0, 4)]
        for n1,n2 in edges:
            self.edges.append((self.nodes[n1], self.nodes[n2], {EDGE_TYPE: self.edge_types[0]}))
        self.edges.append((self.nodes[0], self.nodes[9], {EDGE_TYPE: self.edge_types[1]}))

        self.network = MetapopulationNetwork(self.keys, self.events, self.nodes, self.edges)

    def test_initialise(self):
        self.assertTrue(isinstance(self.network, nx.Graph))
        self.assertEqual(self.network.population_keys, self.keys)
        # Nodes
        self.assertItemsEqual(self.network.node_list, self.nodes)
        self.assertItemsEqual(self.network.nodes(), self.nodes)

        # Edges
        for (n1,n2,_) in self.edges:
            self.assertTrue(self.network.has_edge(n1, n2))
        self.assertEqual(len(self.network.edges()), len(self.edges))
        # Events
        self.assertItemsEqual(self.network.events, self.events)
        self.assertEqual(self.network.time, 0.0)

    def test_initialise_fail_event_wrong_type(self):
        a = dict()
        with self.assertRaises(AssertionError) as context:
            network = MetapopulationNetwork(self.keys, [a], self.nodes, self.edges)
        self.assertTrue('Events specified must be instances of class Event' in context.exception)

    def test_add_node(self):
        node = Patch(99, self.keys)
        self.network.add_node(node)
        self.assertTrue(self.network.has_node(node))
        self.assertTrue(node in self.network.node_list)

    def test_add_node_fail_not_patch(self):
        with self.assertRaises(AssertionError) as context:
            self.network.add_node(9)
        self.assertTrue('Nodes specified must be of instances of Patch class' in context.exception)

    def test_add_node_fail_keys_missing(self):
        p = Patch(1, [])
        with self.assertRaises(AssertionError) as context:
            self.network.add_node(p)
        self.assertTrue('Node Patch: 1 missing key a' in context.exception)

    def test_add_edge(self):
        network = MetapopulationNetwork(self.keys, self.events, [], [])

        node1 = Patch(0, self.keys)
        node2 = Patch(1, self.keys)
        node3 = Patch(2, self.keys)

        self.assertEqual(len(node1.degrees), 0)
        self.assertEqual(len(node2.degrees), 0)

        network.add_edge(node1, node2, {EDGE_TYPE:self.edge_types[0]})
        self.assertTrue(network.has_edge(node1, node2))
        self.assertEqual(len(network.edges()), 1)

        self.assertItemsEqual(node1.degrees.keys(), [self.edge_types[0]])
        self.assertEqual(node1.degrees[self.edge_types[0]], 1)
        self.assertItemsEqual(node2.degrees.keys(), [self.edge_types[0]])
        self.assertEqual(node2.degrees[self.edge_types[0]], 1)

        network.add_edge(node2, node3, {EDGE_TYPE: self.edge_types[1]})
        self.assertTrue(network.has_edge(node3, node2))
        self.assertEqual(len(network.edges()), 2)

        self.assertItemsEqual(node2.degrees.keys(), [self.edge_types[0], self.edge_types[1]])
        self.assertEqual(node2.degrees[self.edge_types[0]], 1)
        self.assertEqual(node2.degrees[self.edge_types[1]], 1)
        self.assertItemsEqual(node3.degrees.keys(), [self.edge_types[1]])
        self.assertEqual(node2.degrees[self.edge_types[1]], 1)

    def test_add_edge_fail_no_edge_type(self):
        network = MetapopulationNetwork(self.keys, self.events, [], [])

        node1 = Patch(0, self.keys)
        node2 = Patch(1, self.keys)
        with self.assertRaises(AssertionError) as context:
            network.add_edge(node1, node2, {})
        self.assertTrue('Edge type not specified for edge Patch: 0-Patch: 1' in context.exception)

    def test_record_data(self):

        np.random.seed(101)

        file_ = open('test_record_data.csv', 'wb')
        csv_writer = csv.writer(file_, delimiter=',')

        expected = dict()
        expected[0.0] = []
        for n in range(10):
            values = dict()
            for a in range(len(self.keys)):
                value = np.random.randint(0, 100)
                self.nodes[n].subpopulations[self.keys[a]] = value
                values[self.keys[a]] = value
            expected[0.0].append(values)

        self.network.record_data(csv_writer)

        expected[4.0] = []
        self.network.time = 4.0
        for n in range(10):
            values = dict()
            for a in range(len(self.keys)):
                value = np.random.randint(0, 100)
                self.nodes[n].subpopulations[self.keys[a]] = value
                values[self.keys[a]] = value
            expected[4.0].append(values)

        self.network.record_data(csv_writer)
        file_.close()

        # Read
        file_ = open('test_record_data.csv', 'r')
        csv_reader = csv.reader(file_)
        row_index = 0
        for row in csv_reader:
            if row_index < 10:
                self.assertEqual(row[0], '0.0')
                self.assertEqual(row[1], str(row_index))
                self.assertEqual(row[2], str(expected[0.0][row_index][self.keys[0]]))
                self.assertEqual(row[3], str(expected[0.0][row_index][self.keys[1]]))
                self.assertEqual(row[4], str(expected[0.0][row_index][self.keys[2]]))
            else:
                self.assertEqual(row[0], '4.0')
                self.assertEqual(row[1], str(row_index-10))
                self.assertEqual(row[2], str(expected[4.0][row_index - 10][self.keys[0]]))
                self.assertEqual(row[3], str(expected[4.0][row_index - 10][self.keys[1]]))
                self.assertEqual(row[4], str(expected[4.0][row_index - 10][self.keys[2]]))

            row_index += 1

        os.remove("test_record_data.csv")

    def test_run_record(self):
        run_id = 99
        self.network.run(101, run_id)
        self.assertTrue(os.path.exists(str(run_id) + ".csv"))
        os.remove(str(run_id) + ".csv")

    def test_run_no_record(self):
        filenames_before = os.listdir(os.curdir)
        self.network.run(101)
        filenames_after = os.listdir(os.curdir)
        self.assertItemsEqual(filenames_before, filenames_after)

    # TODO - more tests for run

    def test_get_neighbouring_edges(self):

        # No edge type specified
        all_edges_at_node0 = self.network.get_neighbouring_edges(self.nodes[0])
        expected_edges = [(self.nodes[1], {EDGE_TYPE:self.edge_types[0]}),
                          (self.nodes[3], {EDGE_TYPE:self.edge_types[0]}),
                          (self.nodes[4], {EDGE_TYPE:self.edge_types[0]}),
                          (self.nodes[9], {EDGE_TYPE:self.edge_types[1]})]
        self.assertItemsEqual(all_edges_at_node0, expected_edges)
        # edge type 1
        e1_edges_at_node0 = self.network.get_neighbouring_edges(self.nodes[0], self.edge_types[0])
        expected_edges = [(self.nodes[1], {EDGE_TYPE: self.edge_types[0]}),
                          (self.nodes[3], {EDGE_TYPE: self.edge_types[0]}),
                          (self.nodes[4], {EDGE_TYPE: self.edge_types[0]})]
        self.assertItemsEqual(e1_edges_at_node0, expected_edges)
        # Edge type 2
        e2_edges_at_node0 = self.network.get_neighbouring_edges(self.nodes[0], self.edge_types[1])
        expected_edges = [(self.nodes[9], {EDGE_TYPE: self.edge_types[1]})]
        self.assertItemsEqual(e2_edges_at_node0, expected_edges)
