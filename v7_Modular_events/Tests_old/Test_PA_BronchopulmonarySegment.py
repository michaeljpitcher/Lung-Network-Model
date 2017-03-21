import unittest

from ..Models.PulmonaryAnatomy.BronchopulmonarySegment import *


class BronchopulmonarySegmentTestCase(unittest.TestCase):
    def setUp(self):
        self.patch_id = 1
        self.keys = ('a','b')
        self.position = (5, 4)
        self.bps = BronchopulmonarySegment(self.patch_id, self.keys, self.position)

    def test_attributes(self):
        # TODO - amend later for realistic attributes
        self.assertEqual(self.bps.ventilation, ((10 - self.position[1]) * 0.05) + 0.2)
        self.assertEqual(self.bps.perfusion, ((10 - self.position[1]) * 0.09) + 0.1)
        expected_oxygen = (((10 - self.position[1]) * 0.05) + 0.2) / (((10 - self.position[1]) * 0.09) + 0.1)
        self.assertEqual(self.bps.oxygen_tension, expected_oxygen)

if __name__ == '__main__':
    unittest.main()
