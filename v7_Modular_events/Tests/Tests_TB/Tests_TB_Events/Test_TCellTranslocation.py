import unittest

from v7_Modular_events.Models.TB.TBEvents.TCellTranslocation import *


class TCellTranslocateLymphTestCase(unittest.TestCase):
    def setUp(self):
        T_CELL = 't_cell'
        self.event = TCellTranslocateLymph(T_CELL, 0.1)

    def test_something(self):
        self.assertTrue(isinstance(self.event, TranslocateLymphatic))


if __name__ == '__main__':
    unittest.main()
