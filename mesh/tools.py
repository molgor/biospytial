#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Mesh / Grid module
==================
This module implements tools for generating grids based on polygons.

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "0.0.8"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Unstable"

from django.db import connection
import logging

logger = logging.getLogger('biospatial.mesh.tools')


def createGridOnThisSquare(square,tablename,n_partitions_in_x):
    """
    .. createGridOnThisSquare
    
    This function creates a GRID in the database.
    It makes use of the function: generategridon(polygon,t_name_grid_division)
    defined in the database. 
    It you need to install this functions the scripts are in biospatial/SQL_functions
    
    .. note:: This function needs a SQUARE polygon given as parameter if this requirement is not
    satisfied the grid will not be regular or may have problems to be defined.
    
    Parameters
    ----------
    
        square : Geometry WKT
            This object should be a square.
            
        tablename : String
            The grid name that is going to have the newly created table.
            
        n_partitions_in_x : integer
            The number of partitionsper axis the grid is going to have with respect to the square parameter.
            For example: if n_partitions_in_x = 2 then the grid will have 4 squares, 
            therefore 2 partitions in the x axis and 2 partitions in the y axis.
            
    """

    cursor = connection.cursor()
    #works with (SELECT geom from tests.sketches WHERE id  = 6) as geom
    
    sentence = "SELECT mesh.generategridon(ST_Geomfromtext(\'%s\'), \'%s\',%i)" %(square,tablename,n_partitions_in_x)
    logger.info("Generating Grid %s" %tablename)
    cursor.execute(sentence)
    connection.commit()
    f = cursor.cursor.fetchall()
    logger.info('Done: %s'%f)
    return f


def createRegionalNestedGrid(parent_square,store_prefix,n_levels):
    """
    .. createRegionalNestedGrid
    This function creates the all the grids needed for analyzing a regions 
    with the Nestedtaxonomy module.
    The function uses the parent_square as parameter to define the square region in which it's going to 
    start the partion. The following levels are derived by partioning the former level by half in the X axis and half in the Y-axis
    giving four squares in the immediate successor. Therefore, each level is going to have 4 more cells than the previous level. 
    Giving a total number of 4^n cells, where n is the number of levels.
    This structure is the same as the canonical Quad-tree representation. 
    
    Parameters
    ----------
    
        parent_square : geometry
            The square geometric object in WKT. Should be a square.
            
        store_prefix : string
            The prefix name that the grids are going to have. Could be,
            for instance, the name of the main region. e.g. mex
            
        n_levels : integer
            The number of levels (partitions) to build.
            
    .. note:: As it can be seen, the computational complexity of this 
    function is exponential, meaning that a high number of levels will lead in a
    high performance process that could crash the server or the postgres instance.
    Be careful with the number of levels to generate.
    
    Parameters
    ----------
    
    Returns
    -------
    
        scales : dictionary
        The dictionary of the tables builded. For use with the mesh models. module
        
        e.g.
            scales = { 8 : 'mesh\".\"braz_grid8a',
              9 : 'mesh\".\"braz_grid16a',
              10 : 'mesh\".\"braz_grid32a',
              11 : 'mesh\".\"braz_grid64a',
              12 : 'mesh\".\"braz_grid128a',
              13 : 'mesh\".\"braz_grid256a',
              14 : 'mesh\".\"braz_grid512a',
              15 : 'mesh\".\"braz_grid1024a',
              16 : 'mesh\".\"braz_grid2048a',
              17 : 'mesh\".\"braz_grid4096a'
              }
    """
    levels = map(lambda i : (i,2**i), range(n_levels))
    
    scales = {}
    messages = []
    for id, n_p in levels:
        tablename =  'mesh\".\"'+store_prefix+str(n_p) 
        name = store_prefix+str(n_p)
        t = createGridOnThisSquare(parent_square,name,n_p)
        scales[id] = tablename
        messages.append(t)
    return scales
