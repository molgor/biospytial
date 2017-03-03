## These are Notes for showing how to extract raster data from a polygon and export it to Geotiff

from sketches.models import Country
from raster_api.models import raster_models
from django.contrib.gis.db.models.fields import RasterField
from raster_api.tools import RasterData
from raster_api.models import intersectWith
from raster_api.models import MeanTemperature
from raster_api.models import raster_models


mexico = Country.objects.filter(name__contains='exico').get()
RasterField.register_lookup(intersectWith)




# Take a polygon in WKT and produce a geometric object.
polystr = "POLYGON((-119 1,-85 1,-85 33,-119 33,-119 1))"



from django.contrib.gis.geos import GEOSGeometry
polygon = GEOSGeometry(polystr)

#mex = RasterData(MeanTemperature,polygon)

mex = RasterData(MeanTemperature,mexico.geom)