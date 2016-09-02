#!/usr/bin/env python
#-*- coding: utf-8 -*-


import logging
from django.contrib.gis.geos import GEOSGeometry

import pandas
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from raster_api.tools import RasterData
from itertools import groupby
from collections import OrderedDict
from compiler.ast import nodes
from raster_api.models import raster_models


logger = logging.getLogger('biospatial.neo4j_reader')

import py2neo
graph = py2neo.Graph()

global TAXDESCEND
TAXDESCEND = "IS_A_MEMBER_OF"

global TAXASCEND
TAXASCEND = "IS_PARENT_OF"
global ISNEIGHBOUR 
ISNEIGHBOUR = "IS_NEIGHBOUR_OF"
global ISIN 
ISIN = "IS_IN"

global HASEVENT
HASEVENT = "HAS_EVENT"

global RASTERDICT





class GraphObject(GraphObject):
    
    def __hash__(self, *args, **kwargs):
        """
        Method overwritten because it was broken.
        This was necessary to have hashable objects and converting to Sets. 
        Uff it wa difficult to find this problem. 
        https://docs.python.org/2/library/stdtypes.html#set
        """
        return hash(self.__ogm__.node)



class RasterNode(GraphObject):
    """
    Super class for each node.
    """
    __primarykey__ = "uniqueid"
    uniqueid = Property()
    regval = Property('reg.val')
    value = Property()
    
    def __repr__(self):
        c = "<Raster Data type: %s value = %s >"%(str(self.__primarylabel__),str(self.regval))
        return c





class WindSpeed(RasterNode):
    """
    WindSpeed
    """
    __primarylabel__ = 'WindSpeed-30s'
    has_events = RelatedFrom("Occurrence",'WindSpeed')

class Elevation(RasterNode):
    """
    Elevation
    """
    __primarylabel__ = 'DEM_12'
    has_events = RelatedFrom("Occurrence",'Elevation')
    
class Vapor(RasterNode):
    __primarylabel__ = 'Vapor-30s'
    has_events = RelatedFrom("Occurrence",'Vapor')
            
class MaxTemp(RasterNode):   
    __primarylabel__ = 'MaxTemp-30s'
    has_events = RelatedFrom("Occurrence",'MaxTemperature')
 
class MinTemp(RasterNode):    
    __primarylabel__ = 'MinTemp-30s'
    has_events = RelatedFrom("Occurrence",'MinTemperature')
    
class MeanTemp(RasterNode):
    __primarylabel__ = 'MeanTemp-30s'
    has_events = RelatedFrom("Occurrence",'MeanTemperature')
      
class SolarRadiation(RasterNode):
    __primarylabel__ = 'SlrRad-30s'
    has_events = RelatedFrom("Occurrence",'SolarRadiation')
  
class Precipitation(RasterNode):        
    __primarylabel__ = 'Prec-30s'
    has_events = RelatedFrom("Occurrence",'Precipitation')
 



"""
WindSpeed
Elevation
Vapor     
MaxTemp
MinTemp
MeanTemp
SolarRadiation
Precipitation
"""


