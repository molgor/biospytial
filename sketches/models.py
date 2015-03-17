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
    #modified = models.DateTimeField(db_index=True,blank=True, null=True)
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


# Create your models here.