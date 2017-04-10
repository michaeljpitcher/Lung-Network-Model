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

STRAHLER = 'strahler'
HORSFIELD = 'horsfield'

def tree_weight_calculations(origin, edges, weight_type):
    """ Calculate edge weights for a tree
    
    Given a set of nodes, an origin and a weighting method, calculates the appropriate weights based on the method. 
    Methods are:
        STRAHLER: terminal edges are given weight 1. Parent edges have weight +1 of max of child edge weights
        HORSFIELD: terminal edges are given weight 1. Parent edges have weight +1 of max of child edge weights if all
                   edges have same weight, else max of child edge weights 
    
    :param origin: 
    :param edges: 
    :param weight_type: 
    :return: 
    """
    weights = dict()

    # Work out neighbours
    neighbours = dict()
    for (u, v) in edges:
        if u in neighbours:
            neighbours[u].append(v)
        else:
            neighbours[u] = [v]
        if v in neighbours:
            neighbours[v].append(u)
        else:
            neighbours[v] = [u]

    queued_nodes = [origin]

    # Order nodes so a node isn't processed before its child nodes are
    ordered_nodes = []

    while queued_nodes:
        # Remove the first node of the queued list
        node = queued_nodes.pop()
        # Insert the new node at the start of ordered list
        ordered_nodes.insert(0, node)
        # Queue up the neighbours (that aren't already ordered) of this node
        queued_nodes += [neighbour for neighbour in neighbours[node] if neighbour not in ordered_nodes]

    processed_nodes = []

    for node in ordered_nodes:
        # Don't process origin (has no parent)
        if node == origin:
            continue
        # Get parent to node
        parent = [n for n in neighbours[node] if n not in processed_nodes]
        assert len(parent) == 1
        parent = parent[0]

        # get the child weights
        child_weights = [weights[(u,v)] for (u,v) in weights if v == node]
        # No child weights -> terminal edges, so weight 1
        if not child_weights:
            new_weight = 1
        # Strahler ordering - max of child weights + 1
        elif weight_type == STRAHLER:
            new_weight = max(child_weights) + 1
        # Horsfield ordering - if all even, max of child weights +1, else max of child weights
        elif weight_type == HORSFIELD:
            if len(set(child_weights)) <= 1:
                new_weight = max(child_weights) + 1.0
            else:
                new_weight = max(child_weights)
        else:
            raise Exception, "Invalid weight type"
        # Set the new weight
        weights[(node,parent)] = new_weight
        # Add to processed nodes
        processed_nodes.append(node)

    return weights
