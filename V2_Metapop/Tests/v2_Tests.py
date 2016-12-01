import unittest
import V1_SIR.v2_Lung_network_metapopulation as MetapopNetwork
import numpy as np


class v2TestCase(unittest.TestCase):

    def setUp(self):
        self.network = MetapopNetwork.LungNetwork([0,1,3],10,0.2,0.1,100)



if __name__ == '__main__':
    unittest.main()
