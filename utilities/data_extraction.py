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

def compilePredictorStack(polygon,pixel_size,list_of_models,algorithm='NearestNeighbour'):
    """
    Returns a dataframe corresponding to the subselection of the rasters models
    already scaled at the same resolution.

    Parameters:
        polygon : a valid gis.geos polygon
        pixel_size : (Float) The value to rescale the selected raster.
        list_of_models : (list) of Rastermodels from which the selection would be
        performed.
    """
    rasters = map(lambda model : RasterData(model,border=polygon),list_of_models)
    datacube_field = map(lambda raster :
            raster.resize(1000,1000,algorithm=algorithm),rasters)
    

    return rasters
