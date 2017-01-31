import unittest
from v4_Compartmental import TBFastAndSlow
import numpy as np

class FastSlowTestCase(unittest.TestCase):

    def setUp(self):

        self.rates = {}
        self.rates['p_transmit_F'] = 0.1
        self.rates['p_transmit_S'] = 0.1
        self.rates['p_growth_F'] = 0.1
        self.rates['p_growth_S'] = 0.1
        self.rates['p_change_F_to_S'] = 0.1
        self.rates['p_change_S_to_F'] = 0.1

        limit = 100

        self.loads_fast = dict()
        self.loads_fast[0] = 10
        self.loads_fast[1] = 7

        self.loads_slow = dict()
        self.loads_slow[15] = 1
        self.loads_slow[16] = 4

        self.model = TBFastAndSlow.TBFastSlowMetapopulationNetwork(self.rates, limit, self.loads_fast, self.loads_slow)


    def test_initialise(self):
        # Loads
        for node in self.model.nodes():
            if node.id in self.loads_fast:
                self.assertEqual(node.counts['F'], self.loads_fast[node.id])
            else:
                self.assertEqual(node.counts['F'], 0)
            if node.id in self.loads_slow:
                self.assertEqual(node.counts['S'], self.loads_slow[node.id])
            else:
                self.assertEqual(node.counts['S'], 0)

        self.assertItemsEqual(self.model.rates.keys(), self.rates.keys())
        for r in self.model.rates:
            self.assertEqual(self.model.rates[r], self.rates[r])

    def test_update_totals(self):
        self.model.update_totals()
        self.assertEqual(self.model.total_f, sum(self.loads_fast.values()))
        self.assertEqual(self.model.total_s, sum(self.loads_slow.values()))

        self.assertEqual(self.model.total_transmit_f, 10*1 + 7*3)
        self.assertEqual(self.model.total_transmit_s, 1*3 + 4*3)

    def test_transmit_F(self):
        np.random.seed(101)
        self.model.update_totals()
        self.model.transmit('F')
        self.assertEqual(self.model.node_list[1].counts['F'], 6)
        self.assertEqual(self.model.node_list[2].counts['F'], 1)

    def test_transmit_S(self):
        np.random.seed(10111)
        self.model.update_totals()
        self.model.transmit('S')
        self.assertEqual(self.model.node_list[16].counts['S'], 3)
        self.assertEqual(self.model.node_list[15].counts['S'], 2)

    def test_growth_F_pos(self):
        np.random.seed(101)
        self.model.update_totals()
        self.model.growth('F')
        self.assertEqual(self.model.node_list[0].counts['F'], 11)

    def test_growth_F_neg(self):
        np.random.seed(10111)
        self.model.rates['p_growth_F'] = -0.1
        self.model.update_totals()
        self.model.growth('F')
        self.assertEqual(self.model.node_list[1].counts['F'], 6)

    def test_growth_S_pos(self):
        np.random.seed(101)
        self.model.update_totals()
        self.model.growth('S')
        self.assertEqual(self.model.node_list[16].counts['S'], 5)

    def test_growth_S_neg(self):
        np.random.seed(23466)
        self.model.rates['p_growth_S'] = -0.1
        self.model.update_totals()
        self.model.growth('S')
        self.assertEqual(self.model.node_list[15].counts['S'], 0)

    def test_change_F_to_S(self):
        np.random.seed(101)
        self.model.update_totals()
        self.model.change('F','S')
        self.assertEqual(self.model.node_list[0].counts['F'], 9)
        self.assertEqual(self.model.node_list[0].counts['S'], 1)

    def test_change_S_to_F(self):
        np.random.seed(101)
        self.model.update_totals()
        self.model.change('S','F')
        self.assertEqual(self.model.node_list[16].counts['S'], 3)
        self.assertEqual(self.model.node_list[16].counts['F'], 1)


if __name__ == '__main__':
    unittest.main()
