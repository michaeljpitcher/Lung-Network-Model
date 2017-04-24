import unittest

from v8_ComMeN.ComMeN.Base.Node.Patch import *
from v8_ComMeN.ComMeN.Pulmonary.Events.PhagocyteTranslocate import *


class MacrophageTranslocationBaseFunctionTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_move_bacteria(self):
        mac = 'mac'
        bac = 'bac'

        node = Patch(0, [mac, bac])
        neighbour = Patch(1, [mac, bac])

        node.update_subpopulation(mac, 10)
        node.update_subpopulation(bac, 89)

        move_internals(node, neighbour, bac, mac)

        # Doesn't move macrophage, that's handled elsewhere
        self.assertEqual(node.subpopulations[mac], 10)
        self.assertEqual(node.subpopulations[bac], 89 - (int(round(89/10))))
        self.assertEqual(neighbour.subpopulations[bac], (int(round(89 / 10))))
        self.assertEqual(node.subpopulations[bac] + neighbour.subpopulations[bac], 89)


class MacrophageTranslocateBronchusTestCase(unittest.TestCase):

    def setUp(self):
        self.mac = 'mac'
        self.bac= 'bac'
        self.event_with_bac = PhagocyteTranslocateBronchus(None, 0.1, self.mac, False, self.bac)
        self.event_no_bac = PhagocyteTranslocateBronchus(None, 0.1, self.mac, False, None)

    def test_initialise(self):
        self.assertEqual(self.event_with_bac.internal_compartment_to_translocate, self.bac)
        self.assertEqual(self.event_no_bac.internal_compartment_to_translocate, None)

    def test_move(self):
        node = Patch(0, [self.mac, self.bac])
        neighbour = Patch(1, [self.mac, self.bac])
        node.update_subpopulation(self.mac, 6)
        node.update_subpopulation(self.bac, 13)
        self.event_with_bac.move(node, neighbour)
        self.assertEqual(node.subpopulations[self.mac], 5)
        self.assertEqual(node.subpopulations[self.bac], 11)
        self.assertEqual(neighbour.subpopulations[self.mac], 1)
        self.assertEqual(neighbour.subpopulations[self.bac], 2)

        node = Patch(0, [self.mac, self.bac])
        neighbour = Patch(1, [self.mac, self.bac])
        node.update_subpopulation(self.mac, 6)
        node.update_subpopulation(self.bac, 13)
        self.event_no_bac.move(node, neighbour)
        self.assertEqual(node.subpopulations[self.mac], 5)
        self.assertEqual(node.subpopulations[self.bac], 13)
        self.assertEqual(neighbour.subpopulations[self.mac], 1)
        self.assertEqual(neighbour.subpopulations[self.bac], 0)


class MacrophageTranslocateLymphTestCase(unittest.TestCase):

    def setUp(self):
        self.mac = 'mac'
        self.bac= 'bac'
        self.event_with_bac = PhagocyteTranslocateLymph(None, 0.1, self.mac, False, self.bac)
        self.event_no_bac = PhagocyteTranslocateLymph(None, 0.1, self.mac, False, None)

    def test_initialise(self):
        self.assertEqual(self.event_with_bac.internal_compartment_to_translocate, self.bac)
        self.assertEqual(self.event_no_bac.internal_compartment_to_translocate, None)

    def test_move(self):
        node = Patch(0, [self.mac, self.bac])
        neighbour = Patch(1, [self.mac, self.bac])
        node.update_subpopulation(self.mac, 6)
        node.update_subpopulation(self.bac, 13)
        self.event_with_bac.move(node, neighbour)
        self.assertEqual(node.subpopulations[self.mac], 5)
        self.assertEqual(node.subpopulations[self.bac], 11)
        self.assertEqual(neighbour.subpopulations[self.mac], 1)
        self.assertEqual(neighbour.subpopulations[self.bac], 2)

        node = Patch(0, [self.mac, self.bac])
        neighbour = Patch(1, [self.mac, self.bac])
        node.update_subpopulation(self.mac, 6)
        node.update_subpopulation(self.bac, 13)
        self.event_no_bac.move(node, neighbour)
        self.assertEqual(node.subpopulations[self.mac], 5)
        self.assertEqual(node.subpopulations[self.bac], 13)
        self.assertEqual(neighbour.subpopulations[self.mac], 1)
        self.assertEqual(neighbour.subpopulations[self.bac], 0)


class MacrophageTranslocateBloodTestCase(unittest.TestCase):

    def setUp(self):
        self.mac = 'mac'
        self.bac= 'bac'
        self.event_with_bac = PhagocyteTranslocateBlood(None, 0.1, self.mac, False, self.bac)
        self.event_no_bac = PhagocyteTranslocateBlood(None, 0.1, self.mac, False, None)

    def test_initialise(self):
        self.assertEqual(self.event_with_bac.internal_compartment_to_translocate, self.bac)
        self.assertEqual(self.event_no_bac.internal_compartment_to_translocate, None)

    def test_move(self):
        node = Patch(0, [self.mac, self.bac])
        neighbour = Patch(1, [self.mac, self.bac])
        node.update_subpopulation(self.mac, 6)
        node.update_subpopulation(self.bac, 13)
        self.event_with_bac.move(node, neighbour)
        self.assertEqual(node.subpopulations[self.mac], 5)
        self.assertEqual(node.subpopulations[self.bac], 11)
        self.assertEqual(neighbour.subpopulations[self.mac], 1)
        self.assertEqual(neighbour.subpopulations[self.bac], 2)

        node = Patch(0, [self.mac, self.bac])
        neighbour = Patch(1, [self.mac, self.bac])
        node.update_subpopulation(self.mac, 6)
        node.update_subpopulation(self.bac, 13)
        self.event_no_bac.move(node, neighbour)
        self.assertEqual(node.subpopulations[self.mac], 5)
        self.assertEqual(node.subpopulations[self.bac], 13)
        self.assertEqual(neighbour.subpopulations[self.mac], 1)
        self.assertEqual(neighbour.subpopulations[self.bac], 0)
