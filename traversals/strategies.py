#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Strategies
==========
..
This modile implments different strategies for retrieving information in the shape of Graphs.

Based on the :ref:`drivers.graph_builder` and spatial operations.
"""
from drivers.tree_builder import TreeNeo

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2017, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"


import logging

logger = logging.getLogger('biospytial.traversals')

import numpy as np
from itertools import imap

def UniformRandomSampleForest(cell_list,size=100):
    """
    Obtains a random sample of size 'size; of  Trees corresponding to a uniform random subsets of cells given a list of cells 
    Returns an iterator. Cast a list to obtain the result
    """
    n = len(cell_list)
    
    sampleids = lambda size : np.random.randint(0,n,size)
    logger.debug("Random list creates")
    # get cells
    #givecell = lambda i : cell_list[i]
    givecells = lambda size : imap(lambda i : cell_list[i] ,sampleids(size))
    logger.debug("Random cells selected")
    #cells = [ cell_list[i] for i in sampleids(n)]
    getTrees = lambda size : imap(lambda cell : TreeNeo(cell.occurrencesHere()),givecells(size))

    trees = getTrees(size)
    return trees


sumTrees = lambda tree_list : reduce(lambda a,b : a + b , tree_list)


