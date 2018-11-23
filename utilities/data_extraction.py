#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Data Extraction Tools 
=====================
..  
This module includes utilities to extract complete datasets in standard formats. 
It can be seen as specified datapipelines ready to be used for model inputs.

"""


__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2018, JEM"
__license__ = "GPL"
__version__ = "3.2.1"
__mantainer__ = "Juan"
__email__ ="j.escamilla.molgora@ciencias.unam.mx"
__status__ = "Beta"

#from django.contrib.gis.geos import Polygon
from raster_api.tools import RasterData
from raster_api.models import raster_models_dic as models
import pandas as pd
import geopandas as gpd
import numpy as np
import logging
from shapely.geometry import Point

logger = logging.getLogger('biospytial.raster_api.tools')

def compilePredictorRasterStack(polygon,width,height,list_of_raster_models,algorithm='NearestNeighbour',as_dataframe=True):
    """
    Returns a dataframe corresponding to the subselection of the rasters models
    already scaled at the same resolution.

    Parameters:
        polygon : a valid gis.geos polygon
        height : (Integer,or float [percentage]) The number of rows in the resulting raster selection.
        width : (Integer,or float [percentage]) The number of columns  in the resulting raster selection.
        list_of_models : (list) of Rastermodels from which the selection would be
        performed.
        as_dataframe : (Bool) returns a dataframe with coordinates.
    """
    rasters = map(lambda model : RasterData(model,border=polygon),list_of_raster_models)
    datacube_field = map(lambda raster :
            raster.resize(width,height,algorithm=algorithm),rasters)
    
    logger.info("Alligning stacked raster data to common origin...")
    trast_params = rasters[0].rasterdata.geotransform
    for rst in rasters:
        rst.rasterdata.geotransform = trast_params
    if as_dataframe:
        df = _transformRasterStackToDF(rasters)
        return df
    else:
        return rasters

def _transformRasterStackToDF(rasterdata_list):
    dfs = pd.concat(map(lambda rst : rst.toPandasDataFrame(aggregate_with_mean=True,with_coordinates=False),rasterdata_list),axis=1)
    r0 = rasterdata_list[0]
    coords = r0.getCoordinates()
    df = pd.concat([dfs,coords],axis=1)
    return df

def extractVectorFeatures(vector_model,list_of_geometric_coordinates,selected_features="",nan_values_for_selected_features=""):
    """
    Returns a Pandas Dataframe of the selected features given a list of Points.
    """
    queryset = map(lambda p :
            vector_model.objects.filter(geom__intersects=p),list_of_geometric_coordinates)
    if selected_features:
        if isinstance(selected_features,list):
            logger.info("extracting info from: %s this can take some minutes"%str(vector_model))
            lvals = map(lambda qs : qs.values_list(*selected_features),queryset)
            try:
                nvals = [r.get() if r.exists() else nan_values_for_selected_features for
                    r in lvals ]
            except:
                logger.error("Nan_values_for_selected_features maybe incompatible with the number of selected features")
                return None
            return pd.DataFrame(nvals,columns=selected_features)
        else:
            logger.error("Selected features must be a list of valid model features (Columns)")
            return None
    else:
        logger.error("You must select some features to extract")
        return None


def extractSeveralVectorFeatures(list_of_points,vector_models_selection):
    """
    Extract a dataframe of a set of features.
    Parameters : 
        list_of_points (List) of Point Types (Geometric)
        vector_models_selection : A list of triplets.
        Each triplet has the form: 
            [VectorDataModelClass,['feature1','feature2'],[Nan-value for feature1,Nan for feature2]]
    """
    vp = []
    for (vmodel,selfeats,nasvals) in vector_models_selection:
        vects_preds  = extractVectorFeatures(vmodel,list_of_points,selected_features=selfeats,nan_values_for_selected_features=nasvals)
        vp.append(vects_preds)
    vdf = pd.concat(vp,axis=1)
    return vdf
	



def toGeoDataFrame(pandas_dataframe,xcoord_name='Longitude',ycoord_name='Latitude',srs = 'epsg:4326'):
    """
    Convert Pandas objcet to GeoDataFrame
    Inputs:
        pandas_dataframe : the pandas object to spatialise
        xcoord_name : (String) the column name of the x coordinate.
        ycoord_name : (String) the column name of the y coordinate. 
        srs : (String) the source referencing system in EPSG code.
                e.g. epsg:4326 .
    """
    data = pandas_dataframe
    #import ipdb; ipdb.set_trace()
    data[xcoord_name] = pd.to_numeric(data[xcoord_name])
    data[ycoord_name] = pd.to_numeric(data[ycoord_name])
    data['geometry'] = data.apply(lambda z : Point(z[xcoord_name], z[ycoord_name]), axis=1)
    #data['geometry'] = data.apply(lambda z : Point(z.LON, z.LAT), axis=1)

    new_data = gpd.GeoDataFrame(data)
    new_data.crs = {'init':'epsg:4326'}
    return new_data


       
