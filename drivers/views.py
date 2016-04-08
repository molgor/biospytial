#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
"""

Http interfaces using Views
===========================
..
This module implements command-line tools for use in external applications through HTTP request/responses.
TO feed the database with CSV files.

.. note::
    This is where all the interfaces between biospytial and QGIS or Browsers should be living.

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2016, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



import logging
logger = logging.getLogger('biospatial.gbif.views')


def ExtractDataFromCSVFile(request):
    """
    .. ExtractDataFromCSVFile:
    
    This view will read a CSV file and insert it into the database.
    It's intented to be used in parallel with other modules in a Docker platform.
    
    The absolute path is given by default in the settings file.
    PATHTOCSVFILES
    
    Parameters in GET variable
    ===========================
    filename : string
        The file name.
        
    Returns
    =======
    HTTP RESPONSE
    with text showing status.
    

    """

    import ipdb
    from biospatial.settings import CSVABSOLUTEPATH
    import drivers.populate as populate
    
    response = HttpResponse()
    get = request.GET
    
   

    try:
        filename = get['filename']
    except:
        response.content='Bad request. Check GET variable definitions \n. Check filename value'
        response.status_code = 400
        return response
    
    
    Abspath = CSVABSOLUTEPATH + '/' + filename
    html = "Filename to analysed will be: %s" %Abspath
    
    try:
        #dictionary_csv,_file = populate.CSVReadfrom(Abspath)
        dictionary_csv = populate.CSVLoadfrom(Abspath)

    except:
        html = 'File doesn\'t exist in the filesystem. Check parameters in Settings file '
        response.status_code = 415
        response.content=(html)
        return response
    try:
        #ipdb.set_trace()
        list_objects = populate.createOccurrenceFromCSVFile(dictionary_csv)
        #map(lambda o : o.insertOccurrence(),list_objects)
    except:
        html = 'Can\'t insert data in database. Check connection and try again'
        response.status_code = 500
        response.content=(html)
        return response
    response.content=(html)
    #response.content=str(forest[taxonomic_level])
    response.status_code = 200
    
    return response