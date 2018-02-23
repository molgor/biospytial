#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Strategies
==========
..
This module implements different strategies for retrieving information in the shape of Graphs.

Based on the :ref:`drivers.graph_builder` and spatial operations.
"""
from drivers.tree_builder import TreeNeo,buildTreeNeo
from django.contrib.gis.geos import GEOSGeometry
from mesh.models import initMesh
import pandas as pd
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


def PolygonToTrees(polygon_wkt,mesh_level=11):
    """
    Receives a polygon str in wkt, get the cells and extracts the trees in that Cell.
    Will work on the cell layer that has a direct link Occurrence - IS_IN - Cell
    
    note: It uses the spatial querying from the Geoprocessing Unit (RDMS) module.
    """
    polygon = GEOSGeometry(polygon_wkt)
    mesh = initMesh(mesh_level)
    cells = list(mesh.objects.filter(cell__intersects=polygon))
    logger.info("Getting information. DEveloper! You can make this faster if you use Batchmode for py2neo.")
    cellnode = map(lambda c : c.toCellNode().first(),cells)
    logger.info("Retrieving the Tree Structures. \n Get a coffee this will take time.")
    trees = map(lambda cell : buildTreeNeo(cell),cellnode)

    return trees
 
 

def getEnvironmentalCovariatesFromListOfCells(list_of_cells,vars=['Elevation','MaxTemperature', 'MeanTemperature','MinTemperature','Precipitation','Vapor','SolarRadiation','WindSpeed']):
    """
    Returns a Dataframe of the summary statistics of the raster covariates defined in the cell's border (polygon).
    """ 
    
    getdata = lambda cell : cell.getEnvironmentalData(vars)
    rdata = map(getdata,list_of_cells)
    return pd.DataFrame(rdata)

def getAllRichnessOf(list_of_cells,taxonomic_level_name):
    """
    Given a list of cells it returns the respective richness in the shape of pandas object.
    Returns:
        richness : DataFrame 
    
    """    
    rs = map(lambda cell : cell.getRichnessOf(taxonomic_level_name))
    richness = pd.DataFrame({'n.'+taxonomic_level_name : rs })
    return richness
    

def getEnvironmentalCovariatesFromListOfTrees(list_of_trees):
    """
    Returns a Dataframe of the summary statistics of the raster covariates defined in the cell's border (polygon).
    """ 
    
    getdata = lambda tree : tree.associatedData.getEnvironmentalVariablesCells()
    
    rdata = map(getdata,list_of_trees)
    return pd.DataFrame(rdata)
    
def getPresencesForNode(TreeNode,list_of_trees, option='presences'):
    """
    Given a list of trees and a Tree Node the function returns a binary list if the node was found on that Tree.
    Returns:
        list of presence absences
    
    notes:
        For the future, implement with count data (Poisson)
    """    
    signal = map(lambda tree : float(tree.hasNode(TreeNode)),list_of_trees)
    y = {TreeNode.name : signal}
    return pd.DataFrame(y)
    
def getPresencesForListOfNodes(list_of_tree_nodes,list_of_trees,with_centroids=True):
    """
    Given a list of trees and a list of TreeNodes this function returns a binary table if the node was found on each of the trees.
    Similar to getSignalForNode but multivalued.
    """    
    signals = map(lambda tree_node :  getPresencesForNode(tree_node, list_of_trees),list_of_tree_nodes)
    if with_centroids:
        centroids = getCentroidsFromListofTrees(list_of_trees)
        p = pd.concat(signals,axis=1)
        
        return pd.concat([p,centroids],axis=1)
    else:
        return pd.concat(signals,axis=1)
    
    
def getCentroidsFromListofTrees(list_of_trees):
    """
    Returns list of centroids in numpy array format.
    """    
    npoints = map(lambda c : np.array(c.getExactCells()[0].centroid),list_of_trees)
    points = pd.DataFrame(npoints,columns=["Longitude","Latitude"])
    
    return points
    
    