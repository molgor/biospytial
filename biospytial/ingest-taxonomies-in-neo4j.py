#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Script for ingesting all the taxonomies in a grid into Neo and with the corresponding RasterData nodes.
=======================================================================================================
..  

It is a complete guide for migrating the gridded taxonomy into neo4j with the corresponding  Raster Matching.


"""


__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2016, JEM"
__license__ = "GPL"
__version__ = "3.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"


from raster_api.aggregates import Union,Slope, Hillshade, SummaryStats
from raster_api.models import DemMexLow,DemMex

from django.contrib.gis.db.models.fields import RasterField
from raster_api.models import intersectWith
RasterField.register_lookup(intersectWith)

from django.contrib.gis.gdal import GDALRaster
from raster_api.aggregates import aggregates_dict
from raster_api.tools import RasterData
from raster_api.models import SolarRadiation
from raster_api.models import MeanTemperature
from matplotlib import pyplot as plt

from mesh.tools import migrateGridToNeo

import mesh.tools as mt
from gbif.taxonomy import Occurrence, Taxonomy, GriddedTaxonomy
from mesh.models import initMesh
# register the new lookup
RasterField.register_lookup(intersectWith)


from mesh.models import MexMesh

# Load data from a Country polygon 
from sketches.models import Country
mexico_border = Country.objects.filter(name__contains='exico').get()

import logging
logger = logging.getLogger('biospatial.raster_api.tools')

# Subselect the grid to match the region
mexgrid = MexMesh.objects.filter(cell__intersects=mexico_border.geom)
## Total without filtering: 279 277
## Total inside the boarder: 74 200
###Ya estuvo
#migrateGridToNeo(MexMesh,intersect_with=mexico_border.geom)
#migrateGridToNeo(mexgrid, create_unique_index=True, intersect_with='')

## Instantiate the biosphere
biosphere = Occurrence.objects.all()

#ggg = GriddedTaxonomy(biosphere,mexgrid.all(),generate_tree_now=False,use_id_as_name=False)

## Start the super analysis
from raster_api.models import raster_models
import multiprocessing

def doitall(list_of_taxonomies,rastermodels):
    n = len(list_of_taxonomies)
    for i,tax in enumerate(list_of_taxonomies):
        try:
            tax.ingestAllDataInNeo(rastermodels,with_raster=False)
        except:
            logger.error("Something occurred with taxonomy: %s"%i)
        logger.info("Processed: %s"%(float(i)/n))
        del(tax)
    return None





#mex = RasterData(MeanTemperature,mexico.geom)
#mex.getRaster(band=1)
#s = mex.rasterdata.allBandStatistics()



polystr = "POLYGON((-109 27,-106 27,-106 30,-109 30,-109 27))"




from django.contrib.gis.geos import GEOSGeometry
polygon = GEOSGeometry(polystr)
ggg = GriddedTaxonomy(biosphere,mexgrid.filter(cell__intersects=polystr),generate_tree_now=False,use_id_as_name=False)

#####
##
## Uncomment this if the grid hasn't been stored in the neo4j previously
#





