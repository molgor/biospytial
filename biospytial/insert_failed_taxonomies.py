from error_index_extractor import *

from gbif.models import Occurrence
from sketches.models import Country
from mesh.models import initMesh
from gbif.taxonomy import GriddedTaxonomy
from raster_api.models import raster_models
import django.db as db
import logging
biosphere = Occurrence.objects.all()
mexico_border = Country.objects.filter(name__contains='exico').get()
mexbiosphere = biosphere.filter(geom__intersects=mexico_border.geom)


logger = logging.getLogger('biospytial.insert_taxonomies_worker_errors')


## Select one cell of one thing
m11 = initMesh(11)
mexmesh = m11.objects.filter(cell__intersects=mexico_border.geom)



W1_FILE = open("logs/w1.log",'r')
W2_FILE = open("logs/w2.log",'r')
#W3_FILE = open("logs/w3.log",'r')


w1_list = W1_FILE.readlines()
w2_list = W2_FILE.readlines()
#w3_list = W3_FILE.readlines()
W1_FILE.close()
W2_FILE.close()


w1 = cleandata(w1_list)
w2 = cleandata(w2_list)
dd1 = prepare1(w1)
dd2 = prepare1(w2)            
t1 = Only(extractIdx(dd1))
t2 = Only(extractIdx(dd2))

errors = t1 + t2


getCell = lambda errid : mexmesh.get(pk=errid)

subsetmexmesh = map(getCell,errors)
mexmesherrors= mexmesh.filter(pk__in=errors)

#ggg = GriddedTaxonomy(biosphere,mexmesherrors,"mex4km")
#taxonomy.ingestAllDataInNeo(raster_models,with_raster=True)





def insertFULLTaxonomiesInNeo4J(mesh_subset,biosphere,gridname,num_proc=4):
    logger.info("Initialising mesh subset %s"%num_proc)
    ggg = GriddedTaxonomy(biosphere,mesh_subset,gridname)
    N =len(ggg.taxonomies)
    for i,taxonomy in enumerate(ggg.taxonomies):
        try :
            taxonomy.ingestAllDataInNeo(raster_models,with_raster=True)
        except db.OperationalError:
            logger.error("Disconnected worker %s from database! Taxonomy %s problem %s Attempting to reconnect... engage!" %(num_proc,taxonomy.gid,i))
            db.connections.close_all()
            continue
        perc = i / float(N) * 100    
        logger.info("[PROCESS: %s ] Taxonomy %s inserted. %s / N. Completed: %s"%(num_proc,taxonomy.gid,i,perc))
             
    return ggg

#ggg = insertFULLTaxonomiesInNeo4J(mexmesherrors,biosphere,"mex4km",num_proc=4)
