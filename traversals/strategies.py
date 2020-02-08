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
import geopandas as gpd
from shapely.geometry import Point
from drivers.graph_models import Cell,Mex4km,graph
import logging
import numpy as np
from itertools import imap, chain
import networkx as nx
from utilities import data_extraction as de
from pandas.api.types import CategoricalDtype
import copy 

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2017, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



logger = logging.getLogger('biospytial.traversals')


####
## Multifunc
## These are function for handling dataframes and creating subsets.
#def toGeoDataFrame(pandas_dataframe,xcoord_name='Longitude',ycoord_name='Latitude',srs = 'epsg:4326'):
#    """
#    Convert Pandas objcet to GeoDataFrame
#    Inputs:
#        pandas_dataframe : the pandas object to spatialise
#        xcoord_name : (String) the column name of the x coordinate.
#        ycoord_name : (String) the column name of the y coordinate. 
#        srs : (String) the source referencing system in EPSG code.
#                e.g. epsg:4326 .
#    """
#    data = pandas_dataframe
#    #import ipdb; ipdb.set_trace()
#    data[xcoord_name] = pd.to_numeric(data[xcoord_name])
#    data[ycoord_name] = pd.to_numeric(data[ycoord_name])
#    data['geometry'] = data.apply(lambda z : Point(z[xcoord_name], z[ycoord_name]), axis=1)
#    #data['geometry'] = data.apply(lambda z : Point(z.LON, z.LAT), axis=1)
#
#    new_data = gpd.GeoDataFrame(data)
#    new_data.crs = {'init':'epsg:4326'}
#    return new_data
#
#
# to allow retrocompatibility
toGeoDataFrame = de.toGeoDataFrame
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
    data = de.toGeoDataFrame(data, 'Longitude', 'Latitude')
    return data

def getEnvironmentalCovariatesFromListOfCells(list_of_cells,vars=['Elevation','MaxTemperature',
'MeanTemperature','MinTemperature','Precipitation','Vapor','SolarRadiation','WindSpeed'],with_coordinates=True):
    """
    Parameters :
        vars (list) name of the environmental layers. By default select all layers.
    
    Returns:
         a Dataframe of the summary statistics of the raster covariates defined in the cell's border (polygon).
    """ 
    
    getdata = lambda cell : cell.getEnvironmentalData(vars)
    rdata = map(getdata,list_of_cells)
    if not with_coordinates:
        return pd.DataFrame(rdata)
    else:
        coords = getCentroidsFromListofCells(list_of_cells)
        data = pd.DataFrame(rdata)
        return pd.concat([data,coords],axis=1)

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

def CoordinatesDataFrameToPointsGeometry(coordinate_df,srid=4326):
    """
    Returns the geometric interpretation (GEOS) of the points in coordinate_df 
    """
    toPoint = lambda array :'POINT(%s %s)'%(array[0],array[1])
    points = map(lambda p :GEOSGeometry(p,srid=srid), map(toPoint,coordinate_df.values))
    return points



def idsToCells(list_of_ids,cell_type=Mex4km):
    """
    Given a list of indices (primary values), returns the corresponding object (OGM).
    Parameters :
        list_of_is : (List) a list with integers defining the pk values of the objects to obtain.
        cell_type : The class name or object to query from (default Mex4km) 
    """
    logger.info("Compiling Query and asking the Graph Database")
    look4 = str(list_of_ids)
    selection_of_cells = cell_type.select(graph).where("_.id IN  %s "%look4)
    return selection_of_cells


def LatticeToNetworkx(list_of_cells,intrinsic_graph=True,use_only_ids=True):
    """
    Returns a Networkx Graph Object given by the cells and it's neighbours
    Parameters : 
        list_of_cells (list) : List of Cell objects 
        intrinsic_graph (Boolean) : If true returns a graph with exactly the nodes
        given in the list of cells (i.e. excluding neighbouring nodes that are not in the
        list_of_cells)
        use_only_ids (Boolean) : If true each node will be an integer (corresponding
        id) otherwise each node is a Cell object.
        it is usefull if the graph is going to be pickled.
    """
    def insert_nodes((center,neighbours)):
        # if the neighbour is empty insert the node
        if neighbours:
            map(lambda n : G.add_edge(center,n),neighbours)
        else:
            G.add_node(center)

    neighbours = map(lambda cell : cell.getNeighbours(),list_of_cells)

    G = nx.Graph()
    if use_only_ids:
        list_of_cells = map(lambda c : c.id, list_of_cells)
        neighbours = map(lambda nl : map(lambda n : n.id,nl),neighbours)
    
    node_edges = zip(list_of_cells,neighbours)
    map(insert_nodes,node_edges)
    # Excluding neighbouring nodes
    if intrinsic_graph:
        cells_s = set(list_of_cells)
        nodes_s = set(G.nodes())
        extra = filter(lambda n : n not in cells_s,nodes_s)
        map(lambda x : G.remove_node(x),extra)
    return G



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


