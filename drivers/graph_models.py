# -*- coding: utf-8 -*-
# graph_models.py
# The Module for Object Graph Mapping OGM . 
# Currently in Neo4J
 
# Author: Juan Escamilla 
# Date: 26/10/2016
 
#!/usr/bin/env python



import logging
import itertools


#from drivers.tree_builder import TreeNeo

logger = logging.getLogger('biospytial.graph_models')

from py2neo import NodeSelector
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Related
from django.contrib.gis.geos import GEOSGeometry
from itertools import groupby, imap
#from drivers.tree_builder import LocalTree
from biospytial import settings
from raster_api.tools import RasterData
from raster_api.models import raster_models_dic,raster_models
import networkx as nt

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


global BOTTOMSCALE_CLASSNODE
BOTTOMSCALE_CLASSNODE = "Mex4km"



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
    Occurrence class for maping objects to nodes.
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
    #is_in  = RelatedTo("Cell",ISIN)
    is_in  = RelatedTo(BOTTOMSCALE_CLASSNODE,ISIN)
    #families = RelatedFrom("Family", "HAS_EVENT")
    parent_link = RelatedTo("Specie",TAXDESCEND)
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
        Returns the associated value of each occurrence based on the available spystats.
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
    #is_in = Related("Cell",ISIN)
    is_in  = RelatedTo(BOTTOMSCALE_CLASSNODE,ISIN)
    has_events = RelatedTo("Occurrence",HASEVENT)

    localoccurrences = []



    @property 
    def children(self):
        return iter(self.children_link)
    


    @property
    def allOccurrences(self):
        """
        Retrieve all data! related to this taxonomic node.
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
        #return self.is_in


    def getCellsById(self):
        """
        Get's the associated cells by Id. 
        Optimized with a Cypher query to be very fast.
        It will return a list of ids that can be used in the sampling method.
        """
        from pandas import DataFrame as df
        cell_node_type = self.is_in.related_class
        cypher_str = "MATCH (b:%s {id:%s})-[r:IS_IN]->(c:%s) Return c.id"%(self.__primarylabel__,self.id,cell_node_type.__primarylabel__)
        try:
            n = graph.data(cypher_str)
            ids = [o['c.id'] for o in n]
            #selection_of_cells = cell_node_type.select(graph).where("_.id IN  %s "%ids)
            return ids
    

        except AttributeError:
            logger.error("Not a Node Object defined in the Graph Database")
            raise



    
    def giveNCells(self,k=10):
        """
        Gives the first 10 elements of the total list (which is an iterator)
        """
        return itertools.islice(self.is_in,k)

    def __repr__(self):
        ## converting to ascii values ignoring special characters.
        ## deprecated when migrating to python 3
        c = "<TreeNode type: %s id = %s name: %s>"%(unicode(self.levelname),unicode(self.__primaryvalue__),self.name.encode('ascii','ignore'))
        #.encode('utf-8')
        return c

    def setLabel(self,labelname):
        """
        Useful when selecting arbitrary nodes of certain taxonomy.
        """
        self.__primarylabel__ = labelname
        

    def getParent(self):
        parent = list(self.parent_link)
        # Se if its not empty
        if parent :
            if len(parent) > 1 or not isinstance(parent[0],TreeNode):
                raise TypeError
            else:
                return parent.pop()
        else:
            raise TypeError

    def getSiblings(self):
        parent = self.getParent()
        siblings = parent.children
        #siblings = filter(lambda node : node != self,siblings)
        return siblings
    
    def getAncestors(self):
        """
        Given the parameter depth it walks through the Subgraph Taxonomy
        Starting from the Occurrence Node to the depth specified.
        Remember that there is a loop in the LUCA node therefore.
        
        Returns a networkx.Graph object
        """
            
        
        G = nt.Graph()
        this_node = self
        while not isinstance(this_node,Root):
            next_node = this_node.getParent()
            G.add_edge(this_node, next_node)
            this_node = next_node
        return G

    def mergeLinageWithNode(self,other_node):
        """
        Merges the linages (ancestors) between the current node and another.
        Parameters:
            other_node : A TreeNode instance.
        Returns:
            a Networkx.Graph instance
        """
        this_ancestors = self.getAncestors()
        other_ancestors = other_node.getAncestors() 
        new_graph = nt.compose(this_ancestors, other_ancestors)
        return new_graph


    def taxonomicDistanceTo(self,other_node,depth=8):
        """
        Calculates the taxonomic distance (simple) between this node and another.
        Parameters:
            other_node : A TreeNode instance.
        Returns:
            Distance : Integer
            
        note: It is possible to use an extra argument in the shortestpath method.
        Select a given attribute as weight. See documentation.   
        """
        merged = self.mergeLinageWithNode(other_node)
        return nt.shortest_path_length(merged,source=self,target=other_node)
        
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
        
        
        
    def getAssociatedTrees(self,first_n_cells=10):
        """
        Returns an iterator of trees defined on each of the cells where the Node has events
        Parameter :
            first_n_cells : Number of cells to obtain 
            note:
             choose first_n_cells = 'all' to obtain all the cells.
        """
        logger.info("Retrieving cells")
        #cells = self.cells
        logger.info("Done!")
        logger.info("Retriving Occurrences")
        from drivers.tree_builder import TreeNeo
        if first_n_cells != "all":
            try:
                cs = self.giveNCells(k=first_n_cells)
            except:
                logger.error("Bad parameter first_n_cells. Use an integer or \'all\' .")
        else:
            cs = self.cells
        itrees = imap(lambda c : TreeNeo(c.occurrencesHere()),cs)
        
        return itrees

    def getUpperScaleCells(self):
        """
        si mira, te vengo manejando lo que es el m'etodo para obtener las celdas a una resoluci'on espacial mayor.
        La inmediata superior.
        
        Returns list of upper scale cells.
        """
        #upcell = lambda cell : list(cell.contained_in)
        #upper_cells = imap(upcell,self.cells)
        #logger.info("Reducing cells")
        #upp_cells = list(set(reduce(lambda c1,c2 : c1 + c2 ,upper_cells)))
        #return upp_cells
    
        upcell = lambda cell : cell.upperCell.next()
        upper_cells = imap(upcell,self.cells)
        logger.info("Reducing cells")
        return upper_cells
    
    def insideCellRatio(self,cells_list='',option=1):
        """
        Scales 
        Calculates the inside cell ratio for all scales
        Returns list of ratios 
        
        parameters: 
             option : 1 
                 returns ratios
            option : 2
                returns true values (number of cells)
        """
        nested_cells = self.propagateCells(cells_list)
        lengths = map(lambda lc : float(len(lc)),nested_cells)
        if option == 2:
            return lengths
        elif option == 1:
            c = lengths
            return [c[i+1]/c[i] for i in range(len(c)-1) ]
    
    def propagateCells(self,cells_list=''):
        """
        Extracts the cells by going upstream in the scales.
        It uses the POSET structure of the Quadtree.
        """
        
        ## This function maps all the cells given by the parameter cells and extract the upperCell.
        ## Later performs a cast list -> set to remove repetitions

        if not cells_list:
            cells_list = list(self.cells)
        levels = [list(cells_list)]    
        getUpperCells = lambda list_of_cells : set(imap(lambda cell : list(cell.upperCell)[0],list_of_cells))
        finish = False
        i = 0
        #import ipdb; ipdb.set_trace()
        while not finish:
            logger.info("Raising scale layer %s"%i)
            try:
                if cells_list:
                    cells_list = getUpperCells(cells_list)
                    levels.append(cells_list)
                    i += 1
                else:
                    finish = True
            except:
                finish = True
            
        return levels
            

class Root(TreeNode):
    __primarylabel__  ='Root'
    __primarykey__ = "id"
    parent_link = RelatedTo("Root",TAXDESCEND)
    children_link = RelatedTo("Kingdom",TAXASCEND)
    #parent_link = None
    

class Kingdom(TreeNode):
    __primarylabel__  ='Kingdom'
    __primarykey__ = "id"
    parent_link = RelatedTo("Root",TAXDESCEND)
    children_link = RelatedTo("Phylum",TAXASCEND)

class Phylum(TreeNode):
    __primarylabel__  ='Phylum'
    __primarykey__ = "id"
    parent_link = RelatedTo("Kingdom",TAXDESCEND)
    children_link = RelatedTo("Class_",TAXASCEND)
   
class Class_(TreeNode):
    __primarylabel__  ='Class'
    __primarykey__ = "id"
    parent_link = RelatedTo("Phylum",TAXDESCEND)
    children_link = RelatedTo("Order",TAXASCEND)

class Order(TreeNode):
    __primarylabel__  ='Order'
    __primarykey__ = "id"
    parent_link = RelatedTo("Class_",TAXDESCEND)
    children_link = RelatedTo("Family",TAXASCEND)
   
class Family(TreeNode):
    __primarylabel__ = 'Family'
    __primarykey__ = "id"
    parent_link = RelatedTo("Order",TAXDESCEND)
    children_link = RelatedTo("Genus",TAXASCEND)
    #__property_label__ ='Family'

class Genus(TreeNode):
    __primarylabel__  ='Genus'
    __primarykey__ = "id"
    parent_link = RelatedTo("Family",TAXDESCEND)
    children_link = RelatedTo("Specie",TAXASCEND) 

class Specie(TreeNode):
    __primarylabel__  ='Specie'
    __primarykey__ = "id"
    parent_link = RelatedTo("Genus",TAXDESCEND)
    children_link = RelatedTo("Occurrence",TAXASCEND)   
   



## Rememeber that We have two semilattices. 
## ONe given by the nature of the object (Occurrence) and it's taxonomy (Tree Node).
## The other given by the location in the quadtree (Cell)
 

class Cell(GraphObject):
    
    __primarykey__ = 'id'
    __primarylabel__ = 'Cell'
    #__property_label__ ='Cell'
    name = Property()
    longitude = Property()
    latitude = Property()
    cell = Property()
    id = Property()
    
    ## Default Referencing System
    srid = settings.CELL_SRID
    
    
    connected_to = RelatedTo("Cell", ISNEIGHBOUR)
    
    contained_in = RelatedTo("Cell", ISCONTAINED)

    #Occurrences = RelatedFrom(Occurrence, ISIN)
    
    LocalTree  = RelatedFrom(TreeNode, ISIN)
    #Families = RelatedFrom("Family",ISIN)
    #families = RelatedFrom("Family", "HAS_EVENT")    

    def _getAssociatedNodesPerTaxonLevel(self,ClassNode):
        """
        Gets the family nodes
        It's a test
        """
        label = self.__primarylabel__
        pv = self.__primaryvalue__
        pk = self.__primarykey__
        targetlabel = ClassNode.__primarylabel__
        targetpk = ClassNode.__primarykey__
        query = "MATCH (a:%s {%s:%s})<-[_:IS_IN]-(b:%s) RETURN b.%s"%(label,pk,pv,targetlabel,targetpk)
        tkey = "b." + str(targetpk) 
        ids = map(lambda d : d[tkey],graph.run(query).data())
        nodes = ClassNode.select(graph).where("_.%s IN  %s "%(str(targetpk),str(ids)))
        return nodes
     
    #########
    ## Related Taxonomic nodes inside the cell
    @property
    def has_kingdoms(self):
        return self._getAssociatedNodesPerTaxonLevel(Kingdom)
    
    @property
    def has_phyla(self):
        return self._getAssociatedNodesPerTaxonLevel(Phylum)
     
    @property
    def has_classes(self):
        return self._getAssociatedNodesPerTaxonLevel(Class_)
     
    @property
    def has_orders(self):
        return self._getAssociatedNodesPerTaxonLevel(Order)
 
    @property
    def has_families(self):
        return self._getAssociatedNodesPerTaxonLevel(Family)
     
    @property
    def has_genera(self):
        return self._getAssociatedNodesPerTaxonLevel(Genus)
     
    @property
    def has_species(self):
        return self._getAssociatedNodesPerTaxonLevel(Specie)
 
    @property
    def has_occurrences(self):
        return self._getAssociatedNodesPerTaxonLevel(Occurrence)    
        

    @property
    def gridname(self, *args, **kwargs):
        l = list(self.__ogm__.node.labels())
        name = reduce(lambda a,b : str(a) + '-' +str(b) ,l)
        return name
        
    def __repr__(self):
        c = "< %s id = %s >"%(self.gridname,str(self.id))
        return c
        

    @property
    def centroid(self):
        pointstr = 'POINT(%s %s)'%(self.longitude,self.latitude)
        point = GEOSGeometry(pointstr,srid=self.srid)
        return point
    
    @property
    def polygon(self):
        polygon = GEOSGeometry(self.cell,srid=self.srid)
        return polygon

    @property
    def polygon_shapely(self):
        from shapely import wkt
        polyg = wkt.loads(self.polygon.wkt)
        return polyg

    @property
    def upperCell(self):
        return iter(self.contained_in)
        
    def getNeighbours(self,with_center=False):
        """
        Returns the associated neighbours.
        parameters : 
            with_center : (Boolean) adds the given cell to the list of neighbours.
        """
        rn = [n for n in self.connected_to]
        if with_center:
            rn.append(self)
        return rn
       
    def occurrencesHere(self):
        """
        Filter the list of occurrences.
        """
        #occs = filter(lambda l : l.pk,self.Occurrences)
        occs = filter(lambda l : l.pk, self.has_occurrences)

        return occs        


    def getAssociatedRasterAreaData(self,string_selection,aggregated=True):
        """
        Returns the associated RasterData type for each cell where the occurrence happened.
        Returns a raster data type.
        Options:
               
            string_selection $in$ {'Elevation', 'MaxTemperature', 'MeanTemperature',
             'MinTemperature', 'Precipitation', 'Vapor' , 'SolarRadiation' ,
          'WindSpeed'        
        """
        
        raster_model = raster_models_dic[string_selection]
        polygon = self.polygon
        rasters =  RasterData(raster_model,polygon)
        #logger.debug("Retrieving information from layer: %s "%string_selection)
        rasters.getRaster()
        return rasters 

    def getEnvironmentalData(self,vars=['Elevation','MaxTemperature', 'MeanTemperature','MinTemperature','Precipitation','Vapor','SolarRadiation','WindSpeed'],with_std=False):
        """
        Returns summary statistics of each environmental layer defined as `vars`.

        
        Parameters :
            vars : list with the name of the available raster models.
            (Boolean flag) 
            with_std =  Returns the data with means and standard deviation
        
        THIS CAN BE PRIORS!!
        """
        df = {}
        for variable in vars:
            raster = self.getAssociatedRasterAreaData(variable)
            varname = raster.name
            try:
                statistics = raster.rasterdata.allBandStatistics()
            except:
                #import ipdb; ipdb.set_trace()
                statistics = {'mean':'N.A.','mean_std':'N.A'}
            mean_env = statistics['mean']
            df[varname + '_m'] = mean_env
            
            if with_std:
                std_env = statistics['mean_std']
                df[varname + '_std' ] = std_env
        return df

###########EXPERIMENTAL 

    def getRichnessOf(self,taxonomic_level_name):
        """
        Parameters :
            taxonomic_level_name : (String)
            The name of the type of nodes to calculate the richness.
            Options are:
                * kingdom
                * phylum
                * class
                * order
                * family
                * genus
                * species
                * occurrence
        """
        taxonomic_level_name = taxonomic_level_name.lower() 
        dic = {'kingdom' : self.has_kingdoms, 
                    'phylum' : self.has_phyla,
                    'class' : self.has_classes,
                    'order' : self.has_orders,
                    'family' : self.has_families,
                    'genus' :self.has_genera,
                    'species' : self.has_species,
                    'occurrence' : self.has_occurrences
               }

        selection = dic[taxonomic_level_name]
        query, param = selection._query_and_parameters
        newq = query.replace('RETURN _','RETURN Count(_)')
        dic = selection.graph.data(newq).pop() 
        n = dic['Count(_)'] 
        return n

class GridLevel1(Cell):
    __primarylabel__ ='mexico_grid1'

class GridLevel2(Cell):
    __primarylabel__ ='mexico_grid2'
    contained_in = RelatedTo("GridLevel1", ISCONTAINED)
   
class GridLevel3(Cell):
    __primarylabel__ ='mexico_grid4'
    contained_in = RelatedTo("GridLevel2", ISCONTAINED)
   
class GridLevel4(Cell):
    __primarylabel__ ='mexico_grid8'
    contained_in = RelatedTo("GridLevel3", ISCONTAINED)      

class GridLevel5(Cell):
    __primarylabel__ ='mexico_grid16'
    contained_in = RelatedTo("GridLevel4", ISCONTAINED)
   
class GridLevel6(Cell):
    __primarylabel__ ='mexico_grid32'
    contained_in = RelatedTo("GridLevel5", ISCONTAINED)
   
   
class GridLevel7(Cell):
    __primarylabel__='mexico_grid64'
    contained_in = RelatedTo("GridLevel6", ISCONTAINED)
   
   
class GridLevel8(Cell):
    __primarylabel__ ='mexico_grid128'
    contained_in = RelatedTo("GridLevel7", ISCONTAINED)
   
class GridLevel9(Cell):
    __primarylabel__ ='mexico_grid256'
    contained_in = RelatedTo("GridLevel8", ISCONTAINED)

class GridLevel10(Cell):
    __primarylabel__ = 'mexico_grid512'
    contained_in = RelatedTo("GridLevel9", ISCONTAINED)

class Mex4km(Cell):
    
    __primarykey__ = 'id'
    __primarylabel__ = 'mex4km'
    name = Property()
    longitude = Property()
    latitude = Property()
    cell = Property()
    id = Property()
       
    
    
    connected_to = RelatedTo("Mex4km", ISNEIGHBOUR)
    #contained_in = RelatedTo("Cell",ISCONTAINED)
    contained_in = RelatedTo("GridLevel10",ISCONTAINED)
    Occurrences = RelatedFrom(Occurrence, ISIN)
    
    #LocalTree  = RelatedFrom(TreeNode, ISIN)
    #Families = Related(Family,relationship_type=ISIN)
    #Families = RelatedFrom(Family,ISIN)
    #families = RelatedFrom("Family", "HAS_EVENT")    

#    @property
#    def centroid(self):
#        pointstr = 'POINT(%s %s)'%(self.longitude,self.latitude)
#        point = GEOSGeometry(pointstr)
#        return point
#    
#    @property
#    def polygon(self):
#        polygon = GEOSGeometry(self.cell)
#        return polygon
#
#



        
#     def occurrencesHere(self):
#         """
#         Filter the list of occurrences.
#         """
#         logger.debug("[Developer]: check that the Occurrences are the same that in the has_occurrences method")
#         #occs = filter(lambda l : l.pk,self.Occurrences)
#         occs = filter(lambda l : l.pk, self.has_occurrences)
#         return occs   




def pickNode(type='TreeNodeClass',name="str",graph=graph):
    """
    A wrapper for loading TreeNodes of the class 'type'.
    It uses the parameter name to look for a Node that satisfy the ~ string operator in py2neo.
    Parameters:
        type : A Class of Node taken from this module.
            e.g. Family
        name : A name in string. 
    Returns : 
        A TreeNode instance with data retrieved from the GraphDataBase.
        
    """
    #import ipdb; ipdb.set_trace()
    nameregexp = '\'' + name + '.*\''
    try:
        node = type.select(graph).where("_.name=~%s"%nameregexp)
    except:
        logger.error("type : %s argument is not a TreeNode valid Class" %type)
        return None
    #Check if it's empty
    
    nodeselector = list(node.limit(2))
    n = len(nodeselector)
    if n > 1 :
        return node
    elif n == 1:
        return nodeselector.pop()   
    
    else:
        logger.error("Name: \'%s\' was not found for TreeNode: %s"%(name,str(type)))
        return None
    

def countObjectsOf(NodeClass):
    """
    Returns the total number of objects of the class NodeClass.
    """
    try:
        cypher_str = "MATCH (n:%s) RETURN Count(n)"%NodeClass.__primarylabel__
        n = graph.data(cypher_str).pop()['Count(n)']
        return n

    except AttributeError:
        logger.error("Not a Node Object defined in the Graph Database")
        raise




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



