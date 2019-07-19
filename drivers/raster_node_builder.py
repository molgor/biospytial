# raster_node_builder.py
# This module instantiates the Raster node binded to the Occurrences nodes. It also retrives the information in a statitstical objects.


# Author: Juan Escamilla 
# Date: 26/10/2016
 
#!/usr/bin/env python
#-*- coding: utf-8 -*-

from raster_api.models import raster_models
from raster_api.models import raster_models_dic
from raster_api.tools import RasterData
import biospytial.settings as setting
import pandas
import numpy

class RasterCollection(object):
    """
    This class defines a data structure of the associated values and areas of the occurrences involving a specific Local Tree Level.
    """
    
    def __init__(self,Tree):
        self.tree = Tree
        
    def getValuesFromPoints(self,string_selection):
        """
        Returns the values from the associated raster nodes based on the linked occurrence node.
        Options:
               
            string_selection $in$ {'Elevation', 'MaxTemperature', 'MeanTemperature',
             'MinTemperature', 'Precipitation', 'Vapor' , 'SolarRadiation' ,
          'WindSpeed'
            
        """
        values = self.tree.pullbackRasterNodes(string_selection)
        struct = RasterPointNodesList(values)
        prefix = 'points_'
        setattr(self,prefix + string_selection, struct)
        return struct

    def getPointCoordinates(self):
        """
        Returns the coordinates corresponding to the occurrences locations filter  by the selected node
        """
        coords = self.tree.getPointCoordinates()
        return coords
    
    def getAssociatedRasterAreaData(self,string_selection,aggregated=True,refresh_cache=False):
        """
        Returns the associated RasterData type for each cell where the occurrence happened.
        Options:
               
            string_selection $in$ {'Elevation', 'MaxTemperature', 'MeanTemperature',
             'MinTemperature', 'Precipitation', 'Vapor' , 'SolarRadiation' ,
          'WindSpeed'        
        """
        
        raster_model = raster_models_dic[string_selection]
        if aggregated:
            polygons = self.tree.mergeCells(refresh_cache=refresh_cache)
            rasters =  RasterData(raster_model,polygons)
            rasters.getRaster()
        else:
            cells = self.tree.getExactCells(refresh_cache=refresh_cache)
            polygons = map(lambda c : c.polygon,cells)
            rasters = map(lambda polygon : RasterData(raster_model,polygon),polygons)             
            map(lambda raster : raster.getRaster() , rasters)
        
        prefix = 'raster_'
        setattr(self,prefix + string_selection, rasters)
        return rasters        

 

    def getEnvironmentalVariablesPoints(self,vars=['MaxTemperature', 'MeanTemperature','MinTemperature','Precipitation','Vapor','SolarRadiation','WindSpeed'],with_coordinates=True):
        """
        
        """
        df = pandas.DataFrame()
        for variable in vars:
            raster = self.getValuesFromPoints(variable)
            environment_mean = raster.table.mean_yr_val
            environment_std = raster.table.std_yr_val
            df[variable + '_mean'] = environment_mean
            df[variable + '_std' ] = environment_std
        if with_coordinates :
            xy = self.getPointCoordinates()
            xy = pandas.DataFrame(xy,columns=('x','y'))
            df['x'] = xy.x
            df['y'] = xy.y
        return df


    def getEnvironmentalVariablesCells(self,vars=['Elevation','MaxTemperature', 'MeanTemperature','MinTemperature','Precipitation','Vapor','SolarRadiation','WindSpeed'],with_std=False):
        """
        This is by cell.
        But by definition each Tree is defined in a united cell. 
        It could be the union of multiple dijoint cells but the raster aggregation type is taken as ONE raster.
        
        Parameters :
            (Boolean flag) 
            with_std =  Returns the data with means and standard deviation
        
        THIS CAN BE PRIORS!!
        """
        df = {}
        for variable in vars:
            raster = self.getAssociatedRasterAreaData(variable)
            try:
                statistics = raster.rasterdata.allBandStatistics()
            except:
                #import ipdb; ipdb.set_trace()
                statistics = {'mean':'N.A.','mean_std':'N.A'}
            mean_env = statistics['mean']
            df[variable + '_mean'] = mean_env
            
            if with_std:
                std_env = statistics['mean_std']
                df[variable + '_std' ] = std_env
        return df




    
class RasterPointNodesList(object):
    """
    This class provides the operations and interface for handling list of raster nodes retrieved mainly by the Raster Collector on occurrence data.
    """    
    
    def __init__(self,list_duple_raster_occs):

        self.data, self.occurrences = zip(*list_duple_raster_occs)
        self.table = self.transformToTable()
        self.nametype = self.setNameType()
        
    def transformToTable(self):
        """
        Transforms the list of raster nodes into 
        """
        
        values = map(lambda node : ( node.value) ,self.data)
        dates = map(lambda o : o.event_date, self.occurrences)
        pd = pandas.DataFrame(values)
        means = map(lambda v : numpy.mean(v),values)
        std = map(lambda v : numpy.std(v),values)
        pd.columns = ['January','February','March','April','May','June','July','August','September','October','November','December']
        real_val = map(lambda node : node.regval, self.data)
        pd['registered_value'] = real_val
        pd['mean_yr_val'] = means
        pd['std_yr_val'] = std
        pd['date'] = dates
        pd['date'] = pandas.to_datetime(pd['date'],format='%Y-%m-%dT%H:%M:%S')
        #import ipdb; ipdb.set_trace()
        pd.replace(setting.NULL_DATA_INTEGER,setting.RASTERNODATAVALUE,inplace=True)
        return pd
 

    def areTypeHegemonic(self):
        """
        Check if the data is of the same type.
        """
        x = self.data[0]
        xlabel = x.__primarylabel__
        for i in self.data:
            ilabel = i.__primarylabel__
            if xlabel != ilabel:
                return False
        return True 
        
    def setNameType(self):
        """
        Only set an attribute for the name
        """
        x =  self.data[0]
        if self.areTypeHegemonic():
            return x.__primarylabel__
        else:
            return "MIXED DATATYPES"
        
