__author__ = "Michael J. Pitcher"

from TBClasses import *
from TBEventProbabilityKeys import *
from ..PulmonaryAnatomy.LungLymphNetwork import *
from TBEvents.BacteriaReplicate import *
from TBEvents.BacteriumTranslocate import *
from TBEvents.BacteriumChangeMetabolism import *


class TBModel2(LungLymphMetapopulationNetwork):

    def __init__(self, parameters):

        population_keys = [BACTERIA_FAST, BACTERIA_SLOW]

        self.parameters = parameters

        events = []
        events.append(BacteriaReplication(BACTERIA_FAST, self.parameters[P_REPLICATION_BACTERIA_FAST]))
        events.append(BacteriaReplication(BACTERIA_SLOW, self.parameters[P_REPLICATION_BACTERIA_SLOW]))
        events.append(BacteriumTranslocateBronchus(BACTERIA_FAST, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST]))
        events.append(BacteriumTranslocateBronchus(BACTERIA_SLOW, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW]))
        events.append(BacteriumChangeMetabolism(BACTERIA_FAST, BACTERIA_SLOW, self.parameters[P_CHANGE_BACTERIA_FAST_TO_SLOW]))
        events.append(BacteriumChangeMetabolism(BACTERIA_SLOW, BACTERIA_FAST, self.parameters[P_CHANGE_BACTERIA_SLOW_TO_FAST]))

        LungLymphMetapopulationNetwork.__init__(self, population_keys, events)

    def load(self, fast_bacteria_to_load, slow_bacteria_to_load):
        for id in fast_bacteria_to_load:
            self.node_list[id].update(BACTERIA_FAST, fast_bacteria_to_load[id])
        for id in slow_bacteria_to_load:
            self.node_list[id].update(BACTERIA_SLOW, slow_bacteria_to_load[id])






