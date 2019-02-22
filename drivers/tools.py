# Some tools for handling the TreeNeo's

# Author: Juan Escamilla 
# Date: 7/4/2017
 
#!/usr/bin/env python
#-*- coding: utf-8 -*-

# visualizing and analysing
from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nt
import numpy as np

def RankTaxonomicLevel(tree,list_trees,level):
    """
    Returns a list of ranks from top to bottom of the most frequent taxa using the attribute n_presence
    """
    #tree.countNodesFrequenciesOnList(list_of_trees)
    taxa = tree.levels[level]
    n = len(list_trees)
    taxa.sort(key=lambda t : t.n_presences_in_list,reverse=True)
    taxas = map(lambda node : (node,float(node.n_presences_in_list)/n),taxa)
    return taxas


def TreeToTable(tree,level):
    """
    Uses the rank list to return a pandas datatable with frequencies.
    """
    taxa = RankTaxonomicLevel(tree, level)
    pass



def plotTree(treeneo, depth=6,label_depth=5):
    """
    Plot the graph using a circo layout
    """
    ## Some functions for visualising
    extractNames = lambda graph : {k:v for (k,v) in map(lambda n : (n,n.name),graph.nodes())}
    extractColors = lambda graph :  map(lambda n : n.level,graph.nodes())
    #extractfreqs = lambda graph :  np.array(map(lambda n : n.n_presences_in_list,graph.nodes()))
    gt = treeneo.toNetworkx(depth_level=depth)
    root = treeneo.node
    pos = graphviz_layout(gt,prog='circo',root=root.node.name)
    g_labels = treeneo.toNetworkx(depth_level=4)
    #x = nt.draw(gt,pos,labels=extractNames(g_labels),node_color=extractColors(gt),node_size=extractfreqs(gt)*500)
    x = nt.draw(gt,pos,labels=extractNames(g_labels),node_color=extractColors(gt))

    return x


def redisConnection(host='redis'):
    """
    A Redis connection for Biospytial
    """
    import redis
    rc = redis.StrictRedis(host=host)
    return rc