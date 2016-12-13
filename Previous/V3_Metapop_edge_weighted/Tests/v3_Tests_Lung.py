import unittest

from Previous import V3_Metapop_edge_weighted as MWN


class v3LungTestCaseHorsfield(unittest.TestCase):

    def setUp(self):
        self.network = MWN.LungMetapopulationWeighted('horsfield',[0, 7, 15], 100, 0.1, -0.2)


class v3LungTestCaseStahler(unittest.TestCase):

    def setUp(self):
        self.network = MWN.LungMetapopulationWeighted('stahler', [0, 7, 15], 100, 0.1, -0.2)
