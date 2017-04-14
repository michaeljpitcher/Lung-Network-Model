import unittest
from v8_ComMeN.ComMeN.Base.Events.Destruction import *
from v8_ComMeN.ComMeN.Base.Node.Patch import *


class DestroyTestCase(unittest.TestCase):
    def setUp(self):
        self.compartment = 'a'
        self.event = Destroy(None, 0.1, self.compartment)

    def test_initialise(self):
        self.assertEqual(self.event.compartment_destroyed, self.compartment)

    def test_increment_from_node(self):
        node = Patch(0, [self.compartment])
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.compartment, 12)
        self.assertEqual(self.event.increment_from_node(node, None), 12)

    def test_update_node(self):
        node = Patch(0, [self.compartment])
        node.update_subpopulation(self.compartment, 12)
        self.event.update_node(node, None)
        self.assertEqual(self.event.increment_from_node(node, None), 11)


if __name__ == '__main__':
    unittest.main()
