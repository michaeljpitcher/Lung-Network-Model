__author__ = "Michael J. Pitcher"

from unittest import TestCase
from ...Models.Base.Patch import *


class PatchTestCase(TestCase):

    def setUp(self):
        self._id = 1
        self.keys = ['a','b','c']
        self.position = (9, 8)
        self.patch = Patch(self._id, self.keys, self.position)

    def test_initialise(self):
        self.assertEqual(self.patch.id, self._id)
        self.assertItemsEqual(self.patch.subpopulations.keys(), self.keys)
        for key in self.keys:
            self.assertEqual(self.patch.subpopulations[key], 0)
        self.assertSequenceEqual(self.patch.position, self.position)
        self.assertTrue(isinstance(self.patch.degrees, dict))

    def test_update_correct(self):
        self.patch.update(self.keys[0], 1)
        self.assertEqual(self.patch.subpopulations[self.keys[0]], 1)

    def test_update_fail_wrong_key(self):
        wrong_key = 'fail'
        self.assertTrue(wrong_key not in self.keys)
        with self.assertRaises(AssertionError) as context:
            self.patch.update(wrong_key, 1)
        self.assertTrue("update_node: Invalid class " + wrong_key in context.exception)

    def test_update_fail_invalid_value(self):
        with self.assertRaises(AssertionError) as context:
            self.patch.update(self.keys[0], -1)
        self.assertTrue("update_node: Count cannot drop below zero" in context.exception)

    def test_type_per_type(self):
        self.patch.update(self.keys[0], 10)
        self.patch.update(self.keys[1], 5)
        self.patch.update(self.keys[2], 3)
        self.assertEqual(self.patch.type_per_type(self.keys[0], self.keys[1]), 2)
        self.assertEqual(self.patch.type_per_type(self.keys[0], self.keys[2]), 3)
        self.assertEqual(self.patch.type_per_type(self.keys[1], self.keys[2]), 1)
