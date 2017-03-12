from gbif.taxonomy import GriddedTaxonomy
from gbif.models import Occurrence
from mesh.models import initMesh
from mesh.models import MexMesh
from mesh.tools import migrateGridToNeo
import logging
import numpy
from raster_api.models import raster_models
import django.db as db


logger = logging.getLogger('biospytial.insert_taxonomies_worker1')

#m1 = initMesh(7)
#m1
#m1.objects.all()
biosphere = Occurrence.objects.all()


from sketches.models import Country
mexico_border = Country.objects.filter(name__contains='exico').get()
mexbiosphere = biosphere.filter(geom__intersects=mexico_border.geom)

## Select one cell of one thing


m10 = initMesh(10)
#g = GriddedTaxonomy(biosphere,center)

mexmesh = m10.objects.filter(cell__intersects=mexico_border.geom)
####
## This part is for partitioning the data.
## First let's take the ids
vs = numpy.array(mexmesh.values_list('id'))
## I'll use the median . If you want more partici'on use quantiles

middle_index =  int(numpy.median(vs)) 

#e.g. Im going to do 3 partitions
first_indx = int(numpy.percentile(vs,33))
second_indx = int(numpy.percentile(vs,66))
last_indx = int(numpy.max(vs))

mexmesh1 = mexmesh.filter(id__lte=first_indx)

mexmesh2 = mexmesh.filter(id__gt=first_indx).filter(id__lte=second_indx)

mexmesh3 = mexmesh.filter(id__gt=second_indx).filter(id__lte=last_indx)

## Load all the cells in the memory (This is for preventing an exploition of queries to the server)
#logger.info("Loading selected cells in memory. This can take some time")
#cells = list(mexmesh)
#logger.debug("%s cells loaded"%len(cells))
#ggg = GriddedTaxonomy(biosphere,mexmesh1,"mex4km")





def insertFULLTaxonomiesInNeo4J(mesh_subset,biosphere,gridname,num_proc=1):
    logger.info("Initialising mesh subset %s"%num_proc)
    ggg = GriddedTaxonomy(biosphere,mesh_subset,gridname)
    N =len(ggg.taxonomies)
    for i,taxonomy in enumerate(ggg.taxonomies):
        try OperationalError:
            taxonomy.ingestAllDataInNeo(raster_models,with_raster=True)
        except:
            logger.error("Disconnected worker %s from database! Attempting to reconnect... engage!" %num_proc)
            db.connections.close_all()
            continue
        perc = i / float(N) * 100    
        logger.info("[PROCESS: %s ] Taxonomy %s inserted. %s / N. Completed: %s"%(num_proc,taxonomy.gid,i,perc))
            
    return ggg


ggg = insertFULLTaxonomiesInNeo4J(mexmesh1,biosphere,"mex4km",num_proc=1)
#