class Occurrence(GraphObject):
    """
    Lets see hoe this works
    """
    
    __primarykey__ = "pk"
    __primarylabel__ = 'Occurrence'
    
    
    name = Property()
    month = Property()
    level = Property()
    year = Property()
    pk = Property()
    levelname = Property()
    longitude = Property()
    latitude = Property()
    event_date = Property()
    
    
    
    #species = RelatedFrom("Specie", "HAS_EVENT")
    is_in  = RelatedTo("Cell",ISIN)
    #families = RelatedFrom("Family", "HAS_EVENT")
    parent_link = RelatedTo("Tree",TAXDESCEND)
    children_link = RelatedTo("Tree",TAXASCEND)
    has_event = RelatedFrom("Tree",HASEVENT)
    
    

    lives_with_windspeed_of = RelatedTo(WindSpeed,'WindSpeed')
    lives_in_a_elevation_of = RelatedTo(Elevation,'Elevation') 
    lives_with_vapor_pressure_of  = RelatedTo(Vapor,'Vapor')   
    lives_in_a_maximum_temperature_of = RelatedTo(MaxTemp,'MaxTemperature')
    lives_in_a_minimum_temperature_of = RelatedTo(MinTemp,'MinTemperature')
    lives_in_a_mean_temperature_of = RelatedTo(MeanTemp,'MeanTemperature')
    lives_with_a_solar_radiation_of = RelatedTo(SolarRadiation,'SolarRadiation')
    lives_with_a_precipitation_of = RelatedTo(Precipitation,'Precipitation')


    
    def __init__(self,filtered_nodes):
        """
        Test
        """
        self.filtered_nodes = filtered_nodes

    def getParent(self):
        parent = list(self.parent_link)
        if len(parent) > 1 or not isinstance(parent[0],Tree):
            raise TypeError
        else:
            return parent.pop()

    def getAncestors(self,depth=8):
        """
        Given the parameter depth it walks through the Subgraph Taxonomy
        Starting from the Occurrence Node to the depth specified.
        Remember that there is a loop in the LUCA node there fore, 
        """
        
        nodes = []
        parent = self
        for i in range(depth):
            parent = parent.getParent()
            nodes.append(parent)
            
        return nodes

    def isDescendantOf(self,ancestor,depth=8):
        """
        Ancestor is a tree node. Returns True if this occurrence has 'ancestor' in some level of it's Ancestors chain.
        """
        parent = self
        for i in range(depth):
            parent = parent.getParent()
            logger.debug("Okey")
            if ancestor == parent:
                
                i = depth
                return True
                
        return False
            
            
    
    def getCells(self):
        """
        Returns all the cells that are associated with this taxa.
        Occurrence is the Leaf Node of the Tree Of life, therefore 
        It gives the real cell where it was found.
        """
        
        l = list(self.is_in)
        if len(l) > 1 :
            raise TypeError
        else:
            try:
                return l.pop()
            except:
                return None


    
    
    def pullbackRasterNodes(self,raster_name):
        """
        Returns the associated value of each occurrence based on the available models.
        """
        models = {'Elevation' : self.lives_in_a_elevation_of ,
          'MaxTemperature' : self.lives_in_a_maximum_temperature_of,
          'MinTemperature' : self.lives_in_a_minimum_temperature_of,
          'MeanTemperature' : self.lives_in_a_mean_temperature_of,
          'Precipitation' : self.lives_with_a_precipitation_of,
          'Vapor' : self.lives_with_vapor_pressure_of,
          'SolarRadiation' : self.lives_with_a_solar_radiation_of,
          'WindSpeed' : self.lives_with_windspeed_of
          }
    
        
        return iter(models[raster_name])
    
    

