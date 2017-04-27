import unittest

from v8_ComMeN.ComMeN.TB.Events.DendriticCellTranslocation import *


class DendriticMatureLymphTranslocationTestCase(unittest.TestCase):
    def setUp(self):
        self.event = DendriticMatureLymphTranslocation(0.1)

    def test_initialise(self):
        self.assertTrue(isinstance(self.event, TranslocateLymph))
        self.assertItemsEqual(self.event.node_types, [BronchopulmonarySegment])
        self.assertEqual(self.event.translocate_compartment, DENDRITIC_CELL_MATURE)


if __name__ == '__main__':
    unittest.main()
