#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Scripts for testing and playing around with the Taxonomy tree read from neo.
"""

#from drivers.neo4j_reader import TreeNeo, LocalTree


from drivers.tree_builder import TreeNeo

from mesh.models import MexMesh
from gbif.taxonomy import Occurrence, Taxonomy, GriddedTaxonomy
#from drivers.neo4j_reader import Cell,extractOccurrencesFromTaxonomies

from drivers.graph_models import Cell
from drivers.tree_builder import extractOccurrencesFromTaxonomies

from py2neo import Graph
import pandas as pd
import matplotlib.pyplot as plt



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

#from drivers.neo4j_reader import RasterCollection
from drivers.raster_node_builder import RasterCollection
#ts = ggg.taxonomies[0:150]


## Remember t needs to be a list of taxonomies

occurs,g0 = extractOccurrencesFromTaxonomies(t)

occurs1,g1 = extractOccurrencesFromTaxonomies(t1)

occurs2,g2 = extractOccurrencesFromTaxonomies(t2)


complete = TreeNeo(occurs)

part1 = TreeNeo(occurs1)
part2 = TreeNeo(occurs2)

plants2 = part2.to_Plantae

plants1 = part1.to_Plantae
  
arthropods = complete.children[0].children[1]
birds = complete.classes[2]


ggg.taxonomies.sort(key=lambda l : len(l.occurrences),reverse=True)

t = ggg.taxonomies[300]
ocs , cell = extractOccurrencesFromTaxonomies([t])

t = TreeNeo(ocs,cell)

#ocs = map(lambda l : extractOccurrencesFromTaxonomies([l]), ggg.taxonomies)

#trees = map(lambda o : TreeNeo(o[0],o[1]),ocs)

flowers = t.to_Plantae.to_Magnoliophyta.to_Magnoliopsida
n = t.getNeighboringTrees(filter_central_cell=True) 
n.expandNeighbourhood(size=7)  
y = map(lambda t : int(t.hasNode(flowers)),n.neighbours)
Y = pandas.DataFrame({'Y':y})

X = n.getEnvironmentalData()  
Z = n.getCooccurrenceMatrix(3) 

## build of data set
data = pandas.concat((Y,X,Z),axis=1)

#md = smf.mixedlm("Y ~ MeanTemperature_mean + Precipitation_mean",data,groups=data["Mammalia"])


#New things !
import matplotlib.pyplot as plt
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from raster_api import tools as tls
from raster_api.models import MeanTemperature
from raster_api import models as rm



# REmove null cells:
#ocs_free = filter(lambda l : l, ocs)


#trees_f = map(lambda l : TreeNeo(l),ocs_free)



#trees_f = TreeNeo(extractOccurrencesFromTaxonomies([ggg.taxonomies[3400]]))

#central = trees_f


#trees = T.getNeighboringTrees()







#art1 = part1.children[0].children[1]
#art2 = part2.children[0].children[1]

#birds = complete.classes[2]



#rd = RasterCollection(arthropods)

