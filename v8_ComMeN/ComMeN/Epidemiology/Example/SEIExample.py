#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

from ...Base.Network.MetapopulationNetwork import *
from ..EpidemiologyClasses import *
from ...Base.Events.Creation import *
from ...Base.Events.Destruction import *
from ...Base.Events.Change import *
from ...Base.Events.Translocate import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"


class EgPatch(Patch):

    def __init__(self, node_id, compartments, birth, death, contact, infect, progress, recover, move, death_disease, p_infectious):
        self.birth = birth
        self.death = death
        self.contact = contact
        self.infect = infect
        self.progress = progress
        self.recover = recover
        self.move = move
        self.death_disease = death_disease
        self.p_infectious = p_infectious
        Patch.__init__(self, node_id, compartments)


class EgBirth(CreateByOtherCompartments):
    def __init__(self):
        CreateByOtherCompartments.__init__(self, [EgPatch], 1, SUSCEPTIBLE, [SUSCEPTIBLE, INFECTIOUS, LATENT])

    def increment_state_variable_from_node(self, node, network):
        return node.birth * CreateByOtherCompartments.increment_state_variable_from_node(self, node, network)


class EgDeath(Destroy):
    def __init__(self, compartment):
        Destroy.__init__(self, [EgPatch], 1, compartment)

    def increment_state_variable_from_node(self, node, network):
        return node.death * Destroy.increment_state_variable_from_node(self, node, network)


class EgDeathDisease(Destroy):
    def __init__(self):
        Destroy.__init__(self, [EgPatch], 1, INFECTIOUS)

    def increment_state_variable_from_node(self, node, network):
        return node.death_disease * Destroy.increment_state_variable_from_node(self, node, network)


class EgInfectLatent(ChangeByOtherCompartments):
    def __init__(self):
        ChangeByOtherCompartments.__init__(self, [EgPatch], 1, SUSCEPTIBLE, LATENT, [INFECTIOUS])

    def increment_state_variable_from_node(self, node, network):
        return (1 - node.p_infectious) * node.contact * node.infect * \
               ChangeByOtherCompartments.increment_state_variable_from_node(self, node, network)


class EgInfectInfectious(ChangeByOtherCompartments):
    def __init__(self):
        ChangeByOtherCompartments.__init__(self, [EgPatch], 1, SUSCEPTIBLE, INFECTIOUS, [INFECTIOUS])

    def increment_state_variable_from_node(self, node, network):
        return node.p_infectious * node.contact * node.infect * \
               ChangeByOtherCompartments.increment_state_variable_from_node(self, node, network)


class EgProgress(Change):
    def __init__(self):
        Change.__init__(self, [EgPatch], 1, LATENT, INFECTIOUS)

    def increment_state_variable_from_node(self, node, network):
        return node.progress * Change.increment_state_variable_from_node(self, node, network)


class EgRecover(Change):
    def __init__(self):
        Change.__init__(self, [EgPatch], 1, INFECTIOUS, SUSCEPTIBLE)

    def increment_state_variable_from_node(self, node, network):
        return node.recover * Change.increment_state_variable_from_node(self, node, network)


class EgMigrate(Translocate):
    def __init__(self, compartment):
        Translocate.__init__(self, [EgPatch], 1, compartment, STANDARD_EDGE)

    def increment_state_variable_from_node(self, node, network):
        return node.move * Translocate.increment_state_variable_from_node(self, node, network)


class EgModel(MetapopulationNetwork):

    def __init__(self, patches, births, deaths, contacts, infects, progresses, recovers, moves, deaths_disease, p_infectious):

        compartments = [SUSCEPTIBLE, LATENT, INFECTIOUS]

        nodes = []
        edges = []

        for n in range(patches):
            node = EgPatch(n, compartments, birth=births[n], death=deaths[n], contact=contacts[n], infect=infects[n],
                           progress=progresses[n], recover=recovers[n], move=moves[n], death_disease=deaths_disease[n],
                           p_infectious=p_infectious[n])
            for a in nodes:
                edges.append((node, a, {EDGE_TYPE: STANDARD_EDGE}))
            nodes.append(node)

        events = []
        events.append(EgBirth())
        for c in compartments:
            events.append(EgDeath(c))
            events.append(EgMigrate(c))
        events.append(EgInfectLatent())
        events.append(EgInfectInfectious())
        events.append(EgRecover())
        events.append(EgProgress())
        events.append(EgDeathDisease())

        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)
