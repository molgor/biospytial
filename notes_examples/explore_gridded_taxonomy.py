from gbif.taxonomy import GriddedTaxonomy
from gbif.models import Occurrence
from mesh.models import initMesh
from mesh.models import MexMesh
from mesh.tools import migrateGridToNeo
import logging


logger = logging.getLogger('biospytial.mesh.tools')

#m1 = initMesh(7)
#m1
#m1.objects.all()
biosphere = Occurrence.objects.all()


from sketches.models import Country
mexico_border = Country.objects.filter(name__contains='exico').get()
mexbiosphere = biosphere.filter(geom__intersects=mexico_border.geom)

#m1mexico = m1.objects.filter(cell__intersects=mexico_border.geom)

#mexgrid = MexMesh.objects.filter(cell__intersects=mexico_border.geom)
#gg = GriddedTaxonomy(biosphere=mexbiosphere,mesh=m1.objects.all())

#gg = GriddedTaxonomy(biosphere=mexbiosphere,mesh=m1mexico)

<<<<<<< HEAD
=======
#migrateGridToNeo(MexMesh,intersect_with=mexico_border.geom)

# for i in range(1,7):
#     m =  initMesh(i)
#     c = m.objects.all()[0]
#     logger.info("INSERTING MESH %s IN THE GRAPH DATABASE"%c.getScaleLevel())
#     del(m)
#     
#     
>>>>>>> 289c71560bbf46824d420ca0325635a3b104c7eb
    