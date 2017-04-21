#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Pulmonary.Network.PulmonaryAnatomyNetwork import *
from ..TBClasses import *
import inspect
import sys
import os

from ..EventsWithCompartments import *



__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBModelFull(PulmonaryAnatomyNetwork):

    def __init__(self, initial_macrophages_bps, initial_macrophages_tbn, initial_macrophages_lymph,
                 initial_bacteria_fast, initial_bacteria_slow, probabilities,
                 include_bronchials, include_lymphatics, include_bloodstream,
                 tree_weight_method=HORSFIELD):

        compartments = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR] + \
                       [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED] + \
                       [T_CELL]

        # TODO - not the nicest code but this does work. Maybe find better way to import (i.e. Event subclasses?)
        # Get all modules within the EventsWithCompartments directory (based on files ending py
        event_modules = ['ComMeN.TB.EventsWithCompartments.' + p[0:-3] for p in
                         os.listdir("ComMeN/TB/EventsWithCompartments") if p.endswith('.py') and p != '__init__.py']

        # Look in each module for classes
        event_classes = []
        for module in event_modules:
            event_classes += inspect.getmembers(sys.modules[module], lambda member: inspect.isclass(member) and
                                                                                    member.__module__ == module)

        # Using class name and class, add event (class name is probability key)
        events = []
        for (prob_key, event_class) in event_classes:
            if prob_key in probabilities:
                events.append(event_class(probabilities[prob_key]))
            else:
                print "Event {0} probability not defined, skipping".format(prob_key)

        PulmonaryAnatomyNetwork.__init__(self, compartments, events,
                                         bronchial_tree_nodes=include_bronchials,
                                         bronchial_tree_weight_method=tree_weight_method,
                                         lymphatic_nodes=include_lymphatics,
                                         haematogenous_reseeding=include_bloodstream)

        seeding = dict()



        self.seed_network(seeding)