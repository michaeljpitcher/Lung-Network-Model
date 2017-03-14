__author__ = "Michael J. Pitcher"

from TBClasses import *
from TBEventProbabilityKeys import *
from ..PulmonaryAnatomy.LungLymphNetwork import *
from TBEvents.Replication import *
from TBEvents.Translocation import *
from TBEvents.ChangeMetabolism import *
from TBEvents.Recruitment import *
from TBEvents.Ingestion import *
from TBEvents.Death import *


class TBModel3(LungLymphNetwork):

    def __init__(self, parameters):

        population_keys = [BACTERIA_FAST, BACTERIA_SLOW, MACROPHAGE]

        self.parameters = parameters

        events = []
        events.append(Replicate(BACTERIA_FAST, self.parameters[P_REPLICATION_BACTERIA_FAST]))
        events.append(Replicate(BACTERIA_SLOW, self.parameters[P_REPLICATION_BACTERIA_SLOW]))
        events.append(Translocate(BACTERIA_FAST, BRONCHUS, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST]))
        events.append(Translocate(BACTERIA_SLOW, BRONCHUS, self.parameters[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW]))
        events.append(ChangeMetabolism(BACTERIA_FAST, BACTERIA_SLOW, self.parameters[P_CHANGE_BACTERIA_FAST_TO_SLOW]))
        events.append(ChangeMetabolism(BACTERIA_SLOW, BACTERIA_FAST, self.parameters[P_CHANGE_BACTERIA_SLOW_TO_FAST]))
        events.append(Recruit(MACROPHAGE, BronchopulmonarySegment, self.parameters[P_RECRUITMENT_BPS_MACROPHAGE]))
        events.append(Recruit(MACROPHAGE, LymphNode, self.parameters[P_RECRUITMENT_LYMPH_MACROPHAGE]))
        events.append(Ingest(MACROPHAGE, BACTERIA_FAST, False, False, self.parameters[P_INGEST_AND_DESTROY_MACROPHAGE_FAST]))
        events.append(Ingest(MACROPHAGE, BACTERIA_SLOW, False, False, self.parameters[P_INGEST_AND_DESTROY_MACROPHAGE_SLOW]))
        events.append(Die(MACROPHAGE, self.parameters[P_DEATH_MACROPHAGE]))

        LungLymphNetwork.__init__(self, population_keys, events)

    def load(self, fast_bacteria_to_load, slow_bacteria_to_load, macrophages_to_load):
        for id in fast_bacteria_to_load:
            self.node_list[id].update(BACTERIA_FAST, fast_bacteria_to_load[id])
        for id in slow_bacteria_to_load:
            self.node_list[id].update(BACTERIA_SLOW, slow_bacteria_to_load[id])
        for id in macrophages_to_load:
            self.node_list[id].update(MACROPHAGE, macrophages_to_load[id])

