#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

# imports

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

LYMPH_NODE_IDS = range(36, 45)

LYMPH_NODE_POSITIONS = dict()
LYMPH_NODE_POSITIONS[36] = (6, 4.6)
LYMPH_NODE_POSITIONS[37] = (4.5, 5.1)
LYMPH_NODE_POSITIONS[38] = (5, 5.9)
LYMPH_NODE_POSITIONS[39] = (4.25, 6.1)
LYMPH_NODE_POSITIONS[40] = (4.5, 7.6)
LYMPH_NODE_POSITIONS[41] = (4.21, 9.75)
LYMPH_NODE_POSITIONS[42] = (5.9, 7.05)
LYMPH_NODE_POSITIONS[43] = (5.8, 8.2)
LYMPH_NODE_POSITIONS[44] = (6.0, 9.8)

LYMPH_EDGES = [(36, 38), (37, 38), (38, 40), (39, 40), (40, 41), (42, 43), (43, 44)]

for drainage_id in range(32, 36):
    LYMPH_EDGES.append((drainage_id, 36))

for drainage_id in range(28, 32):
    LYMPH_EDGES.append((drainage_id, 42))
for drainage_id in range(23, 28):
    LYMPH_EDGES.append((drainage_id, 37))
for drainage_id in range(18, 23):
    LYMPH_EDGES.append((drainage_id, 39))


def calculate_lymph_flow_rates(terminal_node_positions):
    flow_rates = dict()

    for (a,b) in LYMPH_EDGES:
        if not a in terminal_node_positions and not b in terminal_node_positions:
            flow_rates[(a,b)] = 1.0
        elif a in terminal_node_positions:
            flow_rates[(a, b)] = (10.0 - terminal_node_positions[a][1]) / 10.0
        else:
            flow_rates[(a, b)] = (10.0 - terminal_node_positions[b][1]) / 10.0

    return flow_rates