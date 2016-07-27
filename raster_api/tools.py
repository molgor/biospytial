#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Raster Data Tool
===========
..  
Tools for converting, analysing and migrate to Neo4J


"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2016, JEM"
__license__ = "GPL"
__version__ = "3.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"




from django.contrib.gis.gdal import GDALRaster
from raster_api.aggregates import SummaryStats,aggregates_dict, Union
from django.conf import settings
from matplotlib import pyplot as plt
import logging
from py2neo import Node, Relationship, Graph
graph = Graph()
from osgeo import gdal
logger = logging.getLogger('biospatial.raster_api.tools')


def aggregateDictToRaster(aggregate_dic):
    """
    Convert the input aggregate based on an aggregation of raster data in postgis (aggregate_dic)
     into a fully functional raster datatype.
    """
    key = aggregate_dic.keys()[0]
    try:
        raster = GDALRaster(aggregate_dic[key])
        return raster
    except:
        logger.error("Could not extract Raster data from aggregation")
        return None

class RasterData(object):
    """
    This class provides an interface for processing and analysing raster data stored in a postgis database
    """
    
    def __init__(self,rastermodelinstance,border):
        """
        Parameters:
            rastermodel :  Is a django.contrib.db.models instance . An ORM in raster_data.models
            border : A polygon geometry. The border geometry that defines the interior of the raster.
        """
        self.model = rastermodelinstance.objects.filter(rast__intersect_with=border)
        self.geometry = border
        self.rasterdata = ''
        self.neo_label_name = rastermodelinstance.neo_label_name
        self.aggregatedmodel = ''
        
    def getRaster(self,**bandnumber):
        """
        Returns : A GDALRaster
        """
        # First filter by border
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
        agg_dic = self.model.aggregate(raster=Union('rast',geometry=self.geometry,**bandnumber))
        raster = aggregateDictToRaster(aggregate_dic=agg_dic)
        self.rasterdata = raster
        return raster
    
    
    def processDEM(self,option=1):
        """
        Processes different products using a DEM as input.
        Currently implements:
            Parameters : 
                option : integer
                    1 : Raw DEM (Elevation)
                    2 : Slope (angle 0 - 90) 
                    3 : Aspect Orientation of facet (0, 360) 
                    4 : Hillshade (for visualising)
                    
        Returns : A GDALRaster
        """
        options = {2 : 'Slope', 4:'Hillshade', 1:'Original', 3:'Aspect'}
        key_opt = options[option]
        self.neo_label_name += ('-' + key_opt) 
        # First filter by border
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
        aggregate = aggregates_dict[key_opt]
        agg_dic = self.model.aggregate(raster=aggregate('rast',geometry=self.geometry))
        raster = aggregateDictToRaster(aggregate_dic=agg_dic)
        self.rasterdata = raster
        
        return raster

    def getValue(self,point,**bandnumber):
        """
        Returns the value in the coordinates given by the point.
        """
        Z = self.model.filter(rast__intersect_with=point).aggregate(Z=aggregates_dict['getValue']('rast',geometry=point,**bandnumber))
        z = Z['Z']
        return z

    def getSummaryStats(self,**bandnumber):
        """
        Returns the summary statistics given by the function ST_SummaryStats over a ST_UNion of the blobs within the geometry.
        """
        if self.geometry.dims > 0:
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
            agg_dic = self.model.aggregate(raster=SummaryStats('rast',geometry=self.geometry,**bandnumber))
            summary_str = agg_dic['raster']
            summary_str = summary_str.replace('(','').replace(')','')
            summary = summary_str.split(',')
            uniqueid = str(self.geometry.ewkt)
            dic_sum = {'uniqueid':uniqueid,'count':int(summary[0]),'sum':float(summary[1]),'mean':float(summary[2]),'stddev':float(summary[3]),'min':float(summary[4]),'max':float(summary[5])}        
        else:
            # It's a point.
            z = self.getValue(self.geometry,**bandnumber)
            uniqueid = str(self.geometry.ewkt)
            dic_sum = {'value' : z,'uniqueid':uniqueid}
            
        return dic_sum



    def exportToGeoTiff(self,filename,path=settings.PATH_OUTPUT):
        """
        Exports the raster data to a GeoTiff standard format. For use in any GIS for analysing or visualizing.
        
        Parameters : 
        
            filename : the filename to the output geotiff image. not necessarry to add .tif
            path : the path to store the output. By default it uses the PATH_OUTPUT variable in settings
        
        """
        
        file_ = path + filename +'.tif'
        data = self.rasterdata.bands[0].data()
        NoData_value = self.rasterdata.bands[0].nodata_value
        proj_str = str(self.rasterdata.srs.wkt)
        driver = gdal.GetDriverByName('GTiff')
        geotransform = self.rasterdata.geotransform
        ysize,xsize = data.shape 
        
        output = driver.Create(file_,xsize,ysize,1,gdal.GDT_Int16)
        
        #import ipdb; ipdb.set_trace()
        output.GetRasterBand(1).WriteArray(data)
        output.SetProjection(proj_str)
        output.GetRasterBand(1).SetNoDataValue(NoData_value)
        output.SetGeoTransform(geotransform)
        output.FlushCache()
        
        return None


        
    def getNode(self,writeDB=False):
        """
        Returns a Node data structure that can be put into Neo4j
        """
        class_name = self.neo_label_name
        properties = self.getSummaryStats()
        n0 = Node(class_name,**properties)
        old_node = graph.find_one(class_name,property_key="uniqueid",property_value=properties['uniqueid'])
        if old_node:
            return old_node
        else:
            if writeDB:
                graph.create(n0)
            return n0
        
     
    def display_field(self,**kwargs):
        try:
            matrix = self.rasterdata.bands[0].data()
        except:
            logger.error("No raster data associated. Run getRaster or processDEM first")
            return None
        plt.imshow(matrix,**kwargs) 
        plt.show()
        return None
    
    
    
    
    
    
        