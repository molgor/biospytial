# tree_builder.py
# THis module abstracts the general node in the OGM implementation, to the TreeNOde and LocalTree objects of biospytial.
# The OGM makes the mapping to the database and this class instantiates the data given a location in time or space.
# It uses the Occurrence QuerySet from the Django models in gbif.taxonomy. 
#The Module for Object Graph Mapping OGM . 

# Author: Juan Escamilla 
# Date: 26/10/2016
 
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pandas
import copy
from itertools import groupby
from drivers.graph_models import Occurrence as OccurrenceNode
from drivers.graph_models import Cell
from drivers.raster_node_builder import RasterCollection
import numpy as np
import itertools as it

from collections import OrderedDict
from compiler.ast import nodes
import networkx as nx
from py2neo import Graph
from biospytial import settings


neoparams = settings.NEO4J_DATABASES['default']
uri = "http://%(HOST)s:%(PORT)s%(ENDPOINT)s" % neoparams


import logging
logger = logging.getLogger('biospytial.tree_builder')

## Utility functions

def aggregator(list_sp):
    ##Comming from the first collider
    
    list_sp.sort(key=lambda l : l.getParent().id)
    
    #list_nodes.sort(key=lambda node :  node.getParent().id)
    grouper = groupby(list_sp, lambda node : node.getParent())
    output = []
    for node,children in grouper:
        s = LocalTree(node,list(children))
        #s = TreeNeo(node,list(children))
        output.append(s)
    return output
       
def extractOccurrencesFromTaxonomies(list_of_taxonomies):
    """
    Updates the occurrences attribute to fit all the occurrences of the given list of taxonomies
    """
    neoparams = settings.NEO4J_DATABASES['default']
    uri = "http://%(HOST)s:%(PORT)s%(ENDPOINT)s" % neoparams
    g = Graph(uri)
    occurrences =  reduce( lambda one,two : one + two ,[ list(occurrence) for occurrence in [ taxonomy.occurrences for taxonomy in list_of_taxonomies ]])

    occurrences = map(lambda o : o.asOccurrenceOGM(),occurrences)
    
    geometries_ids = map(lambda tax : tax.gid, list_of_taxonomies)
    cells = map(lambda i : Cell.select(g,i).first(),geometries_ids)

    return occurrences, cells
    #self.windUpLevels()   




