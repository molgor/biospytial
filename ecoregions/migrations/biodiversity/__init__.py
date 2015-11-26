#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Models for GBIF objects. 

"""

__author__ = "Juan Escamilla M—lgora"
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
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min


logger = logging.getLogger('biospatial.gbif')

def richness(taxonomy):
    """
    This is the richness diversity index.
    taxonomy is a data-structure type based on a geoqueryset object.
    Just counting different species.
    """
    inf = logger.info
    inf('Richness index selected')
    noc = taxonomy.occurrences.count()
    #inf('Number of occurrences in this biome: %s' %noc)
    nsp = taxonomy.species.count()
    #inf('Number of species in this biome: %s' %nsp)
    ngn = taxonomy.genera.count()
    #inf('Number of genera in this biome: %s' %ngn)   
    nfa = taxonomy.families.count()
    #inf('Number of families in this biome: %s' %nfa)
    nor = taxonomy.orders.count()
    #inf('Number of orders in this biome: %s' %nor)        
    ncl = taxonomy.classes.count()
    #inf('Number of classes in this biome: %s' %ncl)
    nph = taxonomy.phyla.count()
    #inf('Number of orders in this biome: %s' %nph)
    nki = taxonomy.kingdoms.count()
    #inf('Number of kingdoms in this biome %s' %nki)
    taxonomy.richness ={ 'occurrences' : noc,
           'species' : nsp,
        'genera' : ngn,
        'families': nfa,
        'classes' : ncl,
        'orders' : nor,
        'phyla' : nph,
        'kingdoms' : nki
        }
    
    return taxonomy.richness            