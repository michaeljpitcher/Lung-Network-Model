from ..Base.Patch import Patch

class LymphNode(Patch):

    def __init__(self, patch_id, species, loads, position):
        Patch.__init__(self, patch_id, species, loads, position)

    def __str__(self):
        return "LN {0}".format(self.id)
