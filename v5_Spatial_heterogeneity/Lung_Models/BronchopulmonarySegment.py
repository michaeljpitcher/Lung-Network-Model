from v5_Spatial_heterogeneity.Base.MetapopulationNetwork import Patch


class BronchopulmonarySegment(Patch):
    """ A node within a the lung, representing a bronchopulmonary segment of the bronchial tree """

    def __init__(self, patch_id, subpopulation_keys, position, ventilation, perfusion, oxygen_tension):
        """

        :param patch_id: Unique identifier of the patch within the network
        :param subpopulation_keys: Keys for dictionary of subpopulations (i.e. species)
        :param position: Spatial coordinates of the patch
        """
        Patch.__init__(self, patch_id, subpopulation_keys, position)
        self.ventilation = ventilation
        self.perfusion = perfusion
        self.oxygen_tension = oxygen_tension

    def __str__(self):
        """ String identifier of patch"""
        return "Patch: " + str(self.id)
