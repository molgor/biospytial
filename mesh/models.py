#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Mesh / Grid module
===========
This module defines the classes and functions of mesh (grid) objects.
Models for mesh objects. 

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "0.0.8"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



from django.contrib.gis.db import models
from django.contrib.gis.geos import Point,Polygon
from django.db import utils
import logging
from django.test import TestCase
from django.conf import settings
import dateutil.parser
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min
from py2neo import Node, Relationship, Graph
from django.forms import ModelForm
from biospytial import settings


neoparams = settings.NEO4J_DATABASES['default']
uri = "http://%(HOST)s:%(PORT)s%(ENDPOINT)s" % neoparams
graph = Graph(uri)
scales = settings.MESH_TABLENAMESPACE
logger = logging.getLogger('biospytial.mesh')






    

# The abstract class
class mesh(models.Model):
    """
    .. mesh:
    A Mesh or Grid is a regular two dimensional geometric object
    conformed by a regular tessellation of equal area square tiles.
    
    Let A be a connected and bounded set in a Surface E.
    A tessellation T on A is a set of polygons Pi such that:
    
        * Pi is contained in A for all i
        * Union(Pi) covers A
        * Pi intersects Pj is empty for if i is not equal to j.
    
    This is the standard mesh model that defines a grid.
    ..
    
    Attributes
    ==========
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    id = models.AutoField(primary_key=True, db_column="gid")
    #row = models.IntegerField()
    #col = models.IntegerField()
    cell = models.PolygonField()
    objects = models.GeoManager()
    
    class Meta:
        managed = False
        # Experiment
        abstract =  True
        #db_table = 'mesh\".\"braz_grid2048a'

    def getScaleLevel(self):
        """
        ..
        Gives the current level name
        ..
        
        Returns
        =======
        
        tablename : string
            The table name of the current grid. As stored in the database.
            
        """
        #inv_map = {v: k for k, v in self.scales.items()}
        sc = self._meta.db_table
        self.tablename = sc
        return sc
      
    def __repr__(self):
        """
        String representation of the object 
        """
        a = "<Cell id: %s --%s />" %(self.id,self.cell)
        return a
    
    
    def describeWithDict(self):
        """
        Returns a dictionary with the properties
        """
        latitude = self.cell.centroid.y
        longitude = self.cell.centroid.x
        id = int(self.id)
        indexillo = "%s-%s:%s" %(str(id),str(longitude),str(latitude))
        tablename = self.getScaleLevel()
        indexillo = "%s:%s" %(str(tablename),str(id))
        d = {"id":id , "cell":self.cell.wkt, "latitude":latitude, "longitude":longitude ,"uniqueid":indexillo}
        return d
    
    
    def getNode(self,writeDB=False):
        """
        Returns a Node data structure that can be put into Neo4j
        """
        
        properties = self.describeWithDict()
        scalename = self.getScaleLevel().split(".").pop().replace("\"","")
        properties['name'] = str(self.id)
        n0 = Node("Cell",scalename,**properties)
        #old_node = graph.find_one("Cell",property_key="uniqueid",property_value=properties['uniqueid'])
        old_node = graph.find_one(scalename,property_key="uniqueid",property_value=properties['uniqueid'])
        if old_node:
            return old_node
        else:
            if writeDB:
                graph.create(n0)
            return n0


# Experiment, using abstract tables
    ## Use the settings.MESH_TABLENAMESPACE as reference.
## If needed. Insert here new Class definitions for new meshes (different scales or geographical extend)

## These are concrete classes / table for a certain scale.


class Mesh1(mesh):  
    class Meta:
        managed = False
        # Experiment
        db_table = settings.MESH_TABLENAMESPACE[1]
        

class Mesh2(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[2]

class Mesh3(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[3]
       
class Mesh4(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[4]

class Mesh5(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[5]
        
class Mesh6(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[6]
        
class Mesh7(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[7]                

class Mesh8(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[8]
        
class Mesh9(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[9]
        
class Mesh10(mesh):
    class Meta:
        managed = False
        db_table = settings.MESH_TABLENAMESPACE[10]                 
        
        
def getNeighboursOf(cell,mesh):
    # old version ns = mesh.objects.filter(cell__touches=cell.cell)
    vonNeuman = mesh.objects.filter(cell__touches=cell.cell).filter(cell__overlaps_above=cell.cell).filter(cell__overlaps_below=cell.cell) | mesh.objects.filter(cell__touches=cell.cell).filter(cell__overlaps_left=cell.cell).filter(cell__overlaps_right=cell.cell)
    
    
    return vonNeuman


def bindNeighboursOf(cell,mesh,writeDB=False):
    node_c = cell.getNode(writeDB=writeDB)
    ns = getNeighboursOf(cell, mesh)
    
    nodes = map(lambda n: n.getNode(writeDB=writeDB),ns)
    rels = [Relationship(node_c,"IS_NEIGHBOUR_OF",n) for n in nodes]
    if writeDB:
        created = [graph.create(rel) for rel in rels]
    return rels



def initMesh(Intlevel,scales=scales):
    """
    This function initializes a mesh based on the table definition (name) 
    of a spatially enabled database.
    
    .. note::
   
       The current list for the working mesh names are:
        
        * 8 : 'mesh\".\"braz_grid8a',
        * 9 : 'mesh\".\"braz_grid16a',
        * 10 : 'mesh\".\"braz_grid32a',
        * 11 : 'mesh\".\"braz_grid64a',
        * 12 : 'mesh\".\"braz_grid128a',
        * 13 : 'mesh\".\"braz_grid256a',
        * 14 : 'mesh\".\"braz_grid512a',
        * 15 : 'mesh\".\"braz_grid1024a',
        * 16 : 'mesh\".\"braz_grid2048a',
        * 17 : 'mesh\".\"braz_grid4096a'

    MEX_SCALES = { 
        * 0 : 'mesh"."mexico_grid1',
        * 1: 'mesh"."mexico_grid2',
        * 2: 'mesh"."mexico_grid4',
        * 3: 'mesh"."mexico_grid8',
        * 4: 'mesh"."mexico_grid16',
        * 5: 'mesh"."mexico_grid32',
        * 6: 'mesh"."mexico_grid64',
        * 7: 'mesh"."mexico_grid128',
        * 8: 'mesh"."mexico_grid256',
        * 9: 'mesh"."mexico_grid512',
        * 10: 'mesh"."mexico_grid1024'
         }



    Parameters
    ==========
        IntLevel : int
            The id value of the gridded table to use
            
        scales : dictionary with strings
            The dictionary that maps the grids table names with the levels.
    
    
    Returns
    =======
     m : mesh.Mesh
        An instance of Mesh with the specified resolution (level)
    """

#     import copy
# 
#     m = copy.deepcopy(mesh)
#     try:
#         m._meta.db_table = scales[Intlevel]
#         logger.info('[biospytial.mesh] table name %s' %m._meta.db_table)
#         return m
#     except:
#         logger.error("[biospytial.mesh] Selected zoom level not implemented yet")
#         return False

    i = Intlevel
    if i == 1:
        return Mesh1
    elif (i == 2):
        return Mesh2
    elif (i == 3):
        return Mesh3
    elif (i == 4):
        return Mesh4
    elif (i == 5):
        return Mesh5
    elif (i == 6):
        return Mesh6
    elif (i == 7):
        return Mesh7
    elif (i == 8):
        return Mesh8
    elif (i == 9):
        return Mesh9
    elif (i == 10):
        return MexMesh

    
    
    
    

# def getNeighbours(cell_center,mesh):
#     neighbours = mesh.objects.filter(cell__touches=cell_center.cell)
#     
#     return (cell_center,neighbours)
# 
# 
# 
# def createNetworkOnNode(duple_center_neighbour,writeInDB=False):
#     center = duple_center_neighbour[0]
#     neighbours = duple_center_neighbour[1]
#     n0 = Node("Cell",**center.describeWithDict())
#     nn = [ Relationship(n0,"IS_NEIGHBOUR_OF",Node("Cell", **n.describeWithDict())) for n in neighbours]
#     if writeInDB:
#         for relationship in nn:
#             g.create(relationship)
#     return nn



    

    
    
class NestedMesh:
    """
    .. NestedMesh:
    
    A nested mesh is a hierarchical data structure composed of ordered levels.
    Each level is an instance of a mesh such that for levels li, lj (i < j)
    All levels are defined on the same geographical area.
    The number of cells from level_j is 4**n times bigger than the number of cells in
    level_i, (where n is j - i ).
    
    The resolution is inversely proportional to the size
    
    .. note:: 
        For more information see the grid generation function under the SQL-functions
    folder.
    
    This is the class that defines this geometric data type.
    
    Parameters
    ==========
    id : int
        identification value for the nested grid object
    start_level : int
        The idkey of the parent mesh (top layer)
        See: initMesh()
    end_level : int
        The idkey for the bottom mesh layer of the nested grid.
    
    
    """
    def __init__(self,id,start_level=10,end_level=11):
        """
        I'm the constructor: start_level = (Integer) level of aggregation.
        end_level :: bottom of the nesting grid.
        id = id value of the cell in the starting grid.
        """
        self.levels = {}
        self.table_names = {}
        m1 = initMesh(start_level)
        #Filter with appropiate id
        try:
            cell1 = m1.objects.get(id=id)
        except:
            logger.error("[biospytial.mesh] Selected id does not exist in selected grid")
            return None
        self.levels[start_level] = cell1
        self.table_names[start_level] = m1._meta.db_table
        for level in range(start_level+1,end_level+1):
            m_temp = initMesh(level)
            #within functions perfectly in this situation
            cells=m_temp.objects.filter(cell__within=cell1.cell)
            self.levels[level]=cells
            self.table_names[level] = m_temp._meta.db_table
            del(m_temp)
            
        
        

class MexMesh(models.Model):
    """
    .. mesh:
    A Mesh or Grid is a regular two dimensional geometric object
    conformed by a regular tessellation of equal area square tiles.
    THIS IS FOR THE 4 KM Mexican GRID
    Let A be a connected and bounded set in a Surface E.
    A tessellation T on A is a set of polygons Pi such that:
    
        * Pi is contained in A for all i
        * Union(Pi) covers A
        * Pi intersects Pj is empty for if i is not equal to j.
    
    This is the standard mesh model that defines a grid.
    ..
    
    Attributes
    ==========
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    
    id = models.AutoField(primary_key=True, db_column="gid")
    gid = models.IntegerField(db_column="id")
    xmin = models.FloatField(db_column="__xmin")
    xmax = models.FloatField(db_column="__xmax")
    ymin = models.FloatField()
    ymax = models.FloatField()    
    #row = models.IntegerField()
    #col = models.IntegerField()
    cell = models.MultiPolygonField(db_column = "geom")
    objects = models.GeoManager()
    
    class Meta:
        managed = False
        db_table = 'mesh"."mex4km'

    def getScaleLevel(self):
        """
        ..
        Gives the current level name
        ..
        
        Returns
        =======
        
        tablename : string
            The table name of the current grid. As stored in the database.
            
        """
        #inv_map = {v: k for k, v in self.scales.items()}
        sc = self._meta.db_table
        self.tablename = sc
        return sc
      
    def __repr__(self):
        """
        String representation of the object 
        """
        a = "<Cell id: %s --%s />" %(self.id,self.cell)
        return a
    
    
    def describeWithDict(self):
        """
        Returns a dictionary with the properties
        """
        latitude = self.cell.centroid.y
        longitude = self.cell.centroid.x
        id = int(self.id)
        indexillo = "%s-%s:%s" %(str(id),str(longitude),str(latitude))
        
        d = {"id":id , "cell":self.cell.wkt, "latitude":latitude, "longitude":longitude ,"uniqueid":indexillo}
        return d
    
    
    def getNode(self,writeDB=False):
        """
        Returns a Node data structure that can be put into Neo4j
        """
        
        properties = self.describeWithDict()
        properties['name'] = str(self.id)
        scalename = self.getScaleLevel().split(".").pop().replace("\"","")
        n0 = Node("Cell",scalename,**properties)
        #old_node = graph.find_one("Cell",property_key="uniqueid",property_value=properties['uniqueid'])        
        old_node = graph.find_one(scalename,property_key="uniqueid",property_value=properties['uniqueid'])
        if old_node:
            return old_node
        else:
            if writeDB:
                graph.create(n0)
            return n0
        
