#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Raster Data Aggregates
======================
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
from django.contrib.gis.db.models import RasterField,FloatField

from django.db.models import TextField



class getValue(Aggregate):
    """
    Aggregation method for get the value for a given coordinate point.
    """
    function = 'ST_Value'
    template = '%(function)s(%(expressions)s'
    
    def __init__(self,expression,**extra):
        
        geometry = extra.pop('geometry')
        if geometry.dims != 0:
            raise ValueError('The geometry given is not a Point')
        srid = geometry.srid

           
        #import ipdb; ipdb.set_trace()
        textpoint = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoint,srid)
        try:
            band = extra.pop('band')
        except:
            band = None
        if band:
            ## The request is multiband the query should match this: double precision ST_Value(raster rast, integer band, geometry pt, boolean exclude_nodata_value=true);
            stband = str(band)        
            self.template += ( ',' +  stband + ',' + geomtext + ')' )
        else:
            self.template += ',' + geomtext + ')'        
        
        super(getValue,self).__init__(
            expression,
            output_field = FloatField(),
            **extra
      )
    
    


class Union(Aggregate):
    """
        Aggregation method for extracting Raw data
    """  
    function = 'ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s' #Note the missing parenthesis
    
    
    def __init__(self,expression,**extra):
        
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)

        try:
            band = extra.pop('band')
        except:
            band = None
        if band:
            ## The request is multiband the query should match this: double precision ST_Value(raster rast, integer band, geometry pt, boolean exclude_nodata_value=true);
            stband =  str(band)
            self.template += ',' + stband + ')' # Here I close parenthesis (is for summoning the band) 
            self.template += ',' + geomtext + ')'  # Proceed normally           
           
        else:        
            self.template += '),' + geomtext + ')'        
        
        super(Union,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )


        
class Aspect(Aggregate):
    """
        Aggregation method for calculating Aspect on DEM
    """          
    function = 'ST_Aspect(ST_Transform(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        to_srid = extra.pop('to_srid')
        try:
            algorithm = extra.pop('algorithm')
        except:
            algorithm = 'NearestNeighbour'
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += '),' + geomtext + '),' + str(to_srid) +',\''+str(algorithm)+ '\')'
        self.template += ')'

        super(Aspect,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )

       
class Slope(Aggregate):
    """
        Aggregation method for calculating SLope on DEM
    """          
    function = 'ST_Slope(ST_Transform(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        to_srid = extra.pop('to_srid')
        try:
            algorithm = extra.pop('algorithm')
        except:
            algorithm = 'NearestNeighbour'
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += '),' + geomtext + '),' + str(to_srid) +',\''+str(algorithm)+ '\')'
        self.template += ')'

        super(Slope,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )


#class Hillshade(Aggregate):
#    """
#        Aggregation method for calculating hillshade (standard parameters)
#    """  
#    function = 'ST_Clip(ST_Hillshade(ST_Union'
#    template = '%(function)s(%(expressions)s))'
#    
#    
#    def __init__(self,expression,**extra):
#        geometry = extra.pop('geometry')
#        srid = geometry.srid
#        #import ipdb; ipdb.set_trace()
#        textpoly = '\'' + str(geometry.wkt) + '\''
#        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
#        self.template += ',' + geomtext + ')'
#        super(Hillshade,self).__init__(
#            expression,
#            output_field = RasterField(),
#            **extra
#      )
#
class Hillshade(Aggregate):
    """
        Aggregation method for calculating Hillshade on (standard parameters).
    """          
    function = 'ST_Hillshade(ST_Transform(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        to_srid = extra.pop('to_srid')
        try:
            algorithm = extra.pop('algorithm')
        except:
            algorithm = 'NearestNeighbour'
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += '),' + geomtext + '),' + str(to_srid) +',\''+str(algorithm)+ '\')'
        self.template += ')'

        super(Hillshade,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )



