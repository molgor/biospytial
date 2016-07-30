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
    number_bands = 1
    neo_label_name = 'DEM_12'
    link_type_name = 'Elevation'
    properties = {'units' : 'meters' ,
                  'resolution' : '12 m', 
    }
    
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


class CheseaMeanTemperature(models.Model):
    """
    ..
    WorldWide Mean Temperature by month
    Scale 15m.
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    id = models.AutoField(primary_key=True, db_column="rid")
    rast = models.RasterField()
    band = models.TextField( db_column="filename")
    number_bands = 12
    objects = models.GeoManager()
    neo_label_name = 'MeanTemp-30s'
        
    class Meta:
        managed = False
        
        #db_table = 'bioclim\".\"tmean_30s'
        
        db_table = 'bioclim\".\"tmean_30s'
        
    def __str__(self):
        c = "< Mean Temperature: %s >"
        return c




class BioClimModel(models.Model):
    """
    ..
    Abstract model for all the BioClim variables
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    id = models.AutoField(primary_key=True, db_column="rid")
    rast = models.RasterField()
    band = models.TextField( db_column="filename")
    number_bands = 12
    objects = models.GeoManager()
        
    class Meta:
        managed = False
        abstract = True
        #db_table = 'bioclim\".\"tmean_30s'
        
        #b_table = 'bioclim\".\"tmean_30s'
        
    def __str__(self):
        c = "< Raster Data: %s >"
        return c


class Precipitation(BioClimModel):
    """
    Concrete model for the bioclim precipitation.
    In (mm). Monthly data
    """
    #number_bands = 12
    neo_label_name = 'Prec-30s'
    link_type_name = 'Precipitation'
    units = '(mm)'
    
    class Meta:
        db_table = 'bioclim\".\"prec'
        managed = False

    def __str__(self):
        c = "< Precipitation: %s  >"%self.units
        return c


class SolarRadiation(BioClimModel):
    """
    Concrete model for Solar Radiation.
    In (KJ m^-2 day^-1).
     Monthly data
    """
    #number_bands = 12
    neo_label_name = 'SlrRad-30s'
    link_type_name = 'SolarRadiation'
    units = '(KJ m^-2 day^-1)'
    
    class Meta:
        db_table = 'bioclim\".\"srad'
        managed = False

    def __str__(self):
        c = "< Solar Radiation: %s>"%self.units
        return c



class MeanTemperature(BioClimModel):
    """
    Concrete model for Temperature.
    In (C).
     Monthly data
    """
    #number_bands = 12
    neo_label_name = 'MeanTemp-30s'
    link_type_name = 'MeanTemperature'
    units = '(C)'
    
    class Meta:
        db_table = 'bioclim\".\"tavg'
        managed = False

    def __str__(self):
        c = "< Mean Temperature: %s>"%self.units
        return c  

class MaxTemperature(BioClimModel):
    """
    Concrete model for Temperature.
    In (C).
     Monthly data
    """
    #number_bands = 12
    neo_label_name = 'MaxTemp-30s'
    link_type_name = 'MaxTemperature'
    units = '(C)'
    
    class Meta:
        db_table = 'bioclim\".\"tmax'
        managed = False

    def __str__(self):
        c = "< Maximum Temperature: %s>"%self.units
        return c  

class MinTemperature(BioClimModel):
    """
    Concrete model for Temperature.
    In (C).
     Monthly data
    """
    #number_bands = 12
    neo_label_name = 'MinTemp-30s'
    link_type_name = 'MinTemperature'
    units = '(C)'
    
    class Meta:
        db_table = 'bioclim\".\"tmin'
        managed = False

    def __str__(self):
        c = "< Minimum Temperature: %s>"%self.units
        return c  

class VaporPressure(BioClimModel):
    """
    Concrete model for VaporPressure.
    In (C).
     Monthly data
    """
    #number_bands = 12
    neo_label_name = 'Vapor-30s'
    link_type_name = 'Vapor'
    units = 'kPa'
    
    class Meta:
        db_table = 'bioclim\".\"vapr'
        managed = False

    def __str__(self):
        c = "< VaporPressure: %s>"%self.units
        return c  
    
class WindSpeed(BioClimModel):
    """
    Concrete model for WindSpeed.
    In (C).
     Monthly data
    """
    #number_bands = 12
    neo_label_name = 'WindSpeed-30s'
    link_type_name = 'WindSpeed'
    units = '(m/s)'
    
    class Meta:
        db_table = 'bioclim\".\"wind'
        managed = False

    def __str__(self):
        c = "< WindSpeed: %s>"%self.units
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
    
    
raster_models = [DemMex,Precipitation,SolarRadiation,MeanTemperature,MinTemperature,MaxTemperature,VaporPressure,WindSpeed]