def getPresencesFromAncestralChainofNode(node,list_of_trees,as_dataframe=True,with_centroids=False,merge_with_this_environmental_data=[]):
    """
    Returns a dataframe with the presences of all the nodes 
    contained in the ancestral chain of a given node.
    The columns corresponds to each node in the linage order by the taxonomic level 
    
    Parameters: 
        node : (TreeNode) the node to to whom the presences of ancestors should be obtained.
        list_of_trees : list of TreeNeo objects
        merge_with_this_environmental_data: If this is a pandas dataframe, concatenate with each presence.
        as_dataframe: (Boolean) if true returns a dataframe, else returns a list. 
        with_centroids: (Boolean) if true returns the centroids of each areal unit. 
    """
    
    ng = node.getAncestors()
    
    ancestors = list(ng.nodes)
    # sort ancestors by taxonomic level
    ancestors.sort(key=lambda l : l.level)
    names_anc = map(lambda l : l.name, ancestors)
    anc_levels = map(lambda l : l.level, ancestors)
    keys = dict(zip(names_anc,anc_levels))
    presences = getPresencesForListOfNodes(ancestors,list_of_trees,with_centroids=with_centroids)
    things = []
    for name,presence in presences.iteritems():
        d = pd.DataFrame(presence).stack().reset_index()
        d.drop('level_0', axis=1, inplace=True)
        d.columns = ['level','Y']
        d['Y'] = d['Y'].astype('int')
        ## with environmental data
        if isinstance(merge_with_this_environmental_data,pd.DataFrame):
            env_data = merge_with_this_environmental_data
            tt = pd.concat([d,env_data],axis=1)
            things.append(tt)
        else:
            things.append(d)
    
    if as_dataframe:
            all_data = reduce(lambda l1,l2 : pd.concat([l1,l2],axis=0),things)
            cat_type = CategoricalDtype(categories=names_anc,ordered=True)            
            all_data['level'] = all_data['level'].astype(cat_type)
            all_data['code']=all_data.level.cat.codes
            return(all_data)
    else:
        return(things)


def calculateComplementaryTrees(list_of_trees,occurrences_of_interest,large_size_of_trees=False):
    """
    Returns a list composed of complementary trees given a list of occurrences of
    interest.

    Parameters: 
        list_of_trees : A list of TreeNeo objects
        occurrences_of_interest : a list of occurrences extracted from taxa of
        interest given a certain context.
        large_size_of_trees : Boolean, if True it will cast the occurrences of each
        tree to a Set, this will increase the lookup on large colelction of
        occurrences. However, casting to set will cause a delay and is only
        recommended if its taking longer than expected.
        

    Note >
    If the size of the occurrences in trees is large
    """
    trees = list_of_trees
    occurrences_of_interest = set(occurrences_of_interest)
    complementary_trees = []
    n = len(trees)
    for i,tree in enumerate(trees):
        x = (float(i) / n )* 100
        #logger.info("Calculating complementary tree. Done %s perc."%x)
        s = "Calculating complementary tree. Done %s perc."%x
        print '{0}\r'.format(s),
        if large_size_of_trees :
            ocs_in_tree = set(tree.occurrences)
        else:
            ocs_in_tree = tree.occurrences
        compl_ocs = filter(lambda occurrence: occurrence not in occurrences_of_interest , ocs_in_tree)
        complementary_trees.append(TreeNeo(compl_ocs,cell_objects=tree.getExactCells()))
    print('\n')
    return(complementary_trees)


def buildDesignMatrixForMultispeciesModel(list_of_presences_dfs,complementary_presence_df,covariates_dataframe):
    """
    Returns a stacked GeoDataFrame of all the taxa of interest (defined in the
    list_of_presences_dfs) and the complementary sample (derived from the function:
    calculateComplementaryTrees and the projected to some vector, typically binary).

    The resulting table is composed of stacked design matrices for each each taxon of
    interest and the covariates matrix, including geometry.
    Parameters: 
        list_of_presences_dfs : (List of dataframes). Usually derived from the
        function: getPresencesForNode(TreeNode,list_of_trees). 
        
        complementary_presence_df (pandas Series) : a vector (usually binary) that maps each
        complementary tree to a number. 
        
        covariates_dataframe : (Pandas Geodataframe) a dataframe corresponding to the
        covariates, including the geometry. This will be stacked for each taxon. i.e.
        they are repeated. 

    Example:

        complementary_trees = st.calculateComplementaryTrees(list_of_trees=trees[0],occurrences_of_interest=occurrences_of_interest,large_size_of_trees=True)

        taxa_of_interest_nodes = map(lambda taxon : taxon.node,taxa_of_interest)

        list_of_presences_dfs = map(lambda taxon : st.getPresencesForNode(TreeNode=taxon,list_of_trees=trees[0]),taxa_of_interest_nodes)

        complementary_presences_list = [1.0 if tree.richness > 0 else 0.0 for tree in complementary_trees]
        
        complementary_presence_df = pd.DataFrame(complementary_presences_list,columns=['Complement'])

        from raster_api.models import raster_models_dic

        rstmods = raster_models_dic.keys()

        data = map(lambda cell : st.getEnvironmentalCovariatesFromListOfCells(cell,vars=rstmods),cells)
        ids = pd.DataFrame(map(lambda cell : (cell.id,cell.polygon_shapely),cells[0]),columns=['cell_ids','geometry'])
        newdata = pd.concat([ids,data[0]],axis=1)
        data_level = gpd.GeoDataFrame(newdata,geometry='geometry')

    Note: 
        This is a beta version, it has not been tested throughly.

    """
    llp = copy.copy(list_of_presences_dfs)
    llp.append(complementary_presence_df)
    n_levels = len(llp)
    n_areas = len(llp[0])
    plist= []
    for l in range(n_levels):
        level = pd.DataFrame( (l + 1) * np.ones(n_areas).astype('int'),columns=['level'])
        p_df = llp[l]
        name = p_df.columns[0]
        names = pd.Series([name for i in range(n_areas)],name='taxon') 
        p = pd.concat([p_df,level,names],axis=1)
        p.columns=['Y','level','taxon']
        pn = pd.concat([p,covariates_dataframe],axis = 1)
        plist.append(pn)
    
    data = pd.concat(plist,axis=0)
    data = data.set_index(['cell_ids','level'])
    data = gpd.GeoDataFrame(data,geometry='geometry')
    return(data)
