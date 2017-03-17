__author__ = "Michael J. Pitcher"

from ...Base.Events.Create import *


class BacteriaReplication(Create):

    def __init__(self, bacterium_type, probability):
        Create.__init__(self, bacterium_type, probability)