# class grid(models.Model):
#     """
#     .. mesh:
#     A Mesh or Grid is a regular two dimensional geometric object
#     conformed by a regular tessellation of equal area square tiles.
#     
#     Let A be a connected and bounded set in a Surface E.
#     A tessellation T on A is a set of polygons Pi such that:
#     
#         * Pi is contained in A for all i
#         * Union(Pi) covers A
#         * Pi intersects Pj is empty for if i is not equal to j.
#     
#     This is the standard mesh model that defines a grid.
#     ..
#     
#     Attributes
#     ==========
#     id : int Unique primary key
#         This is the identification number of each element in the mesh.
#     
#     """
#     id = models.AutoField(primary_key=True, db_column="gid")
#     row = models.IntegerField()
#     col = models.IntegerField()
#     cell = models.PolygonField()
#     objects = models.GeoManager()
#     
#     class Meta:
#         managed = False
#         db_table = 'grid025mex'
# 
#     def getScaleLevel(self):
#         """
#         ..
#         Gives the current level name
#         ..
#         
#         Returns
#         =======
#         
#         tablename : string
#             The table name of the current grid. As stored in the database.
#             
#         """
#         #inv_map = {v: k for k, v in self.scales.items()}
#         sc = self._meta.db_table
#         self.tablename = sc
#         return sc
#       
#     def __repr__(self):
#         """
#         String representation of the object 
#         """
#         a = "<Cell id: %s --%s />" %(self.id,self.cell)
#         return a
        