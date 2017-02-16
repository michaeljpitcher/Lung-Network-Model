class Patch:
    """ A node within a metapopulation network, containing various subpopulations of defined species """

    def __init__(self, patch_id, subpopulation_keys, loads, position=(0, 0)):
        """

        :param patch_id: Unique identifier of the patch within the network
        :param subpopulation_keys: Keys for dictionary of subpopulations (i.e. species)
        :param position: Spatial coordinates of the patch
        """
        self.id = patch_id
        self.position = position
        self.subpopulations = dict()
        for species in subpopulation_keys:
            if species in loads:
                self.subpopulations[species] = loads[species]
            else:
                self.subpopulations[species] = 0
        self.degree = 0

    def __str__(self):
        """ String identifier of patch"""
        return "Patch: " + str(self.id)
