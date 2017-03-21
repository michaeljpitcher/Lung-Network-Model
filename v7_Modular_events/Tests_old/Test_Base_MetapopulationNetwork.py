import os
import unittest

from v7_Modular_events.Models.Base.Events.Event import *
from ..Models.Base.MetapopulationNetwork import *
from ..Models.Base.Patch import *

class MetapopulationNetworkTestCase(unittest.TestCase):
    def setUp(self):
        self.keys = ['a','b']

        self.nodes = []
        self.nodes.append(Patch(0, self.keys))
        self.nodes.append(Patch(1, self.keys))
        self.nodes.append(Patch(2, self.keys))

        self.nodes[0].subpopulations['a'] = 1
        self.nodes[0].subpopulations['b'] = 2
        self.nodes[1].subpopulations['a'] = 3
        self.nodes[1].subpopulations['b'] = 4
        self.nodes[2].subpopulations['a'] = 5
        self.nodes[2].subpopulations['b'] = 6

        self.edges = []
        self.edges.append((self.nodes[0], self.nodes[1], {EDGE_TYPE: 'edge'}))
        self.edges.append((self.nodes[1], self.nodes[2], {EDGE_TYPE: 'edge'}))

        class NAEvent(Event):

            def __init__(self, prob, _class):
                self._class = _class
                Event.__init__(self, prob)

            def increment_from_node(self, node, network):
                return node.subpopulations[self._class]

            def update_network(self, chosen_node, network):
                chosen_node.update(self._class, 1)

        self.events = []
        self.events.append(NAEvent(0.1, 'a'))
        self.events.append(NAEvent(0.2, 'b'))

        self.network = MetapopulationNetwork(self.keys, nodes=self.nodes, edges=self.edges, events=self.events)

    def test_initialise(self):
        self.assertItemsEqual(self.network.population_keys, self.keys)
        self.assertItemsEqual(self.network.node_list, self.nodes)

        self.assertItemsEqual(self.network.nodes(), self.nodes)

        # When edges added to networkx, nodes may be reversed so can't do direct comparison
        # I.e. (node1, node2, data) could be in network as (node2, node1, data)
        actual_edges = self.network.edges(data=True)
        for (n1,n2,data) in self.edges:
            self.assertTrue((n1,n2,data) in actual_edges or (n2,n1,data) in actual_edges)
        for (n1, n2, data) in actual_edges:
            self.assertTrue((n1, n2, data) in self.edges or (n2, n1, data) in self.edges)

        self.assertItemsEqual(self.network.events, self.events)
        self.assertEqual(self.network.time, 0)

    def test_fail_initialise_not_a_patch(self):
        node_list = [1,2,3]
        with self.assertRaises(AssertionError) as context:
            network = MetapopulationNetwork(self.keys, nodes=node_list, edges=self.edges, events=self.events)
        self.assertTrue("Nodes specified must be of instances of Patch class" in context.exception)

    def test_fail_initialise_missing_population_key(self):
        keys = ['a','b','c']
        with self.assertRaises(AssertionError) as context:
            network = MetapopulationNetwork(keys, nodes=self.nodes, edges=self.edges, events=self.events)
        self.assertTrue("Node " + str(self.nodes[0]) + " missing key c" in context.exception)

    def test_fail_edge_nodes_not_in_graph(self):
        new_patch = Patch(3, self.keys)

        edges = []
        edges.append((self.nodes[0], new_patch, {EDGE_TYPE: 'edge'}))
        with self.assertRaises(AssertionError) as context:
            network = MetapopulationNetwork(self.keys, self.nodes, edges, self.events)
        self.assertTrue("Edge node " + str(new_patch) + " not specified in network" in context.exception)

        edges = []
        edges.append((new_patch, self.nodes[0], {EDGE_TYPE: 'edge'}))
        with self.assertRaises(AssertionError) as context:
            network = MetapopulationNetwork(self.keys, self.nodes, edges, self.events)
        self.assertTrue("Edge node " + str(new_patch) + " not specified in network" in context.exception)

    def test_fail_edge_type_missing(self):
        edges = []
        edges.append((self.nodes[0], self.nodes[1], {'a':1}))
        with self.assertRaises(AssertionError) as context:
            network = MetapopulationNetwork(self.keys, self.nodes, edges, self.events)
        self.assertTrue("Edge type not specified for edge "+ str(self.nodes[0]) + "-" + str(self.nodes[1]) in
                        context.exception)

    def test_fail_not_event(self):
        events = [1,2,3]
        with self.assertRaises(AssertionError) as context:
            network = MetapopulationNetwork(self.keys, self.nodes, self.edges, events)
        self.assertTrue("Events specified must be instances of class Event" in context.exception)


    def test_record_data(self):
        csv_file = open('test.csv', 'wb')
        csv_writer = csv.writer(csv_file, delimiter=',')
        self.network.record_data(csv_writer)
        csv_file.close()
        with open('test.csv', 'rb') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            index = 0
            for row in csv_reader:
                self.assertEqual(row[0], str(0.0))
                self.assertEqual(row[1], str(self.nodes[index].id))
                self.assertEqual(row[2], str(self.nodes[index].subpopulations['a']))
                self.assertEqual(row[3], str(self.nodes[index].subpopulations['b']))
                index += 1
        os.remove("test.csv")

    def test_run_no_chance(self):
        np.random.seed(101)
        for e in self.events:
            e.probability = 0
        self.network = MetapopulationNetwork(self.keys, self.nodes, self.edges, self.events)
        self.network.run(1)

        self.assertEqual(self.network.time, 0.0)

    def test_run_no_id(self):
        np.random.seed(101)
        self.network.run(1)
        filenames = os.listdir(os.curdir)
        # Check no csv files created
        for filename in filenames:
            self.assertFalse(filename.endswith('.csv'))

    def test_run(self):
        np.random.seed(101)
        run_id = 1
        self.network.run(0.5, run_id)
        self.assertTrue(os.path.exists(str(run_id) + ".csv"))

        # TODO - check the output file?
        with open(str(run_id) + '.csv', 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            index = 0
            for row in csv_reader:
                if 0 <= index <= 2:
                    self.assertEqual(row['timestep'], str(0.0))
                elif 3 <= index <= 5:
                    self.assertEqual(row['timestep'], '0.20026553861955745')
                elif 6 <= index <= 8:
                    self.assertEqual(row['timestep'], '0.7039928943290353')

                if index == 0 or index == 3 or index == 6:
                    self.assertEqual(row['patch_id'], "0")
                    self.assertEqual(row['a'], '1')
                    if index == 0:
                        self.assertEqual(row['b'], '2')
                    else:
                        self.assertEqual(row['b'], '3')
                elif index == 1 or index == 4 or index == 7:
                    self.assertEqual(row['patch_id'], "1")
                    self.assertEqual(row['a'], '3')
                    self.assertEqual(row['b'], '4')
                elif index == 2 or index == 5 or index == 8:
                    self.assertEqual(row['patch_id'], "2")
                    self.assertEqual(row['a'], '5')
                    if index == 2 or index == 5:
                        self.assertEqual(row['b'], '6')
                    else:
                        self.assertEqual(row['b'], '7')

                index += 1

        # Get rid of file to avoid further test conflict
        os.remove(str(run_id) + ".csv")


if __name__ == '__main__':
    unittest.main()
