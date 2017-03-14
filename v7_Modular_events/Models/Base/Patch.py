__author__ = "Michael J. Pitcher"


class Patch:
    """ A node within a metapopulation network

    Each Patch has subpopulation, consisting of different classes each with a count. Patch class can be subclassed to
    add specific spatial attributes
    """

    def __init__(self, patch_id, subpopulation_keys, position=(0, 0)):
        """

        :param patch_id: Unique identifier of the patch within the network
        :param subpopulation_keys: Keys for dictionary of subpopulations (i.e. species)
        :param position: Spatial coordinates of the patch
        """
        self.id = patch_id
        self.position = position
        self.subpopulations = dict()
        for class_type in subpopulation_keys:
            self.subpopulations[class_type] = 0

    def __str__(self):
        """ String identifier of patch"""
        return "Patch: " + str(self.id)

    def update(self, class_type, adjustment):
        """
        Alter the count for a class in the subpopulation of the patch
        :param class_type: Class type of subpopulation to adjust
        :param adjustment: Amount to adjust by
        :return:
        """
        # Check valid species and valid adjustment
        assert class_type in self.subpopulations.keys(), "update_node: Invalid species {0}".format(class_type)
        assert self.subpopulations[class_type] + adjustment >= 0, "update_node: Count cannot drop below zero"
        self.subpopulations[class_type] += adjustment
