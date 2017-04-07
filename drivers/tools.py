# Some tools for handling the TreeNeo's

# Author: Juan Escamilla 
# Date: 7/4/2017
 
#!/usr/bin/env python
#-*- coding: utf-8 -*-

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