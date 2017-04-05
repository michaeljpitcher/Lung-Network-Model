import unittest

from v8_Events_at_nodes.Models.Base.Node.Patch import *


class PatchTestCase(unittest.TestCase):
    def setUp(self):
        self.compartments = ['a','b','c']
        self.position = (6, 7)
        self.patch = Patch(self.compartments, self.position)

    def test_initialise(self):
        self.assertItemsEqual(self.patch.subpopulations.keys(), self.compartments)
        for key in self.patch.subpopulations:
            self.assertEqual(self.patch.subpopulations[key], 0)
        self.assertSequenceEqual(self.patch.position, self.position)

    def test_update_subpopulation(self):
        self.patch.update_subpopulation(self.compartments[0], 1)
        self.assertEqual(self.patch.subpopulations[self.compartments[0]], 1)

        # Fail wrong key
        with self.assertRaises(AssertionError) as context:
            self.patch.update_subpopulation('FAIL', 1)
        self.assertEqual('Invalid compartment FAIL for update', str(context.exception))

    def test_compartment_per_compartment(self):
        self.patch.update_subpopulation(self.compartments[0], 10)
        self.patch.update_subpopulation(self.compartments[1], 3)
        self.assertEqual(self.patch.compartment_per_compartment(self.compartments[0], self.compartments[1]), 3)


if __name__ == '__main__':
    unittest.main()
