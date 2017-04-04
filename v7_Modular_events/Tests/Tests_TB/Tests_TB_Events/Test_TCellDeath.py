import unittest

from v7_Modular_events.Models.TB.TBEvents.TCellDeath import *
from v7_Modular_events.Models.TB.TBClasses import *


class TCellDeathTestCase(unittest.TestCase):
    def setUp(self):
        self.event = TCellDeath(T_CELL, 0.1)

    def test_something(self):
        self.assertTrue(isinstance(self.event, Die))

if __name__ == '__main__':
    unittest.main()
