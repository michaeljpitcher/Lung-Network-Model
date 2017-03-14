import unittest

from ..Models.Base.Patch import *


class PatchTestCase(unittest.TestCase):

    def setUp(self):
        self._id = 0
        self.keys = ['a','b','c']
        self.pos = (8, 8)
        self.patch = Patch(self._id, self.keys, self.pos)

    def test_initialise(self):
        self.assertEqual(self.patch.id, self._id)
        self.assertItemsEqual(self.patch.subpopulations.keys(), self.keys)
        self.assertItemsEqual(self.patch.subpopulations.values(), [0, ]*len(self.keys))
        self.assertSequenceEqual(self.patch.position, self.pos)

    def test_update_correct(self):
        self.patch.update(self.keys[0], 1)
        self.assertEqual(self.patch.subpopulations[self.keys[0]], 1)

    def test_update_fail_class(self):
        with self.assertRaises(AssertionError) as context:
            self.patch.update(None, 1)
        self.assertTrue('update_node: Invalid class None' in context.exception)

    def test_update_fail_adjustment(self):
        with self.assertRaises(AssertionError) as context:
            self.patch.update(self.keys[0], -1)
        self.assertTrue('update_node: Count cannot drop below zero' in context.exception)

if __name__ == '__main__':
    unittest.main()
