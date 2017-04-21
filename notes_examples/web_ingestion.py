## This script shows how to insert data using the WEB API.
## Have fun!


from drivers import populate
from django.contrib.gis.geos import GEOSGeometry
from gbif.models import Occurrence
from gbif.taxonomy import GriddedTaxonomy

from mesh.models import initMesh
import logging

logger = logging.getLogger('biospytial.gbif.taxonomy')


squarestr = "POLYGON ((-2.8975 54.1165, -2.8975 54.2415, -2.7725 54.2415, -2.7725 54.1165, -2.8975 54.1165))"

square1 = GEOSGeometry(squarestr)

m10 = initMesh(10)

# For make it more efficient we need a coarser resolution


m7 = initMesh(7)


cells = m10.objects.filter(cell__intersects=square1)

bcells = m7.objects.filter(cell__intersects=square1) 


## Let's make a quick example here for getting data/
#data  = map(lambda cell : populate.getAllOccurrences(cell.cell.wkt,safeinDB=True,maxdepth=700),cells)



## For inserting in NEo , onece the grid is stored there

square1 = "POLYGON((-2.89749999999999996 54.11650000000000205,-2.89749999999999996 54.24150000000000205,-2.77249999999999996 54.24150000000000205,-2.77249999999999996 54.11650000000000205,-2.89749999999999996 54.11650000000000205))"
from django.contrib.gis.geos import GEOSGeometry
polygon = GEOSGeometry(square1)

biosphere = Occurrence.objects.filter(geom__within=polygon)

from mesh.models import initMesh
m10 = initMesh(10)
m10_sub = m10.objects.filter(cell__intersects=polygon)



from raster_api.models import raster_models
import multiprocessing

def doitall(list_of_taxonomies,rastermodels):
    n = len(list_of_taxonomies)
    for i,tax in enumerate(list_of_taxonomies):
        try:
            tax.ingestAllDataInNeo(rastermodels,with_raster=True)
        except:
            logger.error("Something occurred with taxonomy: %s"%i)
        logger.info("Processed: %s"%(float(i)/n))
        del(tax)
    return None

#ggg = GriddedTaxonomy(biosphere,m10_sub,"carnforth512")
