from gbif.taxonomy import GriddedTaxonomy
from gbif.models import Occurrence
from mesh.models import initMesh
from mesh.models import MexMesh
from mesh.tools import migrateGridToNeo
import logging
import numpy

logger = logging.getLogger('biospytial.insert_taxonomies')

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
#ggg = GriddedTaxonomy(biosphere,mexmesh)













