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
import numpy as np
import logging


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
        