class Tree(GraphObject):
    """
    """
    __primarykey__ = "id"
    
    name = Property()
    
    id = Property()
    levelname = Property()
    level = Property()
    abundance = Property()
    keyword = Property()
    
    parent_link = RelatedTo("Tree",TAXDESCEND)
    children_link = RelatedTo("Tree",TAXASCEND)
    is_in = RelatedTo("Cell",ISIN)
    
    has_events = RelatedTo("Occurrence",HASEVENT)

    localoccurrences = []

    @property 
    def children(self):
        return iter(self.children_link)
    

    @property
    def allOccurrences(self):
        """
        Retrieve all data! related to this taxonimic node.
        """
        return iter(self.has_events)
    
    def setLocalOccurrences(self,list_occurrences):
        depth = self.level
        self.localoccurrences = filter(lambda o: o.isDescendantOf(self,depth=depth),list_occurrences)
    
    #def localOccurrences(self):
    #    ls = filter(lambda o: o.isDescendantOf(self),self.localoccurrences)
     #   return ls
    
    @property
    def cells(self):
        """
        Returns all the cells that are associated with this taxa.
        Does not take into account the current leaf nodes in the Tree.
        It gives all the nodes of type cell where this node has been found in all the database.
        """
        return iter(self.is_in)


    def __repr__(self):
        c = "<Tree type: %s id = %s name: %s>"%(str(self.levelname),str(self.__primaryvalue__),str(self.name.encode('utf-8')))
        return c



    def getParent(self):
        parent = list(self.parent_link)
        if len(parent) > 1 or not isinstance(parent[0],Tree):
            raise TypeError
        else:
            return parent.pop()

    def getSiblings(self):
        parent = self.getParent()
        siblings = parent.children
        #siblings = filter(lambda node : node != self,siblings)
        return siblings
    
    
    def filterWithThis(self,occurrence_list):
        """
        Supposing the list is made of NODE Occurrence
        """
        for occurrence in occurrence_list:
            pass
        



    def _isOccurrence(self):
        if self.level == 999:
            return True
        else:
            return False
    
    def _isRoot(self):
        if self.level == 0:
            return True
        else:
            return False
        
    def _isKingdom(self):
        if self.level == 1:
            return True
        else:
            return False
        
        
    def _isPhylum(self):
        if self.level == 2:
            return True
        else:
            return False
                

    def _isClass(self):
        if self.level == 3:
            return True
        else:
            return False
        
        
    def _isOrder(self):
        if self.level == 4:
            return True
        else:
            return False
        
        
    def _isFamily(self):
        if self.level == 5:
            return True
        else:
            return False
        
    
    def _isGenus(self):
        if self.level == 6:
            return True
        else:
            return False
        
        
    def _isSpecie(self):
        if self.level == 7:
            return True
        else:
            return False









class Cell(GraphObject):
    
    __primarykey__ = 'id'
    __primarylabel__ = 'Cell'
    
    name = Property()
    longitude = Property()
    latitude = Property()
    cell = Property()
    id = Property()
       
    
    
    connected_to = RelatedTo("Cell", ISNEIGHBOUR)
    
    #connected_from = RelatedFrom("Cell", ISNEIGHBOUR)
    LocaTree  = RelatedFrom(Tree, ISIN)
    #families = RelatedFrom("Family",ISIN)
    #families = RelatedFrom("Family", "HAS_EVENT")    

    @property
    def centroid(self):
        pointstr = 'POINT(%s %s)'%(self.longitude,self.latitude)
        point = GEOSGeometry(pointstr)
        return point
    
    @property
    def polygon(self):
        polygon = GEOSGeometry(self.cell)
        return polygon


    def getNeighbours(self):
        #ln = [n for n in self.connected_from]
        rn = [n for n in self.connected_to]
        return rn
        
    def OccurrencesHere(self):
        """
        Filter the list of occurrences.
        """




        

 


class LocalTree(object):
    def __init__(self,this_node,children):
        self.node = this_node
        self.children = children
        self.parent = self.node.getParent()
        self.name = self.node.name
        self.id = self.node.id
        self.levelname = self.node.levelname
        self.level = self.node.levelname
        self.occurrences = []
        self.involvedCells = []
        #self.setOccurrences()
                

    @property
    def richness(self):
        return len(self.occurrences)
    
    
    def getParent(self):
        return self.parent


    def __repr__(self):
        cad = "<SubTree Of Life | %s: %s -%s- >"%(self.levelname,self.name,self.id)
        return cad.encode('utf-8')

    def setOccurrences(self):
        """
        Sets the corresponding occurrences for each level.
        It uses recursion and stores the output in each level (occurrences) on it's proper attribute.
        The output of each children is merged (union in sets) together to give the total occurrences of each children of the current node (LocalTree).

        notes :
        
            This method is elegant!
            Took me some time to figure it out. I think I cannot make something more efficient.
        
        
        """
        for occurrence in self.children:
            if not isinstance(occurrence, Occurrence):
                logger.info("Children are not type occurrence")
                occurrences_on_children = occurrence.setOccurrences()
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
        nodes_iters = map(lambda oc : oc.pullbackRasterNodes(raster_name),self.occurrences)
        nodes = reduce(lambda n1,n2 : list(n1) + list(n2) , nodes_iters)
        return nodes
    

    def getExactCells(self):
        """
        Returns the exact regions (cells) where the occurrences (leaf nodes)
        happened.
        """
        
        cells = map(lambda o : list(o.is_in),self.occurrences)
        cells = reduce(lambda a,b : a+b , cells)
        # take away repetition
        cells =  list(set(cells))
        self.involvedCells = cells
        return cells
        

    def mergeCells(self):
        """
        Returns a single polygon of all the interested cells.
        """
        cells = self.getExactCells()
        polygons = map(lambda c : c.polygon, cells)
        polygon = reduce(lambda p1,p2 : p1 + p2, polygons )
        return polygon



