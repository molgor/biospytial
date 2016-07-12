from raster_api.aggregates import Union,Slope, Hillshade, SummaryStats
from raster_api.models import DemMexLow
from django.contrib.gis.db.models.fields import RasterField
from raster_api.models import intersectWith
from django.contrib.gis.gdal import GDALRaster
from raster_api.aggregates import aggregates_dict
from raster_api.tools import RasterData





import mesh.tools as mt
from gbif.taxonomy import Occurrence, Taxonomy, GriddedTaxonomy
from mesh.models import initMesh
# register the new lookup
RasterField.register_lookup(intersectWith)




a_p = (-106,30)

b_p = (-103,33)


d = mt.create_square_from_two_points(a_p,b_p)


biosphere = Occurrence.objects.all()

mex = biosphere.filter(geom__intersects=d['polygon'].wkt)

mmm = initMesh(4)
ggg = GriddedTaxonomy(mex,mmm.objects.all(),generate_tree_now=False,use_id_as_name=False)

t0 = ggg.taxonomies[0]
t1 = ggg.taxonomies[1]



aa = DemMexLow.objects.filter(rast__intersect_with=t0.biomeGeometry)

x = RasterData(DemMexLow,t1.biomeGeometry)
