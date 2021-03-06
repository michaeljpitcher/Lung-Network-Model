#!/usr/bin/env python

"""Short docstring

Long Docstring

"""

__author__ = "Michael Pitcher"
__copyright__ = "Copyright 2017"
__credits__ = ["Michael Pitcher"]
__license__ = ""
__version__ = "1.0.8"
__email__ = "mjp22@st-andrews.ac.uk"
__status__ = "Development"

BRONCHIAL_TREE_NODE_IDS = range(0, 18)

BRONCHIAL_TREE_NODE_POSITIONS = dict()
BRONCHIAL_TREE_NODE_POSITIONS[0] = (5, 10)
BRONCHIAL_TREE_NODE_POSITIONS[1] = (5, 8)
BRONCHIAL_TREE_NODE_POSITIONS[2] = (4, 7)
BRONCHIAL_TREE_NODE_POSITIONS[3] = (3.5, 5)
BRONCHIAL_TREE_NODE_POSITIONS[4] = (6, 6)
BRONCHIAL_TREE_NODE_POSITIONS[5] = (3, 8)
BRONCHIAL_TREE_NODE_POSITIONS[6] = (2.75, 8.5)
BRONCHIAL_TREE_NODE_POSITIONS[7] = (2.5, 5)
BRONCHIAL_TREE_NODE_POSITIONS[8] = (4, 4)
BRONCHIAL_TREE_NODE_POSITIONS[9] = (3.5, 3)
BRONCHIAL_TREE_NODE_POSITIONS[10] = (3, 2.5)
BRONCHIAL_TREE_NODE_POSITIONS[11] = (2.5, 2)
BRONCHIAL_TREE_NODE_POSITIONS[12] = (7, 7)
BRONCHIAL_TREE_NODE_POSITIONS[13] = (7.5, 8)
BRONCHIAL_TREE_NODE_POSITIONS[14] = (8, 7)
BRONCHIAL_TREE_NODE_POSITIONS[15] = (6.5, 5)
BRONCHIAL_TREE_NODE_POSITIONS[16] = (7.5, 4)
BRONCHIAL_TREE_NODE_POSITIONS[17] = (8, 3.5)

BRONCHOPULMONARY_SEGMENT_IDS = range(18, 36)

BRONCHOPULMONARY_SEGMENT_POSITIONS = dict()
BRONCHOPULMONARY_SEGMENT_POSITIONS[18] = (2.5, 7.5)
BRONCHOPULMONARY_SEGMENT_POSITIONS[19] = (2.5, 9)
BRONCHOPULMONARY_SEGMENT_POSITIONS[20] = (3, 9)
BRONCHOPULMONARY_SEGMENT_POSITIONS[21] = (2, 5.5)
BRONCHOPULMONARY_SEGMENT_POSITIONS[22] = (2, 4)
BRONCHOPULMONARY_SEGMENT_POSITIONS[23] = (3.5, 4.25)
BRONCHOPULMONARY_SEGMENT_POSITIONS[24] = (4, 2)
BRONCHOPULMONARY_SEGMENT_POSITIONS[25] = (2.5, 3.25)
BRONCHOPULMONARY_SEGMENT_POSITIONS[26] = (1.5, 1)
BRONCHOPULMONARY_SEGMENT_POSITIONS[27] = (2.75, 1)
BRONCHOPULMONARY_SEGMENT_POSITIONS[28] = (7.25, 8.5)
BRONCHOPULMONARY_SEGMENT_POSITIONS[29] = (8, 8.5)
BRONCHOPULMONARY_SEGMENT_POSITIONS[30] = (8.5, 7.5)
BRONCHOPULMONARY_SEGMENT_POSITIONS[31] = (8.5, 6.5)
BRONCHOPULMONARY_SEGMENT_POSITIONS[32] = (7, 5.5)
BRONCHOPULMONARY_SEGMENT_POSITIONS[33] = (7.5, 3)
BRONCHOPULMONARY_SEGMENT_POSITIONS[34] = (8.5, 4.25)
BRONCHOPULMONARY_SEGMENT_POSITIONS[35] = (8.5, 3)

BRONCHIAL_TREE_EDGES = [(0, 1), (1, 2), (2, 3), (1, 4)]
BRONCHIAL_TREE_EDGES += [(2, 5), (5, 6), (3, 7), (3, 8), (8, 9), (9, 10), (10, 11), (4, 12), (12, 13), (12, 14), (4, 15)
                         , (15, 16), (16, 17)]
BRONCHIAL_TREE_EDGES += [(5, 18), (6, 19), (6, 20), (7, 21), (7, 22), (8, 23), (9, 24), (10, 25), (11, 26), (11, 27),
                         (13, 28), (13, 29), (14, 30), (14, 31), (15, 32), (16, 33), (17, 34), (17, 35)]


def ventilation_from_position(position):
    return ((10 - position[1]) * 0.05) + 0.2


def perfusion_from_position(position):
    return ((10 - position[1]) * 0.09) + 0.1

