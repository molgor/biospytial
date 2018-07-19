from raster_api import aggregates
from django.contrib.gis.db import models
from django.contrib.gis.db.models import RasterField
from django.contrib.gis.gdal import GDALRaster
from django.db.models import TextField
from django.db.models import Lookup


### Class for looking-up geometries. This is auxiliary but very important.
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

# Create your spystats here.
## Old models, consider errasing them
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
    
    Note: Deprecated, use GenericRaster instead.
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
    Note: Deprecated, use GenericRaster instead.    
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


## New GenericRaster model. Parent of the rest.
class GenericRaster(models.Model):
    """
    A generic class for Raster objects. 
    The attributes are the one specified in a default configuration of the raster2psql
    function. 
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    id = models.AutoField(primary_key=True, db_column="rid")
    rast = models.RasterField()
    objects = models.GeoManager()
    
    class Meta:
        abstract = True
        managed = False
         
    def __str__(self):
        c = "< GenericRaster Data: %s >"
        return c        
              
class DemMex(GenericRaster):
    """
    ..
    Concrete model for the ElevationModel.
    In (meters).
    """

    units = '(meters)'
    number_bands = 1
    neo_label_name = 'DEM_12'
    link_type_name = 'Elevation'
    properties = {'units' : 'meters' ,
                  'resolution' : '12 m', 
                  }
                      
    class Meta:
        db_table = 'demmex'
        managed = False

    def __str__(self):
        c = "< ElevationMexico: %s  >"%self.units
        return c     
  
class ETOPO1(GenericRaster):
    """
    ..
    Concrete model for the ElevationModel.
    ETOPO
    In (meters).
    """
    number_bands = 1
    neo_label_name = 'ETOPO1'
    link_type_name = 'HAS_ELEVATION'
    properties = {'units' : 'arc-secs' ,
                  'resolution' : '1', 
    }
    
    class Meta:
        managed = False
        db_table = 'etopo1_ice_c_geotiff'

    def __str__(self):
        c = "< ElevationETOPO1: %s  >"%self.properties['units']
        return c     

class BioClimModel(GenericRaster):
    """
    ..
    Abstract model for all the BioClim variables
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    number_bands = 12
    class Meta:
        managed = False
        abstract = True     
    
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
        #db_table = 'bioclim\".\"prec'
        db_table = 'bioclim\".\"world-prec'
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
#        db_table = 'bioclim\".\"srad'
        db_table = 'bioclim\".\"world-srad'
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
        db_table = 'bioclim\".\"world-tmax'
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
    
class WorldPopulation(GenericRaster):
    """
    ..
    Abstract model for all the Worldpobpulation datasource.
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    number_bands = 1
    class Meta:
        managed = False
        abstract = True     
    
    def __str__(self):
        c = "< WorldPop Raster Data: %s >"
        return c
    
class WorldPopLatam2010(WorldPopulation):
    """
    Concrete model for World Population data for Latin America.
    In (C).
     Monthly data
    """
    #number_bands = 12
    neo_label_name = 'worldpop-latam'
    link_type_name = 'HAS_POPULATION_OF'
    units = '(persons/km2)'
    
    class Meta:
        db_table = 'lac_ppp_2010_adj_v2'
        managed = False

    def __str__(self):
        c = "<WorldPop-Latam: %s>"%self.units
        return c 

class DistanceToRoadMex(GenericRaster):
    """
    ..
    Abstract model for all the Distance to Road datasource.
    
    Attributes
    ==========
    I'll us the default attributes given by the raster2pgsql
    id : int Unique primary key
        This is the identification number of each element in the mesh.
    
    """
    number_bands = 1
    neo_label_name = 'Dist_to_road_mex'
    link_type_name = 'HAS_A_DISTANCE_OF'
    units = '(meters)'
 
    class Meta:
        managed = False
        db_table = 'dist_map_wgs84_clip'
    
    def __str__(self):
        c = "< Distance to Road Raster Data: %s >"
        return c
 



## SOme aux variables available to import within module.    
raster_models = [ETOPO1,Precipitation,SolarRadiation,MeanTemperature,
        MinTemperature,MaxTemperature,VaporPressure,
        WindSpeed,WorldPopLatam2010,DistanceToRoadMex]

raster_models_dic = {
'WindSpeed' : raster_models[7],
'Elevation' : raster_models[0],
'Vapor' : raster_models[6],
'MaxTemperature' : raster_models[5] ,
'MinTemperature' : raster_models[4] ,
'MeanTemperature' : raster_models[3] ,
'SolarRadiation' : raster_models[2], 
'Precipitation' : raster_models[1], 
'WorldPopLatam2010' : raster_models[8] ,
'DistanceToRoadMex' : raster_models[9],
}

#raster_models.pop(0)