class LocalTree(object):
    def __init__(self,this_node,children):
        self.node = this_node
        self.children = children
        self.parent = self.node.getParent()
        self.name = self.node.name
        self.id = self.node.id
        self.levelname = self.node.levelname
        self.associatedData = RasterCollection(self)
        self.level = self.node.level
        self.occurrences = []
        self.involvedCells = []
        self.neighbouringtrees = []
        self.n_presences_in_list = 'N.A.'


    
    #self.graph = self.setGraph()
        # Experiment 1
        # this is a very good method for 
        map(lambda l : setattr(self,'to_'+l.name.encode('utf-8').replace(" ","_").replace(",",""),l), children)
        
        #self.setOccurrences()



    def getGraph(self,graph):
        """
        Converts to a Networkx object
        """
        node = self
        for child in self.children:            
            graph.add_edge(node,child,weight=node.richness)
            try:
                graph = child.getGraph(graph)
            except: 
                continue
                #return graph
            #G.add_edge(node, child.node,attr_dict=None)
        return graph

    def toNetworkx(self):
        """
        Converts the Tree to a Graph structure handled by the Networkx library
        """
        import networkx as nt
        g = nt.Graph()
        tree = self.getGraph(g)
        return tree
    
    @property
    def richness(self):
        return len(self.occurrences)
    
    
    def getParent(self):
        return self.parent



    def __repr__(self):
        try:
            cad = "<LocalTree | %s: %s - n.count : %s- | AF: %s >"%(self.levelname,self.name,self.richness,self.n_presences_in_list)
        except:
            cad = "<LocalTree | %s: - n.count : %s- >"%('No record available',self.richness)
        return cad.encode('utf-8')

    def setOccurrences(self):
        """
        Sets the corresponding occurrences for each level.
        It uses recursion and stores the output in each level (occurrences) on it's proper attribute.
        The output of each children is merged (union in sets) together to give the total occurrences of each children of the current node (LocalTree).

        notes :
        
            This method is elegant!
            Took me some time to figure it out. I think I cannot make something more efficient,yet/.
        
        
        """
        logger.debug("Retrieving the subtrees")
        for occurrence in self.children:
            if not isinstance(occurrence, OccurrenceNode):
                #logger.debug("Children are not type occurrence")
                try:
                    occurrences_on_children = occurrence.setOccurrences()
                except:
                    import ipdb; ipdb.set_trace()
                # magic step!
                self.occurrences += occurrences_on_children
            else:
                self.occurrences.append(occurrence)
                
        return self.occurrences





    def __iter__(self):
        return iter(self.children)



    
    def pullbackRasterNodes(self,raster_name):
        """
        Returns the raster node of the selected 'layer' given by raster name
        Current options are:
        
        Parameters:
        
            raster_name $in$ {'Elevation', 'MaxTemperature', 'MeanTemperature',
             'MinTemperature', 'Precipitation', 'Vapor' , 'SolarRadiation' ,
          'WindSpeed'}
        """
        nodes_iters = map(lambda oc : (oc.pullbackRasterNodes(raster_name),oc),self.occurrences)
        #nodes_iters = map(lambda oc : oc.pullbackRasterNodes(raster_name),self.occurrences)
        #nodes = reduce(lambda n1,n2 : list(n1) + list(n2) , nodes_iters)
        
        ## First extract the list, it could be empty and therefore will throw an exception
        nodes = map(lambda node_occ : (list(node_occ[0]),node_occ[1]),nodes_iters) 
        ## Filter the nodes that have a list different from empty
        new_nodes = filter(lambda (list_node, occurrence) : list_node,nodes)
        ## Extract the element
        new_nodes = map(lambda ( list_node,occurrence ) : (list_node.pop(),occurrence), new_nodes)
        return new_nodes
    

    def getPointCoordinates(self):
        """
        Returns a list of coordinates x, y  (long,lat)
        """
        points = map(lambda o : (o.longitude,o.latitude),self.occurrences)
        return points

    def getExactCells(self):
        """
        Returns the exact regions (cells) where the occurrences (leaf nodes)
        happened.
        
        """
        if self.occurrences:
            cells = map(lambda o : list(o.is_in),self.occurrences)
            cells = reduce(lambda a,b : a+b , cells)
            # take away repetition
            cells =  list(set(cells))
            self.involvedCells = cells
            return cells
        else:
            return self.involvedCells
        

    def getNeighboringTrees(self,filter_central_cell=True,reduce_trees=False):
        """
        It will return the trees associated with the neighbouring cells.
        Algorithm : 
            Get the exact cells,
            Get the neighbours
            Extract the occurrences for each cell.
            Instantiate the tree.
            
        Returns:
            List of NeoTrees
            
        Parameters:
            filter_central_cell : boolean flag, if False it will include de central cell as part of the neighbour list.
        
        """
        neighbourhood = Neighbourhood(self,1,filter_central_cell=filter_central_cell)
        return neighbourhood





    def expandNeighbouringTrees(self,n_order=1,filter_central_cell=True):
        """
        Expand the neighbourhood of influence
        """
        list_trees = self.getNeighboringTrees(filter_central_cell=filter_central_cell)
        ns = list_trees
        neighbours = [ns]
        if n_order > 1:
            for i in range(n_order - 1):
                ns = map(lambda n : n.getNeighboringTrees(filter_central_cell=filter_central_cell),ns)
                ns = reduce(lambda a,b : a + b , ns)
                neighbours.append(ns)
        
        neighbours = reduce(lambda a , b  : a + b, neighbours)
        
        neighbours = list(set(neighbours))
        if filter_central_cell:    
            neighbours = filter(lambda t : t!= self, neighbours)    
        self.neighbouringtrees = neighbours
        return neighbours





    def newExpand(self,n_order=1,filter_central_cell=True):
        list_trees = self.getNeighboringTrees()
        ns1 = list_trees
        neighbours = [ns1]
        ns0 = self
        if n_order > 1:
            for i in range(n_order - 1):
                border = list(set(ns1) - set(ns0))
                ns0 = ns1
                ns1 = map(lambda n : n.getNeighboringTrees(),border)
                ns1 = reduce(lambda a,b : a + b , ns1)
                neighbours.append(ns1)
        
        neighbours = reduce(lambda a , b  : a + b, neighbours)
        
        neighbours = list(set(neighbours))
        if filter_central_cell:    
            neighbours = filter(lambda t : t!= self, neighbours)    
        self.neighbouringtrees = neighbours
        return neighbours
        


    def mergeCells(self):
        """
        Returns a single polygon of all the interested cells.
        """
        cells = self.getExactCells()
        polygons = map(lambda c : c.polygon, cells)
        polygon = reduce(lambda p1,p2 : p1 + p2, polygons )
        return polygon



    def plantTreeNode(self):
        """
        Returns this TreeNode in the form of a TreeNeo.
        It adds the remaining nodes until root.
        """
        occurrences = self.occurrences
        ts = TreeNeo(occurrences)
        return ts



    def childrenInsideCellRatios(self,option=1):
        """
        Returns the insideCell Ratios of all the Children in a lazy list (iterator)
        
        Parameters: 
            option : 1 Ratios
            option : 2 number of cells in each layer.  
        """
        #return it.imap(lambda n : n.node.insideCellRatio(),self.children)
        
        import pandas as pd
        ratios = map(lambda n : n.node.insideCellRatio(option=option),self.children)
        data = pd.DataFrame(ratios).transpose()
        names = map(lambda n : n.name,self.children)
        data.columns = names
        return data

    def __eq__(self,other_tree):
        """
        Checks if two local trees are equivalent.
        Remember, this is the principle of invariantness (me, Badiou).
        """ 
        ## Developer note.
        ## See that there is a problem with the invariant of null trees.
        ## Now I can only think that two null trees are invariant if they have the same cell.
        try:
            this = self.node.node
        # If the node itself is the empty tree
        except AttributeError:
            this = None
        try:
            other_node = other_tree.node.node
        except AttributeError:
            other_node = None
        
        
        this_cells = self.getExactCells()
        other_cells = other_tree.getExactCells()
        if (this == other_node) and (this_cells == other_cells):
        ## Because it can be on the same cell but different taxonomic level or same taxonomic level different cell.    
        #if this_cells == other_cells:
            return True
        else:
            return False
