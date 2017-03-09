__author__ = "Michael J. Pitcher"

from Models.TB.TBModel2 import TBModel2
from Models.TB.TBClasses import *
from Models.TB.TBEventProbabilityKeys import *

params = {}
params[P_REPLICATION_BACTERIA_FAST] = 0.0
params[P_REPLICATION_BACTERIA_SLOW] = 0.0
params[P_TRANSLOCATE_BRONCHUS_BACTERIA_FAST] = 0.0
params[P_TRANSLOCATE_BRONCHUS_BACTERIA_SLOW] = 0.0
params[P_CHANGE_BACTERIA_FAST_TO_SLOW] = 0.1
params[P_CHANGE_BACTERIA_SLOW_TO_FAST] = 0.0

model = TBModel2(params)

loads = {1: 10}

model.load(loads, {})
model.display([BACTERIA_FAST, BACTERIA_SLOW])
model.run(10)
model.display([BACTERIA_FAST, BACTERIA_SLOW])