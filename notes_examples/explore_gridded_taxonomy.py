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

## Select one cell of one thing

m7 = initMesh(7)
center = m7.objects.get(id=8023)

g = GriddedTaxonomy(biosphere,center)


#m1mexico = m1.objects.filter(cell__intersects=mexico_border.geom)

#mexgrid = MexMesh.objects.filter(cell__intersects=mexico_border.geom)
#gg = GriddedTaxonomy(biosphere=mexbiosphere,mesh=m1.objects.all())

#gg = GriddedTaxonomy(biosphere=mexbiosphere,mesh=m1mexico)

