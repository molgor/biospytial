#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Paper 2 (workflow) 
==================
..  
Usefull functions for the Paper2: 'Modelling species distribution with presence-only
data'
"""


__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2018, JEM"
__license__ = "GPL"
__version__ = "3.2.1"
__mantainer__ = "Juan"
__email__ ="j.escamilla.molgora@ciencias.unam.mx"
__status__ = "Prototype"

#from django.contrib.gis.geos import Polygon
from raster_api.tools import RasterData
from raster_api.models import raster_models as models
import utilities.data_extraction as de
import pandas as pd
import numpy as np
import logging


logger = logging.getLogger('biospytial.datapipelines')



#### Specific traversals that I dont know yet where to put them

def compileRasterandVectorPredictors(polygon,width,height,raster_models_list,vector_models_selection):
    """
    Generates a dataframe for selected datasets in raster or vector. 
    
    """
    raster_preds = de.compilePredictorRasterStack(polygon,width,height,raster_models_list,as_dataframe=False)
    r0 = raster_preds[0]
    dfrast = de._transformRasterStackToDF(raster_preds)
    points = r0.getCoordinatesAsGeometricPoints()
    vp = []
    for (vmodel,selfeats,nasvals) in vector_models_selection:
        vects_preds  = de.extractVectorFeatures(vmodel,points,selected_features=selfeats,nan_values_for_selected_features=nasvals)
        vp.append(vects_preds)
    vdf = pd.concat(vp,axis=1)
    total = pd.concat([vdf,dfrast],axis=1)
    return {'df': total,'rasters':raster_preds} 
