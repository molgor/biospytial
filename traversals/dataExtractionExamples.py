#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
# This code is for extracting Data Stored in The Graph Database.


#@Author: Juan Escamilla 
#@Date: 9/08/2017

"""
from django.contrib.gis.geos import GEOSGeometry 
import pandas as pd                                                       

## Here I'm testing how to extract data in the Diggle's format, 2017 letter to Pete, Luigi and Me.

from drivers.graph_models import TreeNode, Order, Family, graph, pickNode
from traversals.strategies import sumTrees, UniformRandomSampleForest,PolygonToTrees
from mesh.models import initMesh
from traversals.strategies import getEnvironmentalCovariatesFromListOfTrees,getPresencesForListOfNodes,getCentroidsFromListofTrees

def main():
    ## Small area.
    polystr = 'POLYGON((-92.24837214921502948 16.53658521768252854,-92.11186028915844304 16.52849027585105901,-92.10623093410457329 16.37327180168962926,-92.25118682674197146 16.37462206197250225,-92.24837214921502948 16.53658521768252854))'
    ## Bigger Area
    #polystr = 'POLYGON((-92.54989447928841173 16.93450143453089396,-91.70267654367958698 16.9021871200489322,-91.68015912346406537 16.28717344210308937,-92.56396786692310741 16.31959139053146757,-92.54989447928841173 16.93450143453089396))'
    trees = PolygonToTrees(polystr)
    big_t = reduce(lambda a,b : a+b, trees)
    polygon = GEOSGeometry(polystr)
    mesh = initMesh(11) 
    # Get cells.
    
    
    # Extract Environmental Covariates
    ## Abiotic components.
    rd = getEnvironmentalCovariatesFromListOfTrees(trees)
    
    ## Select a branch for the big tree
    falcons = big_t.to_Animalia.to_Chordata.to_Aves.to_Falconiformes
    s = getPresencesForListOfNodes(falcons,trees)

    all_data = pd.concat([rd,s],axis=1)
    data = {"BTREE" : big_t, "LTrees":trees, "Table":all_data}
    return data

if __name__ == "__main__":
    main()