class SummaryStats(Aggregate):
    """
     Aggregation method for calculating summary statistics.
         Returns : 
             (count, sum, mean, stdev, min, max)
    """  
    function = 'ST_SummaryStats(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s)'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        try:
            band = extra.pop('band')
        except:
            band = None
        if band:
            ## The request is multiband the query should match this: double precision ST_Value(raster rast, integer band, geometry pt, boolean exclude_nodata_value=true);
            stband =  str(band)        
            self.template += ( ',' + geomtext + ')' + ',' +  stband  + ')' )
        else:
            self.template += ',' + geomtext + ')'  + ')'       
        
        # Extra parenthesis to close the clip and the summarystats
        
        super(SummaryStats,self).__init__(
            expression,
            output_field = TextField(),
            **extra
      )

class Rescale(Aggregate):
    """
        Aggregation method for adjusting only its scale or pixel size.
        Uses Potgis ST_Rescale
        ST_Rescale — Resample a raster by adjusting only its scale (or pixel size). New pixel values are computed using the NearestNeighbour, Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor
    """  
    #function = 'ST_Rescale(ST_Clip(ST_Union'
    function = 'ST_Clip(ST_Rescale(ST_Union'
    template = '%(function)s(%(expressions)s'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        scalexy = extra.pop('scalexy')
        algorithm = extra.pop('algorithm')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += '),' + str(scalexy) +',\''+str(algorithm)+ '\'),' + geomtext + ')' 
        super(Rescale,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )


class Resize(Aggregate):
    """
        Aggregation method for adjusting only its size in terms of num cols and num
        rows.
        Uses Potgis ST_Resize
        ST_Resize — Resize a raster by adjusting only its scale (or pixel size). New pixel values are computed using the NearestNeighbour, Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor
    """  
    #function = 'ST_Clip(ST_Resize(ST_Union'
    function = 'ST_Resize(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        width = extra.pop('width')
        height = extra.pop('height')
        algorithm = extra.pop('algorithm')
        srid = geometry.srid
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += '),' + geomtext + '),' + str(width) +',' + str(height) +',\''+str(algorithm)+ '\')'  
        super(Resize,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )



class Transform(Aggregate):
    """
        Reproject the selected raster data into a valid SRID. Returns a new raster
        data with the specified projection (int SRID).
        Uses Potgis ST_Transform
        New pixel values are computed using the NearestNeighbour, Bilinear, Cubic, CubicSpline or Lanczos resampling algorithm. Default is NearestNeighbor
    """  
    function = 'ST_Transform(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s'
    
    
    def __init__(self,expression,**extra):
        geometry = extra.pop('geometry')
        to_srid = extra.pop('to_srid')
        algorithm = extra.pop('algorithm')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)
        self.template += '),' + geomtext + '),' + str(to_srid) +',\''+str(algorithm)+ '\')'
        super(Transform,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )





class PixelAsPolygons(Aggregate):
    """
        Aggregation method for extracting polygons defined by pixel
        IT's not working. NEED TO REFACTOR.
    """  
    function = 'ST_PixelAsPolygons(ST_Clip(ST_Union'
    template = '%(function)s(%(expressions)s' #Note the missing parenthesis
    
    
    def __init__(self,expression,**extra):
        
        geometry = extra.pop('geometry')
        srid = geometry.srid
        #import ipdb; ipdb.set_trace()
        textpoly = '\'' + str(geometry.wkt) + '\''
        geomtext = "ST_GeomFromText(%s , %s)" %(textpoly,srid)

        try:
            band = extra.pop('band')
        except:
            band = None
        if band:
            ## The request is multiband the query should match this: double precision ST_Value(raster rast, integer band, geometry pt, boolean exclude_nodata_value=true);
            stband =  str(band)
            self.template += ',' + stband + ')' # Here I close parenthesis (is for summoning the band) 
            self.template += ',' + geomtext + ')'  # Proceed normally           
            self.template += ')' ## Close the pixel as polygon func
        else:        
            self.template += '),' + geomtext + ')'        
            self.template += ')' ## Close the pixel as polygon func
            
        super(PixelAsPolygons,self).__init__(
            expression,
            output_field = RasterField(),
            **extra
      )


        
aggregates_dict = { 'Original' : Union,
                    'Slope' : Slope,
                    'Hillshade' : Hillshade,
                    'SummaryStats' : SummaryStats,
                    'Aspect' : Aspect,
                    'getValue' : getValue,
                    'Rescale' : Rescale,
                    'PixelAsPolygons' : PixelAsPolygons,
                    'Transform' : Transform,
                    'Resize' : Resize
                   }

       
