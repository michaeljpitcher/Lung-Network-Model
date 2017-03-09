__author__ = "Michael J. Pitcher"

from TBClasses import *
from TBEventProbabilityKeys import *
from ..PulmonaryAnatomy.LungLymphNetwork import *
from TBEvents.Replication import *
from TBEvents.Translocation import *
from TBEvents.ChangeMetabolism import *


class TBModel2(LungLymphNetwork):

    def __init__(self, parameters):

        population_keys = [BACTERIA_FAST, BACTERIA_SLOW]

        self.parameters = parameters

        events = []
        events.append(Replication(BACTERIA_FAST, self.parameters[P_REPLICATION_BACTERIA_FAST]))
        events.append(Replication(BACTERIA_SLOW, self.parameters[P_REPLICATION_BACTERIA_SLOW]))
        events.append(Translocation(BACTERIA_FAST, BRONCHUS, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST]))
        events.append(Translocation(BACTERIA_SLOW, BRONCHUS, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW]))
        events.append(ChangeMetabolism(BACTERIA_FAST, BACTERIA_SLOW, self.parameters[P_CHANGE_BACTERIA_FAST_TO_SLOW]))
        events.append(ChangeMetabolism(BACTERIA_SLOW, BACTERIA_FAST, self.parameters[P_CHANGE_BACTERIA_SLOW_TO_FAST]))

        LungLymphNetwork.__init__(self, population_keys, events)

    def load(self, fast_bacteria_to_load, slow_bacteria_to_load):
        for id in fast_bacteria_to_load:
            self.node_list[id].update(BACTERIA_FAST, fast_bacteria_to_load[id])
        for id in slow_bacteria_to_load:
            self.node_list[id].update(BACTERIA_SLOW, slow_bacteria_to_load[id])

