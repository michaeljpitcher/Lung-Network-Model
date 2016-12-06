import unittest
import V3_Metapop_edge_weighted.v3_Lung_network_metapop_edge_weight as MWN
import numpy as np
import math

class v3LungTestCaseHorsfield(unittest.TestCase):

    def setUp(self):
        self.network = MWN.LungMetapopulationWeighted('horsfield',[0, 7, 15], 100, 0.1, -0.2)


class v3LungTestCaseStahler(unittest.TestCase):

    def setUp(self):
        self.network = MWN.LungMetapopulationWeighted('stahler', [0, 7, 15], 100, 0.1, -0.2)
