from ..Base.Patch import Patch

class BronchopulmonarySegment(Patch):

    def __init__(self, patch_id, species, loads, position):
        Patch.__init__(self, patch_id, species, loads, position)
        # TODO - specifics of V, Q, V/Q
        self.ventilation = ((10 - position[1]) * 0.05) + 0.2
        self.perfusion = ((10 - position[1]) * 0.09) + 0.1
        self.oxygen_tension = self.ventilation / self.perfusion

    def __str__(self):
        return "BPS {0}".format(self.id)