#    def pullbackCellNodes(self):

    ## This is necesary, apparently the != is not working properly. 
    def __ne__(self,other_tree):
        truth = (self == other_tree)
        
        return not truth



    def __hash__(self):
        """
        This is needed for set operations.
        """
        return self.node.__hash__()


    def __and__(self,otherlocaltree):
        """
        Operator Overloading for calculating difference of Trees!
        In the search of the Monoid!
        New version!
        """
        
        # First, perform set operation on children.
        this = set(self.children)
        other = set(otherlocaltree.children)
        new = this & other
        # Now collapse occurrences (PROTOTYPE)
        # First we need to take select it's proper structure, looking for the distinct occurrences even if they have same node.
        idx_this = []
        idx_other = []
        for child in new:
            try:
                i = self.children.index(child)
                idx_this.append(i)
            except ValueError:
                continue 
            try:
                i = otherlocaltree.children.index(child)
                idx_other.append(i)
            except ValueError:
                continue
                
        occurrences_this = map(lambda i : self.children[i].occurrences,idx_this)
        occurrences_other = map(lambda i : otherlocaltree.children[i].occurrences,idx_other)
        new = occurrences_other + occurrences_this
        # reduce into a single cell
        new = reduce(lambda a,b : a+b , new)
        return TreeNeo(list_occurrences=new)     


    def __sub__(self,otherlocaltree):
        """
        Operator Overloading for calculating difference of Trees!
        In the search of the Monoid!
        New version!
        """
        
        # First, perform set operation on children.
        this = set(self.children)
        other = set(otherlocaltree.children)
        new = this - other
        # Now collapse occurrences (PROTOTYPE)
        # First we need to take select it's proper structure, looking for the distinct occurrences even if they have same node.
        idx_this = []
        idx_other = []
        for child in new:
            try:
                i = self.children.index(child)
                idx_this.append(i)
            except ValueError:
                continue 
            try:
                i = otherlocaltree.children.index(child)
                idx_other.append(i)
            except ValueError:
                continue
                
        occurrences_this = map(lambda i : self.children[i].occurrences,idx_this)
        occurrences_other = map(lambda i : otherlocaltree.children[i].occurrences,idx_other)
        new = occurrences_other + occurrences_this
        # reduce into a single cell
        new = reduce(lambda a,b : a+b , new)
        return TreeNeo(list_occurrences=new)   


    def __xor__(self,otherlocaltree):
        """
        Operator Overloading for calculating difference of Trees!
        In the search of the Monoid!
        New version!
        """
        
        # First, perform set operation on children.
        this = set(self.children)
        other = set(otherlocaltree.children)
        new = this ^ other
        # Now collapse occurrences (PROTOTYPE)
        # First we need to take select it's proper structure, looking for the distinct occurrences even if they have same node.
        idx_this = []
        idx_other = []
        for child in new:
            try:
                i = self.children.index(child)
                idx_this.append(i)
            except ValueError:
                continue 
            try:
                i = otherlocaltree.children.index(child)
                idx_other.append(i)
            except ValueError:
                continue
                
        occurrences_this = map(lambda i : self.children[i].occurrences,idx_this)
        occurrences_other = map(lambda i : otherlocaltree.children[i].occurrences,idx_other)
        new = occurrences_other + occurrences_this
        # reduce into a single cell
        new = reduce(lambda a,b : a+b , new)
        return TreeNeo(list_occurrences=new) 



    def __or__(self,other):
        if isinstance(other, LocalTree):
            other = other.plantTreeNode()
            this = self.plantTreeNode()
            new =  other + this    
            return new
        else:
            raise TypeError("Not same type")



    def exportTreeFormat(self):
        """
        Creates a string representation in a XML like structure.
        Isomorphic to a Context Free Language.
        Returns:
            string
            
        note : 
            This method is recursive
        """
        expression = "<%s:%s> \n " %(self.levelname,self.id)
        expression += "\t <name>%s<\name>\n" %( self.name)
        expression += "\t <count>%s<\count>\n" %( self.richness)
        expression = expression.encode('utf-8')
        #expression = "< Id: %s-%s: %s  : %s " %(self.level,self.levelname,self.levelname,self.name)
        for occurrence in self.children:
            try:    
                expression += occurrence.exportTreeFormat()
                #return expression                   
            except:
                 
                expression += "<\%s:%s>\n" %(self.levelname,self.id)
                #return expression  
                # magic step!
        return expression



    def pseudoPresenceAbsence(self,catalog_ids,level_id,selected_field='id'):
        """
        This method generates a list of presence absence based on a catalog list.
        That is, a list that includes the ids of certain taxa (e.g. taxa found at bigger scale). 
        It returns a list of 1 and 0's where each entry is a particular taxon and the entry 0 or 1 is if that taxon
        was found in the level_id of the current tree (self)
        
        Parameters:
            
            selected_field : id makes the selection for id. 
                          : name the selection for the name
            
        
        """
        levels = [self,self.kingdoms,self.phyla,self.classes,self.orders,self.families,self.genera,self.species,self.occurrences]
        level = levels[level_id]
        catalog_ids.sort()
        output = {}
        for id in catalog_ids:
            if selected_field == 'id':
                s = filter(lambda l : l.id == id,level)
            else:
                s = filter(lambda l : l.name == id,level)
            if s:
                output[id] = 1
            else:
                output[id] = 0
        return pandas.DataFrame.from_dict(output,orient='index')
                

    def countNodesFrequenciesOnList(self,list_of_trees):
        """
        Checks if every node in the tree is in how many members of the list.
        This is used for checking how many nodes of a tree are contained in an arbitrary list of trees.
        Returns:
            list of nodes
            
        note : 
            This method is recursive
        """
        hasNode = lambda node : lambda tree : tree.hasNode(node)
        # filter the trees that have the node in children
         

        for child in self.children:
            try:
                subtrees_with_node = filter(lambda tree : hasNode(child)(tree),list_of_trees) 
                child.n_presences_in_list = len(subtrees_with_node)
                n = child.countNodesFrequenciesOnList(list_of_trees) 
                logger.info("Going deep %s"%n)
            except:
                subtrees_with_node = filter(lambda tree : hasNode(child)(tree),list_of_trees) 
                child.n_presences_in_list = len(subtrees_with_node)
                continue
        return self.n_presences_in_list
  

            


