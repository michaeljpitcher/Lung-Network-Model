import unittest

from v8_ComMeN.ComMeN.TB.Events.MacrophageRecruitment import *
from v8_ComMeN.ComMeN.Pulmonary.Node.BronchopulmonarySegment import *


class MacrophageRecruitmentBronchialByInfectionTestCase(unittest.TestCase):
    def setUp(self):
        self.mac = 'mac'
        self.infs = ['inf_1', 'inf_2']
        self.event_not_perf = MacrophageRecruitmentBronchialByInfection(0.1, self.mac, self.infs, False)
        self.event_perf = MacrophageRecruitmentBronchialByInfection(0.1, self.mac, self.infs, True)


    def test_initialise(self):
        self.assertItemsEqual(self.event_not_perf.infection_compartments, self.infs)

    def test_increment_from_node(self):
        node = BronchopulmonarySegment(0, [self.mac] + self.infs, 0.1, 0.1, (8,8))
        self.assertEqual(self.event_not_perf.increment_from_node(node, None), 0)
        node.update_subpopulation(self.infs[0], 5)
        self.assertEqual(self.event_not_perf.increment_from_node(node, None), 5)
        node.update_subpopulation(self.infs[1], 7)
        self.assertEqual(self.event_not_perf.increment_from_node(node, None), (5 + 7))

        node = BronchopulmonarySegment(0, [self.mac] + self.infs, 0.1, 0.1, (8, 8))
        self.assertEqual(self.event_perf.increment_from_node(node, None), 0)
        node.update_subpopulation(self.infs[0], 5)
        self.assertEqual(self.event_perf.increment_from_node(node, None), 0.1 * 5)
        node.update_subpopulation(self.infs[1], 7)
        self.assertEqual(self.event_perf.increment_from_node(node, None), 0.1 * (5 + 7))


if __name__ == '__main__':
    unittest.main()
