import unittest

from v8_ComMeN.ComMeN.Pulmonary.Node.LungPatch import *


class LungPatchTestCase(unittest.TestCase):

    def setUp(self):
        self.drugs = ['I', 'R', 'P', 'E']
        self.patch = LungPatch(0, ['a','b'], (8,8), self.drugs)
        self.patch_no_drugs = LungPatch(0, ['a', 'b'], (8, 8), self.drugs)

    def test_initialise(self):
        self.assertItemsEqual(self.patch.chemotherapy.keys(), self.drugs)
        for d in self.drugs:
            self.assertEqual(self.patch.chemotherapy[d], 0.0)