class TreeNeo(LocalTree):
    """
    A prototype for reading taxonomic trees stored in the Neo4J database.
    """

    def __init__(self,list_occurrences,cell_object=''):
        """
        THIS IS A PROTOTYPE.
        For now it need a list of node occurrences. Use the function extractOccurrencesFromTaxonomies
        AOI should be a polygon data structure.
        
        """
        # First build list of nodes
        # i.e. take all the occurrences, extract the node then put everything in a list
        #self.occurrences = reduce( lambda one,two : one + two, [ map(lambda occurrence : occurrence.getNode(),occurrences )for occurrences in [ taxonomy.occurrences for taxonomy in list_taxonomies]])
        #self.occurrences =  reduce( lambda one,two : one + two ,[ list(occurrence) for occurrence in [ taxonomy.occurrences for taxonomy in list_taxonomies ]])
        if list_occurrences:
            self.occurrences = list_occurrences
            self.involvedCells = cell_object
            self.windUpLevels()
        else:
            logger.debug('No occurrences found. Returning empty')
            self.occurrences = []
            self.parent = 'No Data found'
            self.children = []
            self.node = None
            self.involvedCells = cell_object
            self.associatedData = RasterCollection(self)
            self.levels = [self]
        
            #return None
            #super(TreeNeo,self).__init__(root,children)
            
    def __repr__(self):
        try:
            cad = "<LocalTree Of Life | %s: %s - n.count : %s- >"%(self.levelname,self.name,self.richness)
        except:
            cad = "<LocalTree Of Life | %s: - n.count : %s- >"%('No record available',self.richness)        
    
        return cad.encode('utf-8')
   
    def setOccurrencesFromTaxonomies(self,list_of_taxonomies):
        """
        Updates the occurrences attribute to fit all the occurrences of the given list of taxonomies
        """
        self.occurrences =  reduce( lambda one,two : one + two ,[ list(occurrence) for occurrence in [ taxonomy.occurrences for taxonomy in list_of_taxonomies ]])
        #self.windUpLevels()


    def windUpLevels(self):
        """
        It uses the aggregator method to generate a nested LocalTree Structure.
        """
        self.species = aggregator(list(self.occurrences))
        self.genera = aggregator(self.species)
        self.families = aggregator(self.genera)
        self.orders = aggregator(self.families)
        self.classes = aggregator(self.orders)
        self.phyla = aggregator(self.classes)
        self.kingdoms = aggregator(self.phyla)
        root = aggregator(self.kingdoms).pop()
        # Reload Occurrences
        super(TreeNeo,self).__init__(root,root.children)
        # Reload Occurrences
        self.setOccurrences()
        self.levels = [self,self.kingdoms,self.phyla,self.classes,self.orders,self.families,self.genera,self.species,self.occurrences]



    def hasNode(self,TreeNode):
        """
        Checks if node exists in current tree.
        """
        if self.richness != 0:
            levels = self.levels
            t_l = TreeNode.level
            if t_l != 0 :
                ids_for_level = map(lambda l : l.id, levels[t_l])
                truth = TreeNode.id in ids_for_level
                return truth
            else:
                ids_for_level = [ levels[t_l].id ]
                truth = TreeNode.id in ids_for_level
                return truth
        else:
            # Case the tree is empty
            return False

    def __add__(self, tree_neo):
        """
        Operator Overloading for adding Trees!
        In the search of the Monoid!
        New version!
        """
        occurrences = self.occurrences
        other_occurrences = tree_neo.occurrences
        new_occs = occurrences + other_occurrences
        new_occs = list(set(new_occs))
        occs = copy.copy(new_occs)
        logger.info("Merging Trees")
        return TreeNeo(list_occurrences=occs)  


    def rankLevels(self):
        """
        Ranks the taxonomicv levels (list of Families, Genera, etc) according to the attribute:
        n_presences_in_list
        """
        count = lambda obj : obj.n_presences_in_list
        levels = [self.kingdoms,self.classes,self.orders,self.families,self.genera,self.species]
        try:
            logger.info("Sorting nodes in taxonomic levels by counts on frequencies")
            map(lambda level: level.sort(key=count,reverse=True),levels)
            return True
        except:
            logger.error("No values of presences in list. \n Hint: RuncountNodesFrequenciesOnList first ")
            return None


