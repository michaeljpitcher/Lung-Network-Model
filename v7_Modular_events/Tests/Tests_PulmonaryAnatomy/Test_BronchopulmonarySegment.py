import unittest
from ...Models.PulmonaryAnatomy.BronchopulmonarySegment import *


class BronchopulmonarySegmentTestCase(unittest.TestCase):

    def setUp(self):
        self.keys = ['a']
        self.position = (7, 7)
        self.bps = BronchopulmonarySegment(0, self.keys, self.position)

    def test_initialise(self):
        self.assertEqual(self.bps.ventilation, ((10 - self.position[1]) * 0.05) + 0.2)
        self.assertEqual(self.bps.perfusion, ((10 - self.position[1]) * 0.09) + 0.1)
        self.assertEqual(self.bps.oxygen_tension, (((10 - self.position[1]) * 0.05) + 0.2) /
                         (((10 - self.position[1]) * 0.09) + 0.1))
