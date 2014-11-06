#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Models for GBIF objects. 

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2014, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



from django.test import TestCase
from django.conf import settings
import logging
from gbif.models import Occurrence, Specie
from django.db import models
from sketches.models import Sketch
import dateutil.parser
#from models import Count,Sum,Avg
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min
from gbif.models import Specie,Genus,Family,Order,Class,Phylum,Kingdom

logger = logging.getLogger('biospatial.gbif')
# Create your tests here.

sketches = Sketch.objects.all()


plgn = sketches[1].geom
# Grouping shit
#r = sp.objects.values('family').annotate(total=Count('scientific_name'))

biosphere = Occurrence.objects.all()

#newPoints=biome.values('kingdom').values('species_id').annotate(points=Collect('geom'))

biome = biosphere.filter(geom__intersects=plgn)

prueba1 = biosphere.raw('SELECT * from "tests.gbif_LB/Esp2"( (SELECT p.geom FROM (SELECT * from tests.sketches WHERE id =2) as p) );')


def aggregateTaxons(GBIF_QuerySet,taxonomic_level=1):
    """
    This function aggregates the GBIF objects according to the given taxonomic level.
    The taxonomic level is an integer which ranges from:
    Kingdom : 0
    Phylum : 1
    Order : 2
    Class : 3
    Family : 4
    Genus : 5
    Species : 6
    Default value is 6 [species]
    It return a list with the aggregated classes, the number of aggregated items per class and a Multipolygon geometry that comprises the aggregation.
    """
    levels = [{'kingdom':['kingdom_id','kingdom']},
              {'phylum' : ['phylum_id','phylum']},
              {'order' : ['order_id','_order']},
              {'class' : ['class_id','_class']},
              {'family' : ['family_id','family']},
              {'genus' : ['genus_id','genus']},
              {'species' : ['species_id','scientific_name']}
              ]
    try:
        selection = levels[taxonomic_level]
    except:
        logger.error("Chosen taxonomic level not existing %s. See documentation" %taxonomic_level)
        return False          
    level = selection.keys().pop()
    logger.debug('Aggregation level selected %s \n' %level)
    gqs = GBIF_QuerySet
    tax_id = selection[level][0]
    tax_featurename = selection[level][1]
    try: 
        taxons = gqs.values(tax_id).annotate(occurrences=Collect('geom'),num_occur=Count(tax_id),species_name=Min(tax_featurename))
    except:
        logger.error("Bad request on GBIF_QuerySet. Either is not a QuerySet object from Occurrence Class or there is something wrong. Check code.")
        return False
    return taxons

species = biome.values('species_id').annotate(occurrences=Collect('geom'),num_occur=Count('species_id'),species_name=Min('scientific_name'))
#orders = families.values('order_id').annotate(Collect('geom'),num_fams=Count('order_id'),order_name=Min('_order'))
#classes = orders.values('class_id').annotate(Collect('geom'),num_orders=Count('class_id'),class_name=Min('_class'))
#phylums = classes.values('phylum_id').annotate(Collect('geom'),num_class=Count('phylum_id'),phylum_name=Min('phylum'))
#kingdoms = phylums.values('kingdom_id').annotate(Collect('geom'),num_phylums=Count('kingdom_id'),kingdom_name=Min('kingdom'))



families = species.values('family_id').annotate(points=Collect('geom'),ab=Count('family_id'),name=Min('family'))

genuses = biome.values('genus_id').annotate(points=Collect('geom'),ab=Count('genus_id'),name=Min('genus'))
reinos=kingdoms = biome.values('kingdom_id').values('phylum_id').values('order_id').values('class_id').values('family_id').values('genus_id').values('species_id').annotate(Collect('geom'),num_phylums=Count('kingdom_id'),kingdom_name=Min('kingdom'))

species = biome.values('species_id').annotate(points=Collect('geom'),ab=Count('species_id'),name=Min('scientific_name'))

classes = biome.values('class_id').annotate(points=Collect('geom'),ab=Count('class_id'),name=Min('_class'))

orders = biome.values('order_id').annotate(points=Collect('geom'),ab=Count('order_id'),name=Min('_order'))

phylums = biome.values('phylum_id').annotate(points=Collect('geom'),ab=Count('phylum_id'),name=Min('phylum'))

kingdoms = biome.values('kingdom_id').annotate(points=Collect('geom'),ab=Count('kingdom_id'),name=Min('kingdom'))


r=species[0]
s=Specie(biome,r)

#genus = map(lambda g : Genus(biome,g),genuses[1:10])

#fams = map(lambda f : Family(biome,f),families[1:10])

#classex = map(lambda c: Class(biome,c),classes[1:6])
#phyls = map(lambda p: Phylum(biome,p),phylums[1:2])
kings = map(lambda k : Kingdom(biome,k),kingdoms[1:2])
#orderes = map(lambda o: Order(biome,o),orders[1:10])


