__author__ = "Michael J. Pitcher"

from ..Base.Patch import Patch


class BronchopulmonarySegment(Patch):
    """ A node within the bronchial tree of the human pulmonary system

    Contains spatial attributes:
    Ventilation - amount of air reaching the node through inhalation
    Perfusion - amount of blood vessels reaching node and thus amount of oxygen being removed
    Oxygen tension - ventilation/perfusion - amount of oxygen remaining at node
    """

    def __init__(self, patch_id, subpopulation_keys, position):
        Patch.__init__(self, patch_id, subpopulation_keys, position)
        # TODO - specifics of V, Q, V/Q
        # Spatial attrbiutes
        self.ventilation = ((10 - position[1]) * 0.05) + 0.2
        self.perfusion = ((10 - position[1]) * 0.09) + 0.1
        self.oxygen_tension = self.ventilation / self.perfusion

    def __str__(self):
        return "BPS: {0}".format(self.id)