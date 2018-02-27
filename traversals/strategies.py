#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Strategies
======
..
This module implements different strategies for retrieving information in the shape of Graphs.

Based on the :ref:`drivers.graph_builder` and spatial operations.
"""
from drivers.tree_builder import TreeNeo,buildTreeNeo
from django.contrib.gis.geos import GEOSGeometry
from mesh.models import initMesh
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

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
from itertools import imap, chain

####
## Multifunc
## These are function for handling dataframes and creating subsets.
def toGeoDataFrame(pandas_dataframe,xcoord_name,ycoord_name,srs = 'epsg:4326'):
    """
    Convert Pandas objcet to GeoDataFrame
    Inputs:
        pandas_dataframe : the pandas object to spatialise
        xcoord_name : (String) the column name of the x coordinate.
        ycoord_name : (String) the column name of the y coordinate. 
        srs : (String) the source referencing system in EPSG code.
                e.g. epsg:4326 .
    """
    data = pandas_dataframe
    data['geometry'] = data.apply(lambda z : Point(z[xcoord_name], z[ycoord_name]), axis=1)
    #data['geometry'] = data.apply(lambda z : Point(z.LON, z.LAT), axis=1)

    new_data = gpd.GeoDataFrame(data)
    new_data.crs = {'init':'epsg:4326'}
    return new_data




###############
## Cell-wise: strategies 
###############

def getEnvironmentAndRichnessFromListOfCells(list_of_cells,taxonomic_level_name,vars=['Elevation','MaxTemperature', 'MeanTemperature','MinTemperature','Precipitation','Vapor','SolarRadiation','WindSpeed']):
    """
    A wrapper function that returns Richness, environmental covariates and centroids.
    For a tailored version of this use the individual functions and concatenate dataframes.
    
    Parameters : 
            vars : (list) name of the environmental layers. By default select all layers.
            taxonomic_level_name : (String) the name of the taxonomic level to which take the richness from.

    Returns : A spatial dataframe (geopandas) 
    
    """
    env = getEnvironmentalCovariatesFromListOfCells(list_of_cells, vars)
    rich = getRichnessPerListOfCells(list_of_cells, taxonomic_level_name)
    data = pd.concat([rich,env],axis =1)
    data = toGeoDataFrame(data, 'Longitude', 'Latitude')
    return data

def getEnvironmentalCovariatesFromListOfCells(list_of_cells,vars=['Elevation','MaxTemperature', 'MeanTemperature','MinTemperature','Precipitation','Vapor','SolarRadiation','WindSpeed']):
    """
    Parameters :
        vars (list) name of the environmental layers. By default select all layers.
    
    Returns:
         a Dataframe of the summary statistics of the raster covariates defined in the cell's border (polygon).
    """ 
    
    getdata = lambda cell : cell.getEnvironmentalData(vars)
    rdata = map(getdata,list_of_cells)
    return pd.DataFrame(rdata)

def getRichnessPerListOfCells(list_of_cells,taxonomic_level_name,with_centroids=True):
    """
    Given a list of cells it returns the respective richness in the shape of pandas object.
    
    Parameters:
        list_of_cells : (List or iterator) the cells to take the richness from.
        taxonomic_level_name : (String) the name of the taxonomic level to which take the richness from.
        with_centroid :  (Bool) if True returns the centroids of each corresponding cell
    Returns:
        richness : DataFrame 
    
    """    
    rs = map(lambda cell : cell.getRichnessOf(taxonomic_level_name),list_of_cells)
    richness = pd.DataFrame({'n_'+taxonomic_level_name : rs })
    if with_centroids:
        coords = getCentroidsFromListofCells(list_of_cells, asDataFrame=True)
        return pd.concat([richness,coords],axis=1)
    else:
        return richness
    
def getCentroidsFromListofCells(list_of_cells,asDataFrame=True):
    """
    Returns list of centroids in numpy array format.
    Params : asDataFrame : (Bool) Returns a DataFrame otherwise returns an iterator. True by default. 
    """
    
    itercentroid = imap(lambda cell : cell.centroid,list_of_cells)    
    if asDataFrame:
        centroids = chain(itercentroid)
        coords = map(lambda p : (p.x,p.y) , centroids)
        points = pd.DataFrame(coords,columns=["Longitude","Latitude"])
        return points
    else:
        return itercentroid


###############
## Treewise Strategies
###############




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
    logger.info("Getting information. Developer! You can make this faster if you use Batchmode for py2neo.")
    cellnode = map(lambda c : c.toCellNode().first(),cells)
    logger.info("Retrieving the Tree Structures. \n Get a coffee this will take time.")
    trees = map(lambda cell : buildTreeNeo(cell),cellnode)

    return trees
 
 



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


    
    