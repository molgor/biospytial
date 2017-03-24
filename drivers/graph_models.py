# graph_models.py
# The Module for Object Graph Mapping OGM . 
# Currently in Neo4J
 
# Author: Juan Escamilla 
# Date: 26/10/2016
 
#!/usr/bin/env python
#-*- coding: utf-8 -*-


import logging
logger = logging.getLogger('biospytial.graph_models')

from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from django.contrib.gis.geos import GEOSGeometry
from itertools import groupby
#from drivers.tree_builder import LocalTree

from biospytial import settings
neoparams = settings.NEO4J_DATABASES['default']
uri = "http://%(HOST)s:%(PORT)s%(ENDPOINT)s" % neoparams

import py2neo
graph = py2neo.Graph(uri,bolt=True)

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

global ISCONTAINED
ISCONTAINED = "IS_CONTAINED_IN"


# Fixes an bug from the original library
class GraphObject(GraphObject):
    
    def __hash__(self, *args, **kwargs):
        """
        Method overwritten because it was broken.
        This was necessary to have hashable objects and converting to Sets. 
        Uff it wa difficult to find this problem. 
        https://docs.python.org/2/library/stdtypes.html#set
        """
        return hash(self.__ogm__.node)


# Nodes for Raster data
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



## Environmental Data.
## Here insert for inserting new variables from the Knowledge Graph.

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
 
 
 
 
# The atomic entity, the random variable, The Unit !
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
    parent_link = RelatedTo("TreeNode",TAXDESCEND)
    children_link = RelatedTo("TreeNode",TAXASCEND)
    has_event = RelatedFrom("TreeNode",HASEVENT)
    
    

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
        if len(parent) > 1 or not isinstance(parent[0],TreeNode):
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





class TreeNode(GraphObject):
    """
    """
    __primarykey__ = "id"
    
    name = Property()
    
    id = Property()
    levelname = Property()
    level = Property()
    abundance = Property()
    keyword = Property()
    
    parent_link = RelatedTo("TreeNode",TAXDESCEND)
    children_link = RelatedTo("TreeNode",TAXASCEND)
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
        Does not take into account the current leaf nodes in the TreeNode.
        It gives all the nodes of type cell where this node has been found in all the database.
        """
        return iter(self.is_in)


    def __repr__(self):
        c = "<TreeNode type: %s id = %s name: %s>"%(str(self.levelname),str(self.__primaryvalue__),str(self.name.encode('utf-8')))
        return c

    def setLabel(self,labelname):
        """
        Usefull when selecting arbitrary nodes of certain taxonomy.
        """
        self.__primarylabel__ = labelname
        

    def getParent(self):
        parent = list(self.parent_link)
        if len(parent) > 1 or not isinstance(parent[0],TreeNode):
            raise TypeError
        else:
            return parent.pop()

    def getSiblings(self):
        parent = self.getParent()
        siblings = parent.children
        #siblings = filter(lambda node : node != self,siblings)
        return siblings
    

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

class Kingdom(TreeNode):
   __property_label__ ='Kingdom'

class Phylum(TreeNode):
   __property_label__ ='Phylum'
   
class Class(TreeNode):
   __property_label__ ='Class'

class Order(TreeNode):
   __property_label__ ='Order'
   
class Family(TreeNode):
    __property_label__ ='Family'

class Genus(TreeNode):
   __property_label__ ='Genus' 

class Specie(TreeNode):
   __property_label__ ='Specie'
   
   



## Rememeber that We have two semilattices. 
## ONe given by the nature of the object (Occurrence) and it's taxonomy (Tree Node).
## The other given by the location in the quadtree (Cell)
 

class Cell(GraphObject):
    
    __primarykey__ = 'id'
    __primarylabel__ = 'Cell'
    name = Property()
    longitude = Property()
    latitude = Property()
    cell = Property()
    id = Property()
       
    
    
    connected_to = RelatedTo("Cell", ISNEIGHBOUR)
    

    Occurrences = RelatedFrom(Occurrence, ISIN)
    
    #LocalTree  = RelatedFrom(TreeNode, ISIN)
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
        # testing thingy
        rn.append(self)
        return rn
        
    def occurrencesHere(self):
        """
        Filter the list of occurrences.
        """
        occs = filter(lambda l : l.pk,self.Occurrences)
        return occs        


class Mex4km_(GraphObject):
    
    __primarykey__ = 'id'
    __primarylabel__ = 'mex4km'
    name = Property()
    longitude = Property()
    latitude = Property()
    cell = Property()
    id = Property()
       
    
    
    connected_to = RelatedTo("Cell", ISNEIGHBOUR)
    

    Occurrences = RelatedFrom(Occurrence, ISIN)
    
    #LocalTree  = RelatedFrom(TreeNode, ISIN)
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
        # testing thingy
        rn.append(self)
        return rn
        
    def occurrencesHere(self):
        """
        Filter the list of occurrences.
        """
        occs = filter(lambda l : l.pk,self.Occurrences)
        return occs   



class Mex4km(Cell):
    
    __primarylabel__ = 'mex4km'
    connected_to = RelatedTo("mex4km", ISNEIGHBOUR)
    contained_in = RelatedTo("Cell", ISCONTAINED)
########THIS IS NOT WORKING
    @classmethod
    def select(cls, graph, primary_value=None):
        return super(Mex4km, cls).select(graph, primary_value=primary_value)



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



