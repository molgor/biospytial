#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Raster Data Aggregates
===========
..  
Aggregating function that make use of the POSTGIS RAster functions.

For use with Geoqueryset.aggregate(key=expression)

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2016, JEM"
__license__ = "GPL"
__version__ = "3.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



from django.db.models import Aggregate
from django.contrib.gis.db.models import RasterField

from django.db.models import TextField


class Union(Aggregate):
    function = 'ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s)'
    
    
    def __init__(self,expression,**extra):
        
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += ',' + geomtext + ')'        
        super(Union,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )
       # import ipdb;
       # ipdb.set_trace()
class Union_with_clip(Aggregate):
    function = 'ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s)'
    
    
    def __init__(self,expression,**extra):
        
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += ',' + geomtext + ')'
        super(Union_with_clip,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )

        
        
class Slope(Aggregate):        
    function = 'ST_Clip(ST_Slope(ST_Union'
    template = '%(function)s(%(expressions)s))'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += ',' + geomtext + ')'
        super(Slope,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )


class Hillshade(Aggregate):
    function = 'ST_Clip(ST_Hillshade(ST_Union'
    template = '%(function)s(%(expressions)s))'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += ',' + geomtext + ')'
        super(Hillshade,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )
        
class SummaryStats(Aggregate):
    function = 'ST_SummaryStats(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s)'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += ',' + geomtext + ')' + ')' # Extra parenthesis to close the clip and the summarystats
        super(SummaryStats,self).__init__(
            expression,
            output_field = TextField(),
            **extra
      )
        
aggregates_dict = { 'Original' : Union,
                    'Slope' : Slope,
                    'Hillshade' : Hillshade,
                    'SummaryStats' : SummaryStats,
                    'withclip' : Union_with_clip
                   }

       