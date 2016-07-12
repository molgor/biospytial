from raster_api import aggregates
from django.contrib.gis.db import models
from compiler.ast import Function
from django.contrib.gis.db.models import RasterField
from django.contrib.gis.gdal import GDALRaster
from django.db.models import TextField
# Create your models here.
class Test(models.Model):
    """
    ..
    Only a test for raster data.
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    id = models.AutoField(primary_key=True, db_column="rid")
    rast = models.RasterField()
    objects = models.GeoManager()
    neo_label_name = 'test_viirs'
    
    class Meta:
        managed = False
        db_table = 'testviirs'
        


class DemMex(models.Model):
    """
    ..
    Digital Elevation Model for Mexico
    Scale 15m.
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    id = models.AutoField(primary_key=True, db_column="rid")
    rast = models.RasterField()
    objects = models.GeoManager()
    neo_label_name = 'DEM_120'
    
    class Meta:
        managed = False
        db_table = 'demmex'
        



class DemMexLow(models.Model):
    """
    ..
    Digital Elevation Model for Mexico
    Scale 15m.
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    id = models.AutoField(primary_key=True, db_column="rid")
    rast = models.RasterField()
    objects = models.GeoManager()
    neo_label_name = 'DEM_120'
    

        
    
    class Meta:
        managed = False
        db_table = 'demmex120'
        




    def __str__(self):
        c = "< Digital Elevation Model: %s >"
        return c
    
from django.db.models import Lookup



class intersectWith(Lookup):
    lookup_name = 'intersect_with'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        
        rhs, rhs_params = self.process_rhs(compiler, connection)
        # was hard to found this, anyway
        #import ipdb
        polygon = rhs_params[0]
        srid = polygon.srid
        textpoly = '\'' + str(polygon.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        #rhs_params[0] = geomtext
        params = lhs_params + rhs_params
        things = (str(lhs), str(geomtext))
        return 'ST_Intersects( %s ,  %s  )' % things, params
    
    


