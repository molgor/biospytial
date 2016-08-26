#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Scripts for testing and playing around with the Taxonomy tree read from neo.
"""

from drivers.neo4j_reader import TreeNeo
from mesh.models import MexMesh
from gbif.taxonomy import Occurrence, Taxonomy, GriddedTaxonomy
from drivers.neo4j_reader import TaxonomicLevel
from drivers.neo4j_reader import Cell
from py2neo import Graph
# Load data from a Country polygon 
#from sketches.models import Country
#mexico_border = Country.objects.filter(name__contains='exico').get()

import logging
logger = logging.getLogger('biospatial.raster_api.tools')

g = Graph()


from django.contrib.gis.geos import GEOSGeometry
polystr = "POLYGON((-109 27,-106 27,-106 30,-109 30,-109 27))"
polygon = GEOSGeometry(polystr)



# Subselect the grid to match the region
#mexgrid = MexMesh.objects.filter(cell__intersects=mexico_border.geom)
mexgrid = MexMesh.objects.filter(cell__intersects=polygon)


## Instantiate the biosphere
biosphere = Occurrence.objects.all()

subbiosphere = biosphere.filter(geom__intersects=polygon)

ggg = GriddedTaxonomy(subbiosphere,mexgrid.filter(cell__intersects=polystr),generate_tree_now=False,use_id_as_name=False)

ts = ggg.taxonomies[0:150]


#ts = ggg.taxonomies[0:150]


yea = TreeNeo()
  

# put list of taxonomies 

yea.setOccurrencesFromTaxonomies(ts)  


yea.refreshNodes()

#sp = TaxonomicLevel(yea.nodes,selected_level=999)
#lll = sp.getNodeCells(12)
#c = lll[0]
#rrr = Cell.select(g,c['id']).first()

#Maybe load all taonomies and measure the time.

## 