#    def pullbackCellNodes(self):


def aggregator(list_sp):
    ##Comming from the first collider
    
    list_sp.sort(key=lambda l : l.getParent().id)
    
    #list_nodes.sort(key=lambda node :  node.getParent().id)
    grouper = groupby(list_sp, lambda node : node.getParent())
    output = []
    for node,children in grouper:
        s = LocalTree(node,list(children))
        output.append(s)
    return output
       
def extractOccurrencesFromTaxonomies(list_of_taxonomies):
    """
    Updates the occurrences attribute to fit all the occurrences of the given list of taxonomies
    """
    occurrences =  reduce( lambda one,two : one + two ,[ list(occurrence) for occurrence in [ taxonomy.occurrences for taxonomy in list_of_taxonomies ]])
    return occurrences
    #self.windUpLevels()


class TreeNeo(LocalTree):
    """
    A prototype for reading taxonomic trees stored in the Neo4J database.
    """

    def __init__(self,list_occurrences,spatiotemporalcontext=''):
        """
        THIS IS A PROTOTYPE.
        For now it need a list of occurrences GeoQuerySet.
        spatiotemporalcontext should be a structure that defines a compact set.
        
        """
        # First build list of nodes
        # i.e. take all the occurrences, extract the node then put everything in a list
        #self.occurrences = reduce( lambda one,two : one + two, [ map(lambda occurrence : occurrence.getNode(),occurrences )for occurrences in [ taxonomy.occurrences for taxonomy in list_taxonomies]])
        #self.occurrences =  reduce( lambda one,two : one + two ,[ list(occurrence) for occurrence in [ taxonomy.occurrences for taxonomy in list_taxonomies ]])
        self.occurrences = list_occurrences
        self.windUpLevels()
        """
        self.species = []
        self.genera = []
        self.families = []
        self.orders = []
        self.classes = []
        self.phyla = []
        self.kingdoms = []
        """
                
    @property
    def nodeOccurrences(self):
        """
        Converts the occurrences to OGM occurrences
        It's a generator. For avoiding massive use of memory.
        """
        
        for occurrence in self.occurrences:
            yield occurrence.asOccurrenceOGM()

   
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
        self.species = aggregator(list(self.nodeOccurrences))
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
        logger.info("Merging Trees")
        return TreeNeo(list_occurrences=new_occs)
        
    
    def __repr__(self):
        cad = "<LocalTree Of Life | %s: %s -%s- >"%(self.levelname,self.name,self.id)
        return cad.encode('utf-8') 
 
 
 
class RasterCollection(object):
    """
    This class defines a data structure of the associated values and areas of the occurrences involving a specific Local Tree Level.
    """
    
    def __init__(self,Tree):
        self.tree = Tree
        self.rasternodes = []
        self.table = []

    
    def getMeanTemperaturePoints(self):
        temps = self.tree.pullbackRasterNodes('MeanTemperature')
        self.rasternodes = temps
        return temps
    
    
    def associateMeanTemperatureRasterData(self):
        """
        Get the cells involved
        PROTOTYPE NEED CHANGE FOR INCLUDING OTHER RASTER DATA
        """
        polygon = self.tree.mergeCells()
        raster = RasterData(raster_models[3],polygon)
        raster.getRaster()
        return raster
        
    
    def transformToTable(self):
        """
        Transforms the list of raster nodes into 
        """
        values = map(lambda node : node.value,self.rasternodes)
        pd = pandas.DataFrame(values)
        return pd
    
    
    
    
        