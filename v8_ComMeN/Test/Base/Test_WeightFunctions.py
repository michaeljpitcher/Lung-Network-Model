import unittest

from v8_ComMeN.ComMeN.Base.Network.WeightFunctions import *


class WeightFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_tree_weight_calculations(self):

        edges = [(0,1), (1,2), (1,3), (2,4), (4,5), (2,6), (6,7), (2,8), (3,9), (3,10), (9,11), (9,12), (10,13),
                 (10,14), (14,15)]

        expected_stahler = {(0,1):5, (1,2):3, (1,3):4, (2,4):2, (4,5):1, (2,6):2, (6,7):1, (2,8):1, (3,9):2, (3,10):3,
                            (9,11):1, (9,12):1, (10,13):1, (10,14):2, (14,15):1}

        weights_stahler = tree_weight_calculations(0, edges, STAHLER)
        for (u,v) in weights_stahler:
            if (u,v) in expected_stahler:
                self.assertEqual(weights_stahler[(u, v)], expected_stahler[(u, v)])
            else:
                self.assertEqual(weights_stahler[(u, v)], expected_stahler[(v, u)])

        expected_horsfield = {(0,1):3, (1,2):2, (1,3):3, (2,4):2, (4,5):1, (2,6):2, (6,7):1, (2,8):1, (3,9):2, (3,10):2,
                              (9,11):1, (9,12):1, (10,13):1, (10,14):2, (14,15):1}
        weights_horsfield = tree_weight_calculations(0, edges, HORSFIELD)
        for (u, v) in weights_horsfield:
            if (u, v) in expected_stahler:
                self.assertEqual(weights_horsfield[(u, v)], expected_horsfield[(u, v)])
            else:
                self.assertEqual(weights_horsfield[(u, v)], expected_horsfield[(v, u)])


if __name__ == '__main__':
    unittest.main()
