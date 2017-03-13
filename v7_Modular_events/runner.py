__author__ = "Michael J. Pitcher"

from Models.TB.TBModel3 import TBModel3
from Models.TB.TBClasses import *
from Models.TB.TBEventProbabilityKeys import *

params = {}
params[P_REPLICATION_BACTERIA_FAST] = 0.1
params[P_REPLICATION_BACTERIA_SLOW] = 0.1
params[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST] = 0.1
params[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW] = 0.1
params[P_CHANGE_BACTERIA_FAST_TO_SLOW] = 0.1
params[P_CHANGE_BACTERIA_SLOW_TO_FAST] = 0.1
params[P_INGEST_AND_DESTROY_MACROPHAGE_FAST] = 0.1
params[P_INGEST_AND_DESTROY_MACROPHAGE_SLOW] = 0.1
params[P_RECRUITMENT_BPS_MACROPHAGE] = 0.1
params[P_RECRUITMENT_LYMPH_MACROPHAGE] = 0.1
params[P_DEATH_MACROPHAGE] = 0.1

model = TBModel3(params)

loads_f = {1: 0}
loads_s = {2: 0}
loads_m = {3: 10}

model.load(loads_f, loads_s, loads_m)
model.display([])
# model.run(10)
# model.display([BACTERIA_FAST, BACTERIA_SLOW, MACROPHAGE])