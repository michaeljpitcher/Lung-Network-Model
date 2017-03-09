__author__ = "Michael J. Pitcher"

from Models.TB.TBModel1 import TBModel1
from Models.TB.TBClasses import *
from Models.TB.TBEventProbabilityKeys import *

params = {}
params[P_REPLICATION_BACTERIA] = 0.0
params[P_TRANSLOCATE_BRONCHUS_BACTERIA] = 10
model = TBModel1(params)

loads = {1: 10}

model.load(loads)
model.display([BACTERIA])
model.run(10)
model.display([BACTERIA])