#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Models for sketches objects. 

"""

__author__ = "Juan Escamilla M�lgora"
__copyright__ = "Copyright 2014, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db import utils
import logging
from django.test import TestCase
from django.conf import settings
import dateutil.parser





class Sketch(models.Model):
    """
    This is the model for making sketches and play.
    """
    id = models.AutoField(primary_key=True)
    description = models.CharField(db_index=True, max_length=50,blank=True, null=True)   
    geom = models.PolygonField()
    #modified = spystats.DateTimeField(db_index=True,blank=True, null=True)
    objects = models.GeoManager()
    
    class Meta:
        managed = False
        db_table = 'tests\".\"sketches'
 
    def __unicode__(self):
        return u'<Sketch: %s >' %(self.id)

class Country(models.Model):
    """
    This is the model for making objects based on the polugons defined by the table world boarders
    """
    id =  models.AutoField(primary_key=True, db_column="gid")
    fips = models.CharField(max_length=2)
    iso2 = models.CharField(max_length=2) 
    iso3 = models.CharField(max_length=3)
    un = models.IntegerField()
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField()
    region = models.IntegerField()
    subregion = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    geom =  models.MultiPolygonField()
    objects = models.GeoManager()
    class Meta:
        managed = False
        db_table = 'public\".\"world_borders'
        
    def __unicode__(self):
        return u'<Country instance: %s >'%(self.name)

# This is an auto-generated Django model module created by ogrinspect.

from django.contrib.gis.db import models

class MexRoads(models.Model): 
    id =  models.AutoField(primary_key=True, db_column="gid")
    fnode_field = models.BigIntegerField(db_column="fnode_") 
    tnode_field = models.BigIntegerField(db_column="tnode_") 
    lpoly_field = models.BigIntegerField(db_column="lpoly_") 
    rpoly_field = models.BigIntegerField(db_column="rpoly_") 
    length = models.FloatField() 
    cov_field = models.BigIntegerField(db_column="cov_") 
    cov_id = models.BigIntegerField() 
    geom = models.MultiLineStringField(srid=4326)
    
    class Meta:
        managed = False
        db_table = 'public\".\"mexroads'
        
    def __unicode__(self):
        return u'<Road Layer instance: %s >'%(self.lpoly_field)
# Auto-generated `LayerMapping` dictionary for MexRoads model

mexroads_mapping = { 'fnode_field' : 'FNODE_',
'tnode_field' : 'TNODE_', 
'lpoly_field' : 'LPOLY_', 
'rpoly_field' : 'RPOLY_', 
'length' : 'LENGTH', 
'cov_field' : 'COV_', 
'cov_id' : 'COV_ID',
'geom' : 'MULTILINESTRING', }


# Create your spystats here.
