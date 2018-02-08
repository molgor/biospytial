#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Sampling
======
This module implements different sampling methods for nodes in the knowledge graph.

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2018, JEM"
__license__ = "GPL"
__version__ = "0.0.8"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"


import numpy as np

def CellRandomUniformSample(CellNodeClass,n,with_replacement=False):
    """
    Returns a random list of Cell Nodes given a class definition of a Mesh.
    Parameters : 
        CellNodeClass : A Cell(GraphObject) 
        k : (Integer) the size of the sample.
        with_replacement (Boolean) : the sample will be with or without replacement. 
    """
    

