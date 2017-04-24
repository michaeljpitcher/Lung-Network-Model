import unittest

from v8_ComMeN.ComMeN.Base.Node.Patch import *
from v8_ComMeN.ComMeN.Pulmonary.Events.PhagocyteActivation import *


class PhagocyteActivationTestCase(unittest.TestCase):

    def setUp(self):
        self.mac_reg = 'mac_a'
        self.mac_act = 'mac_b'
        self.bac_int = 'bac_i'
        self.event_no_bac = PhagocyteActivation(None, 0.1, self.mac_reg, self.mac_act)
        self.event_with_bac = PhagocyteActivation(None, 0.1, self.mac_reg, self.mac_act, self.bac_int)

    def test_initialise(self):
        self.assertEqual(self.event_no_bac.bacteria_compartment_destroy, None)
        self.assertEqual(self.event_with_bac.bacteria_compartment_destroy, self.bac_int)

    def test_update_node(self):
        node = Patch(0, [self.mac_reg, self.mac_act, self.bac_int])
        node.update_subpopulation(self.mac_reg, 10)
        node.update_subpopulation(self.bac_int, 100)

        self.event_no_bac.update_node(node, None)

        self.assertEqual(node.subpopulations[self.mac_reg], 9)
        self.assertEqual(node.subpopulations[self.mac_act], 1)
        self.assertEqual(node.subpopulations[self.bac_int], 100)

        node = Patch(0, [self.mac_reg, self.mac_act, self.bac_int])
        node.update_subpopulation(self.mac_reg, 10)
        node.update_subpopulation(self.bac_int, 100)

        self.event_with_bac.update_node(node, None)

        self.assertEqual(node.subpopulations[self.mac_reg], 9)
        self.assertEqual(node.subpopulations[self.mac_act], 1)
        self.assertEqual(node.subpopulations[self.bac_int], 100 - (100/10))


class PhagocyteActivationByExternalsTestCase(unittest.TestCase):

    def setUp(self):
        self.mac_reg = 'mac_a'
        self.mac_act = 'mac_b'
        self.t_cell_comps = ['inf_a', 'inf_b']
        self.event = PhagocyteActivationByExternals(None, 0.1, self.mac_reg, self.mac_act, self.t_cell_comps)

    def test_initialise(self):
        self.assertItemsEqual(self.event.external_compartments, self.t_cell_comps)

    def test_increment_from_node(self):
        node = Patch(0, [self.mac_reg, self.mac_act] + self.t_cell_comps)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.mac_reg, 10)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.t_cell_comps[0], 1)
        self.assertEqual(self.event.increment_from_node(node, None), 10 * 1)
        node.update_subpopulation(self.t_cell_comps[1], 2)
        self.assertEqual(self.event.increment_from_node(node, None), 10 * (1+2))


class PhagocyteDeactivationByLackOfExternalsTestCase(unittest.TestCase):

    def setUp(self):
        self.mac_reg = 'mac_a'
        self.mac_act = 'mac_b'
        self.inf_comps = ['inf_a', 'inf_b']
        self.event = PhagocyteDeactivationByLackOfExternals(None, 0.1, self.mac_act, self.mac_reg, self.inf_comps)

    def test_initialise(self):
        self.assertItemsEqual(self.event.external_compartments, self.inf_comps)

    def test_increment_from_node(self):
        node = Patch(0, [self.mac_reg, self.mac_act] + self.inf_comps)
        self.assertEqual(self.event.increment_from_node(node, None), 0)
        node.update_subpopulation(self.mac_act, 10)
        self.assertEqual(self.event.increment_from_node(node, None), 10 * (1 / 0.00000001))
        node.update_subpopulation(self.inf_comps[0], 1)
        self.assertEqual(self.event.increment_from_node(node, None), 10 * (1 / 1))
        node.update_subpopulation(self.inf_comps[1], 2)
        self.assertEqual(self.event.increment_from_node(node, None), 10 * (1 / (1+2)))
