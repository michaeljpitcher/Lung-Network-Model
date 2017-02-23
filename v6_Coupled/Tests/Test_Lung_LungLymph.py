import unittest
from ..Models.Lung.LungLymph import *


class LungLymphTestCase(unittest.TestCase):

    def setUp(self):

        self.species = ['a', 'b', 'c', 'd']
        self.loads = {0: dict(), 10: dict(), 40: dict()}
        self.loads[0]['a'] = 1
        self.loads[10]['b'] = 2
        self.loads[40]['c'] = 3

        self.positions = dict()
        for i in range(0, 45):
            self.positions[i] = (np.random.randint(0,10), np.random.randint(0, 10))
        self.network = LungLymph(self.species, self.loads, positions=self.positions)

    def test_initialise(self):
        self.assertEqual(len(self.network.nodes()), 45)
        self.assertEqual(len(self.network.node_list), 45)

        self.assertEqual(len(self.network.node_list_bps), 36)
        self.assertEqual(len(self.network.node_list_terminal_bps), 18)
        self.assertEqual(len(self.network.node_list_ln), 9)

        bps_ids = [n.id for n in self.network.node_list_bps]
        self.assertItemsEqual(bps_ids, range(0, 36))
        terminal_bps_ids = [n.id for n in self.network.node_list_terminal_bps]
        self.assertItemsEqual(terminal_bps_ids, range(18, 36))
        ln_ids = [n.id for n in self.network.node_list_ln]
        self.assertItemsEqual(ln_ids, range(36, 45))

        expected_bronch_edges = [(0, 1), (1, 2), (2, 3), (1, 4), (2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10),
                                 (10, 11), (4, 12), (12, 13), (12, 14), (4, 15), (15, 16), (16, 17), (5, 18), (6, 19),
                                 (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27), (13, 28),
                                 (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]
        for (n1, n2) in expected_bronch_edges:
            node1 = self.network.node_list[n1]
            node2 = self.network.node_list[n2]
            self.assertTrue(self.network.has_edge(node1, node2))

        for a in range(0, 45):
            self.assertSequenceEqual(self.positions[a], self.network.node_list[a].position)

if __name__ == '__main__':
    unittest.main()
