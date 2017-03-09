__author__ = "Michael J. Pitcher"

from TBClasses import *
from TBEventProbabilityKeys import *
from ..PulmonaryAnatomy.LungLymphNetwork import *
from TBEvents.Replication import *
from TBEvents.Translocation import *


class TBModel1(LungLymphNetwork):

    def __init__(self, parameters):

        population_keys = [BACTERIA]

        self.parameters = parameters

        events = []
        events.append(Replication(BACTERIA, self.parameters[P_REPLICATION_BACTERIA]))
        events.append(Translocation(BACTERIA, BRONCHUS, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA]))

        LungLymphNetwork.__init__(self, population_keys, events)

    def load(self, bacteria_to_load):
        for id in bacteria_to_load:
            self.node_list[id].update(BACTERIA, bacteria_to_load[id])

