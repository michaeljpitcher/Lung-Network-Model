import unittest

from v7_Modular_events.Models.TB.TBEvents.BacteriumChangeMetabolism import *
from v7_Modular_events.Models.TB.TBClasses import *


class BacChangeMetabolismTestCase(unittest.TestCase):
    def setUp(self):
        self.event_fast_to_slow = BacteriumChangeMetabolism(BACTERIA_FAST, BACTERIA_SLOW, 0.1)
        self.event_slow_to_fast = BacteriumChangeMetabolism(BACTERIA_SLOW, BACTERIA_FAST, 0.1)

    def test_initialise(self):
        self.assertFalse(self.event_fast_to_slow.oxygen_high)
        self.assertTrue(self.event_slow_to_fast.oxygen_high)

    def test_invalid_metabolisms(self):
        with self.assertRaises(Exception) as context:
            event = BacteriumChangeMetabolism(BACTERIA_FAST, BACTERIA_INTRACELLULAR, 0.1)
        self.assertEqual('Invalid bacteria types {0}, {1}'.format(BACTERIA_FAST, BACTERIA_INTRACELLULAR),
                         str(context.exception))
        with self.assertRaises(Exception) as context:
            event = BacteriumChangeMetabolism(BACTERIA_INTRACELLULAR, BACTERIA_SLOW, 0.1)
        self.assertEqual('Invalid bacteria types {0}, {1}'.format(BACTERIA_INTRACELLULAR, BACTERIA_SLOW),
                        str(context.exception))

if __name__ == '__main__':
    unittest.main()
