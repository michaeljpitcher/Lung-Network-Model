import unittest

from ..Models.PulmonaryAnatomy.LymphNode import *


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.non_terminal_ln = LymphNode(1, ['a'],(0,0))
        self.terminal_ln = LymphNode(1, ['a'], (0, 0), True)

    def test_something(self):
        self.assertTrue(self.terminal_ln.terminal)
        self.assertFalse(self.non_terminal_ln.terminal)


if __name__ == '__main__':
    unittest.main()
