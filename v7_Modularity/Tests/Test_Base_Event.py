import unittest

from ..Models.Base.Event import *

class EventTestCase(unittest.TestCase):

    def setUp(self):
        self.probability = 0.1
        self.event = Event(self.probability)

    def test_initialise(self):
        self.assertEqual(self.event.probability, self.probability)


if __name__ == '__main__':
    unittest.main()
