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
from gbif.models import Occurrence, Especies
from django.db import models
from sketches.models import Sketch
import dateutil.parser
#from models import Count,Sum,Avg
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min


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


species = biome.values('species_id').annotate(Collect('geom'),num_occur=Count('species_id'),species_name=Min('scientific_name'))
families = species.values('family_id').annotate(Collect('geom'),num_esp=Count('family_id'),family_name=Min('family'))
orders = families.values('order_id').annotate(Collect('geom'),num_fams=Count('order_id'),order_name=Min('_order'))
classes = orders.values('class_id').annotate(Collect('geom'),num_orders=Count('class_id'),class_name=Min('_class'))
phylums = classes.values('phylum_id').annotate(Collect('geom'),num_class=Count('phylum_id'),phylum_name=Min('phylum'))
kingdoms = phylums.values('kingdom_id').annotate(Collect('geom'),num_phylums=Count('kingdom_id'),kingdom_name=Min('kingdom'))






