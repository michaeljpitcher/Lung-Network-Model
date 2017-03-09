__author__ = "Michael J. Pitcher"

from TBClasses import *
from ..PulmonaryAnatomy.LungLymphNetwork import *
from TBEvents.Replication import *
from TBEvents.Translocation import *


class TBModel1(LungLymphNetwork):

    def __init__(self, parameters):

        population_keys = [BACTERIA]

        self.parameters = parameters

        events = []
        events.append(Replication(BACTERIA_FAST, self.parameters[P_REPLICATION_BACTERIA_FAST]))
        events.append(Replication(BACTERIA_SLOW, self.parameters[P_REPLICATION_BACTERIA_SLOW]))
        events.append(Translocation(BACTERIA_FAST, BRONCHUS, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST]))
        events.append(Translocation(BACTERIA_SLOW, BRONCHUS, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW]))

        LungLymphNetwork.__init__(self, population_keys, events)