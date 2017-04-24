#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Pulmonary.Network.PulmonaryAnatomyNetwork import *
from ..TBClasses import *
import inspect
import sys
import pkgutil

from .. import Events

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class TBModelFull(PulmonaryAnatomyNetwork):

    def __init__(self, initial_macrophages_bps, initial_macrophages_btn, initial_macrophages_lymph,
                 initial_bacteria_fast, initial_bacteria_slow, probabilities,
                 include_bronchials, include_lymphatics, include_bloodstream,
                 tree_weight_method=HORSFIELD):

        compartments = [BACTERIA_FAST, BACTERIA_SLOW, BACTERIA_INTRACELLULAR] + \
                       [MACROPHAGE_REGULAR, MACROPHAGE_INFECTED, MACROPHAGE_ACTIVATED] + \
                       [T_CELL_HELPER, T_CELL_CYTOTOXIC]

        # TODO - not the nicest code but this does work. Maybe find better way to import (i.e. Event subclasses?)
        package = Events
        prefix = package.__name__ + "."
        # Look in each module for classes
        event_classes = []
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            #print "Importing event module: {0} and searching for classes...".format(modname)
            __import__(modname)
            event_classes += inspect.getmembers(sys.modules[modname], lambda member: inspect.isclass(member) and
                                                               member.__module__ == modname)

        # Using class name and class, add event (class name is probability key)
        events = []
        skipped_events = []
        for (prob_key, event_class) in event_classes:
            if prob_key in probabilities:
                events.append(event_class(probabilities[prob_key]))
            else:
                skipped_events.append(prob_key)

        print "Events without probabilities skipped: {0}".format(skipped_events)

        PulmonaryAnatomyNetwork.__init__(self, compartments, events,
                                         bronchial_tree_nodes=include_bronchials,
                                         bronchial_tree_weight_method=tree_weight_method,
                                         lymphatic_nodes=include_lymphatics,
                                         haematogenous_reseeding=include_bloodstream)

        self.seed_network_node_type(BronchopulmonarySegment, {MACROPHAGE_REGULAR: initial_macrophages_bps})
        self.seed_network_node_type(BronchialTreeNode, {MACROPHAGE_REGULAR: initial_macrophages_btn})
        self.seed_network_node_type(LymphNode, {MACROPHAGE_REGULAR: initial_macrophages_lymph})

        for node_id in initial_bacteria_fast:
            seeding = {BACTERIA_FAST: initial_bacteria_fast[node_id]}
            self.seed_network_node_id(node_id, seeding)
        for node_id in initial_bacteria_slow:
            seeding = {BACTERIA_SLOW: initial_bacteria_slow[node_id]}
            self.seed_network_node_id(node_id, seeding)
