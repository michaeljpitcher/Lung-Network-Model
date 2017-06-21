#!/usr/bin/env python

"""Short docstring

[1] J. Arino, J. R. Davis, D. Hartley, R. Jordan, J. M. Miller, and P. Van Den Driessche, "A multi-species epidemic 
model with spatial dynamics," Math. Med. Biol., vol. 22, pp. 129-142, 2005.

"""

from ..BaseEpidemic.Model.MultiPatchFullConnectedEpidemicModel import *
from ..EpidemiologyClasses import *
from ArinoInfect import *
from ...Base.Events.Creation import *
from ...Base.Events.Change import *
from ...Base.Events.Destruction import *
from ...Base.Events.Translocate import *

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

class ArinoPatch(Patch):
    def __init__(self, node_id, compartments, beta):
        self.beta = beta
        Patch.__init__(self, node_id, compartments)


class ArinoOneSpeciesModel(MetapopulationNetwork):
    """
    Assumes:
    same birth/death rate at all patches
    same infection rate at all patches
    same migration rate between patches
    """


    def __init__(self, number_of_patches, d, betas, m, epsilon, gamma):

        compartments = [SUSCEPTIBLE, EXPOSED, INFECTIOUS, RECOVERED]

        events = []

        # Birth
        events.append(CreateByOtherCompartments([Patch], d, SUSCEPTIBLE, compartments))

        # Infect
        events.append(ArinoInfect([Patch], SUSCEPTIBLE, EXPOSED, [INFECTIOUS]))

        # Migration
        for comp in compartments:
            events.append(Translocate([Patch], m, comp, STANDARD_EDGE, probability_increases_with_edges=True))

        # Progression
        events.append(Change([Patch], epsilon, EXPOSED, INFECTIOUS))

        # Recover
        events.append(Change([Patch], gamma, INFECTIOUS, RECOVERED))

        # Death
        for comp in compartments:
            events.append(Destroy([Patch], d, comp))

        nodes = []
        for n in range(number_of_patches):
            nodes.append(ArinoPatch(n, compartments, betas[n]))
        edges = []
        for n in range(number_of_patches - 1):
            for k in range(n + 1, number_of_patches):
                edges.append((nodes[n], nodes[k], {EDGE_TYPE: STANDARD_EDGE}))

        MetapopulationNetwork.__init__(self, compartments, nodes, edges, events)
