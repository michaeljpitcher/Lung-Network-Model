__author__ = "Michael J. Pitcher"

from TBClasses import *
from TBEventProbabilityKeys import *
from ..PulmonaryAnatomy.LungLymphNetwork import *
from TBEvents.BacteriaReplicate import *
from TBEvents.BacteriumChangeMetabolism import *
from TBEvents.BacteriumTranslocate import *
from TBEvents.MacrophageRecruitment import *
from TBEvents.MacrophageIngestBacterium import *
from TBEvents.MacrophageDeath import *


class TBModel3(LungLymphMetapopulationNetwork):

    def __init__(self, parameters):

        population_keys = [BACTERIA_FAST, BACTERIA_SLOW, MACROPHAGE]

        self.parameters = parameters

        events = []
        events.append(BacteriaReplication(BACTERIA_FAST, self.parameters[P_REPLICATION_BACTERIA_FAST]))
        events.append(BacteriaReplication(BACTERIA_SLOW, self.parameters[P_REPLICATION_BACTERIA_SLOW]))
        events.append(BacteriumTranslocateBronchus(BACTERIA_FAST, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST]))
        events.append(BacteriumTranslocateBronchus(BACTERIA_SLOW, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW]))
        events.append(BacteriumChangeMetabolism(BACTERIA_FAST, BACTERIA_SLOW, self.parameters[P_CHANGE_BACTERIA_FAST_TO_SLOW]))
        events.append(BacteriumChangeMetabolism(BACTERIA_SLOW, BACTERIA_FAST, self.parameters[P_CHANGE_BACTERIA_SLOW_TO_FAST]))
        events.append(MacrophageRecruitmentRegularBPS(MACROPHAGE, self.parameters[P_RECRUITMENT_BPS_MACROPHAGE]))
        events.append(MacrophageRecruitmentRegularLymph(MACROPHAGE, self.parameters[P_RECRUITMENT_LYMPH_MACROPHAGE]))
        events.append(MacrophageIngestBacterium(BACTERIA_FAST, MACROPHAGE, self.parameters[P_INGEST_AND_DESTROY_MACROPHAGE_FAST], True))
        events.append(MacrophageIngestBacterium(BACTERIA_SLOW, MACROPHAGE, self.parameters[P_INGEST_AND_DESTROY_MACROPHAGE_SLOW], True))
        events.append(MacrophageDeath(MACROPHAGE, self.parameters[P_DEATH_MACROPHAGE]))

        LungLymphMetapopulationNetwork.__init__(self, population_keys, events)

    def load(self, fast_bacteria_to_load, slow_bacteria_to_load, macrophages_to_load):
        for id in fast_bacteria_to_load:
            self.node_list[id].update(BACTERIA_FAST, fast_bacteria_to_load[id])
        for id in slow_bacteria_to_load:
            self.node_list[id].update(BACTERIA_SLOW, slow_bacteria_to_load[id])
        for id in macrophages_to_load:
            self.node_list[id].update(MACROPHAGE, macrophages_to_load[id])

