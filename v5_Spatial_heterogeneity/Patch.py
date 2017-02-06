class Patch:
    """ A node within a metapopulation network, containing various subpopulations of defined species """

    def __init__(self, patch_id, subpopulations, attributes, position=(0, 0)):
        """

        :param patch_id: Unique identifier of the patch within the network
        :param subpopulations: Dictionary of subpopulations - keys=species, values=counts for each species
        :param attributes: Attributes of the patch environment
        :param position: Spatial coordinates of the patch
        """
        self.id = patch_id
        self.position = position
        self.subpopulations = subpopulations
        self.attributes = attributes

    def __str__(self):
        """ String identifier of patch"""
        return "Patch: " + str(self.id)