class Neighbourhood(object):
    """
    Class that defines the neighbourhood object (Similar to gridded taxonomy)
    """
    def __init__(self,central_node,size,filter_central_cell=True):
        """
        Constructor
        """
        self.center = central_node
        self.size = size
        self.neighbours = self.getNeighboringTrees(filter_central_cell=filter_central_cell)

    def __iter__(self):
        return iter(self.neighbours)


    @property
    def extendedTree(self):
        """
        Merges the neighbouring trees into one
        """
        bigtree = reduce(lambda t1,t2 : t1 + t2 , self.neighbours)
        return bigtree


    def getEnvironmentalData(self):
        """
        Returns a DataFrame of all the environmental covariates
        """
        environment = map(lambda t : t.associatedData.getEnvironmentalVariablesCells(),self.neighbours)
        env = pandas.DataFrame.from_dict(environment)
        return env



    def getNeighboringTrees(self,filter_central_cell=True,reduce_trees=False,size=1,update_attribute=True):
        """
        It will return the trees associated with the neighbouring cells.
        Algorithm : 
            Get the exact cells,
            Get the neighbours
            Extract the occurrences for each cell.
            Instantiate the tree.
            
        Returns:
            List of NeoTrees
            
        Parameters:
            filter_central_cell : boolean flag, if False it will include de central cell as part of the neighbour list.
        
        """
        cells = self.center.getExactCells()
        cells = map(lambda c: c.getNeighbours(),cells)
        # to extract the cells from the nested list. i.e. all the cells are in a list 
        cells = reduce(lambda a,b : a+b , cells)
        # Insert the central cell
        #cells.append(self.center.getExactCells().pop()) 
        
        for i in range(size -1):
            cell_neighbours = map(lambda c: c.getNeighbours(),cells)
            cells = reduce(lambda l1 , l2  : l1 + l2, cell_neighbours)
            #if not filter_central_cell:
            #cells.append(self.center.getExactCells().pop()) 
            # remove repeated
            cells = list(set(cells))    

            
        occurrences = map(lambda oc : oc.occurrencesHere(),cells)
        ## prototyping
        duples = zip(occurrences,cells)
        trees = []
        for list_, cell in duples:
            trees.append(TreeNeo(list_,[cell]))

        # This if the filter central cell parameter is chosen.
        if filter_central_cell:    
            trees = filter(lambda t : t!= self.center, trees)    

        if reduce_trees:
            trees = reduce(lambda t1,t2 : t1 + t2, trees)

        if update_attribute:
            self.neighbours = trees
            self.size = size
            
        return trees
        

    def expandNeighbourhood(self,size,filter_central_cell=True, reduce_trees=False):
        """
        Set the desire neighbourhood as the attribute.
        """
        ns = self.getNeighboringTrees(filter_central_cell=filter_central_cell, reduce_trees=reduce_trees, size=size)

        self.neighbours = ns

    def getCooccurrenceMatrix(self,taxonomic_level=1):
        """
        Returns the matrix of co-occurrences (taxa that share a given cell (neighbour's cell) ) for a specific taxonomic level.
        """
        bt = self.extendedTree
        nodes = bt.levels[taxonomic_level]
        # sort the nodes according to its id
        nodes.sort(key=lambda t : t.id)
        occurrences = {}
        #for neighbour in self.neighbours:
        for node in nodes:
            existence = map(lambda neighbour : int(neighbour.hasNode(node)),self.neighbours)
            occurrences[node.name] = existence
            #existence = map(lambda node : int(neighbour.hasNode(node)),nodes)
            #occurrences.append(existence)
        ocs = pandas.DataFrame.from_dict(occurrences)
        return ocs
    
    
    def getCentroids(self,asnumpyarray=True):
        """
        Returns the Points of position, long,lat
        """
        cells = map(lambda tree : tree.getExactCells(),self.neighbours)
        cells = reduce(lambda a,b : a + b , cells)
        points = map(lambda c : c.centroid,cells)
        if asnumpyarray:
            ps = map(lambda p : (p.x,p.y), points)
            points = np.atleast_2d(ps)
            
            p = pandas.DataFrame(points)
            p.columns = ['x','y']
        return p
    