#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Scripts for testing and playing around with the Taxonomy tree read from neo.
"""

from drivers.neo4j_reader import TreeNeo
from mesh.models import MexMesh
from gbif.taxonomy import Occurrence, Taxonomy, GriddedTaxonomy
from drivers.neo4j_reader import Cell,extractOccurrencesFromTaxonomies
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

t = ggg.taxonomies[0:150]

t1 = ggg.taxonomies[0:75]

t2 = ggg.taxonomies[75:150]

import pandas

from drivers.neo4j_reader import RasterCollection
#ts = ggg.taxonomies[0:150]


## Remember t needs to be a list of taxonomies

occurs = extractOccurrencesFromTaxonomies(t)

occurs1 = extractOccurrencesFromTaxonomies(t1)

occurs2 = extractOccurrencesFromTaxonomies(t2)


complete = TreeNeo(occurs)

part1 = TreeNeo(occurs1)
part2 = TreeNeo(occurs2)

plants2 = part2.to_Plantae

plants1 = part1.to_Plantae
  
arthropods = complete.children[0].children[1]
birds = complete.classes[2]


ggg.taxonomies.sort(key=lambda l : len(l.occurrences))
map(lambda l : len(l.occurrences),ggg.taxonomies)
chiqui = map(lambda l : len(l.occurrences),ggg.taxonomies)


alta_biodiv = ggg.taxonomies[3800:]

t = alta_biodiv[0]

T = TreeNeo(extractOccurrencesFromTaxonomies([t]))

trees = T.getNeighboringTrees()

neighbour_tree = reduce(lambda a,b : a + b , trees)

o = neighbour_tree.occurrences[0]





#art1 = part1.children[0].children[1]
#art2 = part2.children[0].children[1]

#birds = complete.classes[2]



#rd = RasterCollection(arthropods)

