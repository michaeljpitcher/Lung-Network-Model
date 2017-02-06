import unittest
from v4_Compartmental import LungCompartmentalNetwork

class LungNetworkTestCase(unittest.TestCase):

    def setUp(self):

        loads = dict()
        loads[0] = {'A':1}
        loads[1] = {'B':2}
        loads[2] = {'A':3,'B':4}

        self.network_stahler = LungCompartmentalNetwork.LungNetwork(10, ['A', 'B'], loads, 'stahler')
        self.network_horsfield = LungCompartmentalNetwork.LungNetwork(10, ['A', 'B'], loads, 'horsfield')

    def test_initialise(self):
        self.assertEqual(len(self.network_horsfield.nodes()), 36)
        self.assertEqual(len(self.network_horsfield.edges()), 35)

        self.assertEqual(self.network_horsfield.origin, 0)

        self.assertItemsEqual([n.id for n in self.network_horsfield.terminal_nodes], range(18,36))

        # TODO - check edge weights


if __name__ == '__main__':
    unittest.main()
