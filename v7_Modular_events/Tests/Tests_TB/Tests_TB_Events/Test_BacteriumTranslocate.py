import unittest
from v7_Modular_events.Models.TB.TBEvents.BacteriumTranslocate import *


class BacteriumTranslocateTestCase(unittest.TestCase):
    def setUp(self):
        self.event_edge_weight = BacteriumTranslocateBronchus('BACTERIUM', 0.1, True)
        self.event_not_edge_weight = BacteriumTranslocateBronchus('BACTERIUM', 0.1, False)

    def test_initialise(self):
        self.assertTrue(self.event_edge_weight.move_by_edge_weight)
        self.assertFalse(self.event_not_edge_weight.move_by_edge_weight)


if __name__ == '__main__':
    unittest.main()
