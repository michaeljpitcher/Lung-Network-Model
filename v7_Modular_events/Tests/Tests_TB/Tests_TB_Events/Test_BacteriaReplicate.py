import unittest

from v7_Modular_events.Models.TB.TBEvents.BacteriaReplicate import *


class BacteriaReplicateTestCase(unittest.TestCase):
    def setUp(self):
        self.bac_type = 'a'
        self.prob = 0.1
        self.event = BacteriaReplication(self.bac_type, self.prob)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, Replication))

if __name__ == '__main__':
    unittest.main()
