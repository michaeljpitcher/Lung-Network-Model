__author__ = "Michael J. Pitcher"

from ...Base.Events.Create import *


class BacteriaReplication(Replication):

    def __init__(self, bacterium_type, probability):
        Replication.__init__(self, bacterium_type, probability)
