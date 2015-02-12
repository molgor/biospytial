#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Models for mesh objects. 

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
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


logger = logging.getLogger('biospatial.mesh')


from django.forms import ModelForm



def initMesh(Intlevel):
    import copy
    scales = { 8 : 'mesh\".\"braz_grid8a',
              9 : 'mesh\".\"braz_grid16a',
              10 : 'mesh\".\"braz_grid32a',
              11 : 'mesh\".\"braz_grid64a',
              12 : 'mesh\".\"braz_grid128a',
              13 : 'mesh\".\"braz_grid256a',
              14 : 'mesh\".\"braz_grid512a',
              15 : 'mesh\".\"braz_grid1024a',
              16 : 'mesh\".\"braz_grid20148a',
              17 : 'mesh\".\"braz_grid4096a'
              }
    m = copy.deepcopy(mesh)
    try:
        m._meta.db_table = scales[Intlevel]
        logger.info('[biospatial.mesh] table name %s' %m._meta.db_table)
        return m
    except:
        logger.error("[biospatial.mesh] Selected zoom level not implemented yet")
        return False

class mesh(models.Model):
    id = models.AutoField(primary_key=True, db_column="gid")
    cell = models.PolygonField()
    objects = models.GeoManager()
    
    class Meta:
        managed = False
        db_table = 'mesh\".\"braz_grid2048a'

    def getScaleLevel(self):
        """
        Gives the current level 
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
    
    
class NestedMesh:
    """
    Class that defines a geometrical datatype with nested grid cells. 
    """
    def __init__(self,id,start_level=10,end_level=11):
        """
        I'm the constructor: start_level = (Integer) level of aggregation.
        end_level :: bottom of the nesting grid.
        id = id value of the cel in the starting grid.
        """
        self.levels = {}
        self.table_names = {}
        m1 = initMesh(start_level)
        #Filter with appropiate id
        try:
            cell1 = m1.objects.get(id=id)
        except:
            logger.error("[biospatial.mesh] Selected id does not exist in selected grid")
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
            
        
        
        
        
        
        
        