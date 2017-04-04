import unittest

from v7_Modular_events.Models.TB.TBEvents.MacrophageTranslocation import *
from v7_Modular_events.Models.Base.Patch import *

class MacrophageTranslocateBronchusTestCase(unittest.TestCase):
    def setUp(self):
        self.event_has_intra = MacrophageTranslocateBronchus(MACROPHAGE_INFECTED, 0.1, True)
        self.event_no_intra = MacrophageTranslocateBronchus(MACROPHAGE_REGULAR, 0.1, True)

    def test_initialise(self):
        self.assertEqual(self.event_has_intra.move_by_edge_weight, True)

    def test_calculate_bacteria_moving(self):
        node = Patch(0, [MACROPHAGE_INFECTED, BACTERIA_INTRACELLULAR])
        node.update(MACROPHAGE_INFECTED, 10)
        node.update(BACTERIA_INTRACELLULAR, 54)

        has_intra_moves = self.event_has_intra.amounts_to_move(node)
        self.assertItemsEqual(has_intra_moves.keys(), [MACROPHAGE_INFECTED, BACTERIA_INTRACELLULAR])
        self.assertEqual(has_intra_moves[MACROPHAGE_INFECTED], 1)
        self.assertEqual(has_intra_moves[BACTERIA_INTRACELLULAR], int(round(54/10)))

        no_intra_moves = self.event_no_intra.amounts_to_move(node)
        self.assertItemsEqual(no_intra_moves.keys(), [MACROPHAGE_REGULAR])
        self.assertEqual(no_intra_moves[MACROPHAGE_REGULAR], 1)


if __name__ == '__main__':
    unittest.main()
