#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Raster Data Toold
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
from raster_data.aggregates import SummaryStats



def aggregateDictToRaster(aggregate_dic):
    """
    Convert the input aggregate based on an aggregation of raster data in postgis (aggregate_dic)
     into a fully functional raster datatype.
    """
    key = aggregate_dic.keys()[0]
    raster = GDALRaster(aggregate_dic[key])
    return raster

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
        self.rasterdata = 'NA'
        
    def getGDALRaster(self,aggregate):
        """
        Returns : A GDALRaster
        """
        # First filter by border
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
        agg_dic = self.model.aggregate(raster=aggregate('rast',geometry=self.geometry))
        raster = aggregateDictToRaster(aggregate_dic=agg_dic)
        self.rasterdata = raster
        return raster
        

    def getSummaryStats(self):
        """
        Returns the summary statistics given by the function ST_SummaryStats over a ST_UNion of the blobs within the geometry.
        """
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
        agg_dic = self.model.aggregate(raster=SummaryStats('rast',geometry=self.geometry))
        summary_str = agg_dic['raster']
        summary_str = summary_str.replace('(','').replace(')','')
        summary = summary_str.split(',')
        dic_sum = {'count':int(summary[0]),'sum':float(summary[1]),'mean':float(summary[2]),'stddev':float(summary[3]),'min':float(summary[4]),'max':float(summary[5])}        
        return dic_sum




        