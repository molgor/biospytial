from gbif.taxonomy import GriddedTaxonomy
from gbif.models import Occurrence
from mesh.models import initMesh
m1 = initMesh(7)
m1
m1.objects.all()
biosphere = Occurrence.objects.all()
#gg = GriddedTaxonomy(biosphere=biosphere,mesh=m1.objects.all())
