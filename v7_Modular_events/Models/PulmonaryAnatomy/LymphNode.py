__author__ = "Michael J. Pitcher"

from ..Base.Patch import Patch


class LymphNode(Patch):

    def __init__(self, patch_id, species, position, terminal=False):
        self.terminal = terminal
        Patch.__init__(self, patch_id, species, position)

    def __str__(self):
        return "LN: {0}".format(self.id)
