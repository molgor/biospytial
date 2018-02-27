#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Sampling
======
This module implements different sampling methods for nodes in the knowledge graph.

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2018, JEM"
__license__ = "GPL"
__version__ = "0.0.8"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"


import numpy as np
import pandas as pd
import geopandas as gpd
from drivers.graph_models import countObjectsOf
from drivers.graph_models import logger, graph



def UniformRandomCellSample(list_of_cell_ids,CellNodeClass,sample_size=100,with_replacement=False,random_seed=''):
    """
    Returns a random list of cells of the given grid defined by the *CellNodeClass* parameter (definition of a Mesh).
    
    Parameters : 
        list_of_cell_ids : (List of Integers) the ids of the cells to sample from.
        CellNodeClass : A Cell (GraphObject) see: 'graph_models' 
        sample_size : (Integer) the size of the sample.
        with_replacement (Boolean) : the sample will be with or without replacement. 
        random_seed  (integer) : if empty it will not use any seed. 
    """  
    if random_seed:
        logger.info("Using custom random seed of: %s"%random_seed)
        np.random.seed(random_seed)
    
    n = len(list_of_cell_ids)
    idxchoices = np.random.choice(range(1,n),sample_size,replace=with_replacement)
    cells = pd.DataFrame(list_of_cell_ids,columns=['pk'])
    choices = list(cells.loc[idxchoices].pk)
    ## This will stringify the id list to get the selected cells.
    logger.info("Compiling Query and asking the Graph Database")
    look4 = str(list(choices))
    selection_of_cells = CellNodeClass.select(graph).where("_.id IN  %s "%look4)
    
    return selection_of_cells



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


