from v5_Spatial_heterogeneity.Base.MetapopulationNetwork import Patch


class LymphNode(Patch):
    """ A node within a the lung, representing a bronchopulmonary segment of the bronchial tree """

    def __init__(self, patch_id, subpopulation_keys, loads, position):
        """

        :param patch_id: Unique identifier of the patch within the network
        :param subpopulation_keys: Keys for dictionary of subpopulations (i.e. species)
        :param position: Spatial coordinates of the patch
        """
        Patch.__init__(self, patch_id, subpopulation_keys, loads, position)
        self.drainage = []
        self.lymphatic_vessels = []

    def __str__(self):
        """ String identifier of patch"""
        return "Lymph Node: " + str(self.id)
