#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Raster Data Tool
================
..  
Tools for converting, analysing and migrate to Neo4J


"""


__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2016, JEM"
__license__ = "GPL"
__version__ = "3.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"




from django.contrib.gis.gdal import GDALRaster
from raster_api.aggregates import SummaryStats,aggregates_dict, Union
from django.conf import settings
from matplotlib import pyplot as plt
import logging
from py2neo import Node, Relationship, Graph, NodeSelector
from biospytial import settings
from osgeo import gdal
from numpy.ma import masked_where,masked_equal
import numpy
from django.contrib.gis.db.models.fields import RasterField
from raster_api.models import intersectWith
import pandas as pd
from scipy.special import expit
from django.contrib.gis.geos import GEOSGeometry

# register the new lookup
RasterField.register_lookup(intersectWith)




neoparams = settings.NEO4J_DATABASES['default']
uri = "http://%(HOST)s:%(PORT)s%(ENDPOINT)s" % neoparams
graph = Graph(uri,bolt=True)
node_selector = NodeSelector(graph)

logger = logging.getLogger('biospytial.raster_api.tools')



class GDALRasterExtended(GDALRaster):
    
    def allBandStatistics(self):
        bands = [b for b in self.bands]
        stats = [ b.statistics() for b in bands]
        mins = []
        maxs = []
        means = []
        stds = []
        for s in stats:
            m, M, mu, st = s
            mins.append(m)
            maxs.append(M)
            means.append(mu)
            stds.append(st)
            
        ## extract the data
        min_t = min(mins)
        max_t = max(maxs)
        mean_t = sum(means) / float(len(means))
        # Maybe here put std but it's not important now
        stds_t = sum(stds) / float(len(stds))
        b = self.bands[0]
        
        return {'min':min_t,'max':max_t,'mean':mean_t,'mean_std':stds_t,'nodata':b.nodata_value}


    def getCentroidCoordinates(self):
        """
        Returns precise location of centroids derived by an affine transformation
        """
        A = numpy.array(self.geotransform).reshape(2,3)
        ## Create the coordinates in the matrix coordinate systems
        ijs = [ numpy.array((1,j,i)) for i in range(self.height) for j in range(self.width)]

        #ijs = [ numpy.array((1,i,j)) for i in range(self.height) for j in range(self.width)]
        coords = map(lambda v : A.dot(v),ijs)
        return coords
        
        

def aggregateDictToRaster(aggregate_dic):
    """
    FOR POSTGIS data retrieval only.
    Convert the input aggregate based on an aggregation of raster data in postgis (aggregate_dic)
     into a fully functional raster datatype.
    """
    key = aggregate_dic.keys()[0]
    try:
        raster = GDALRasterExtended(aggregate_dic[key])
        return raster
    except:
        logger.error("Could not extract Raster data from aggregation. The raster could not be defined in that area.")
        return None



class Raster(object):
    """
    Class that defines Raster Objects. 
    This includes the prediction done by models, other external data not in the relational database and extensible to objects in the relational database.
    """
    
    def __init__(self,rasterdata=''):
        self.rasterdata = rasterdata
    
    def exportToGeoTiff(self,filename,path=settings.PATH_OUTPUT):
        """
        Exports the raster data to a GeoTiff standard format. For use in any GIS for analysing or visualizing.
        
        Parameters : 
        
            filename : the filename to the output geotiff image. not necessary to add .tif
            path : the path to store the output. By default it uses the PATH_OUTPUT variable in settings
        
        """
        
        file_ = path + filename +'.tif'
        try:
            data = self.rasterdata.bands
        except AttributeError:
            logger.warning("No data defined. Loading data from the server this can take some time.")
            try:
                self.getRaster()
            except:
                logger.error("Unexpected Error. There was a problem with the server or this object's geographical extension")
                return None
            data = self.rasterdata.bands
        
        b1 = self.rasterdata.bands[0]
        NoData_value = b1.nodata_value
        proj_str = str(self.rasterdata.srs.wkt)
        driver = gdal.GetDriverByName('GTiff')
        geotransform = self.rasterdata.geotransform
        
        ## converting data to numpy n-array    
        data = map(lambda b : b.data(),data)
        data = numpy.array(data)
        
        ## Verifying structure 
        dim = len(data.shape)
        if dim == 3:
            nbands, ysize, xsize = data.shape
        else:
            ysize,xsize = data.shape
            nbands = 1 

                
        
        #output = driver.Create(file_,xsize,ysize,nbands,gdal.GDT_Int16)
        output = driver.Create(file_,xsize,ysize,nbands,b1.datatype())        
        for i in range(nbands):
            outband = output.GetRasterBand(i+1)
            outband.WriteArray(data[i])
        
        output.SetProjection(proj_str)
        outband.SetNoDataValue(NoData_value)
        output.SetGeoTransform(geotransform)
        output.FlushCache()
        
        
        #outband.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)  
        #ct = gdal.ColorTable()
        # Some examples 
        #ct.CreateColorRamp(0,(0,0,0),127,(255,0,0))
        #ct.CreateColorRamp(0,(0,0,255),255,(255,0,0))
        #import ipdb; ipdb.set_trace()
        #ct.SetColorEntry( 0, (0, 0, 0, 255) )
        #ct.SetColorEntry( 20, (0, 255, 0, 255) )
        #ct.SetColorEntry( 40, (255, 0, 0, 255) )
        #ct.SetColorEntry( 60, (255, 0, 255, 255) )
        # Set the color table for your band
        #import ipdb; ipdb.set_trace()
        #outband.SetColorTable(ct)    
        return None



     

    
    def plotField(self,stats_dir='default',band=1,xlabel='Temperatura Promedio (C)',**kwargs):
        """
        """
        try:
            matrix = self.rasterdata.bands[band - 1].data()
        except:
            logger.error("No raster data associated with specified band")
            return None
        if stats_dir == 'default':
            stats_dir = self.rasterdata.allBandStatistics()
        # Mask data 
        nodataval = stats_dir['nodata']
        matrix = masked_where(matrix == nodataval, matrix)
        f, ax = plt.subplots()

        plt.imshow(matrix,clim=(stats_dir['min'],stats_dir['max']),**kwargs)
        plt.text(0.2,-0.6,'Made with BiosPYtial: -Biodiversity Informatics-',horizontalalignment='center',verticalalignment='bottom',transform=ax.transAxes,fontsize=10)

        cbar = plt.colorbar(orientation='horizontal',shrink=0.8) 
        cbar.set_label(xlabel,size=12)
        # access to cbar tick labels:
        #cbar.ax.tick_params(labelsize=5) 
        plt.axis('off')
        #plt.show()
        return plt         
    
    def display_field(self,stats_dir='default',title='',band=1,**kwargs):
        p = self.plotField(stats_dir, band=band,xlabel=title+' Month',**kwargs)
        p.title(title)
        plt.show()
        return None
    
    def exportToJPG(self,filename,stats_dir,path=settings.PATH_OUTPUT,title='',unitstitle='',band=1,**kwargs):

        p = self.plotField(stats_dir, band=band,xlabel=unitstitle,**kwargs)
        p.title(title)
        file_ = path + filename + '.png'
        plt.savefig(file_)

        return None 

    def exportMonthlyStack(self,prefix,stats_dict,path=settings.PATH_OUTPUT,prefixtitle='',unitstitle='',lang='eng',**kwargs):
        """
        Export layer stack
        """
        #stats_dict = self.rasterdata.allBandStatistics()
        if lang == 'esp':
            months = {'01':'Enero','02':'Febrero','03':'Marzo','04':'Abril','05':'Mayo','06':'Junio','07':'Julio','08':'Agosto','09':'Septiembre','10':'Octubre','11':'Noviembre','12':'Diciembre'}
        else:
            months = {'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
        
        for i,name in months.items():
            self.exportToJPG(i+prefix, stats_dict, path=path, title=prefixtitle+name,unitstitle=unitstitle, band=int(i),**kwargs)
        


    def toNumpyArray(self):
        """
        Returns a narray
        """
        bands = map(lambda b : b.data(),self.rasterdata.bands)
        nodataval = self.rasterdata.allBandStatistics()['nodata']
        bands = map(lambda b : masked_equal(b,nodataval),bands)
        
        return numpy.ma.array(bands)


    def getCoordinates(self):
        """
        Returns array of coordinates for each pixel a wrapper.
        Translates it into a pandas object for better manipulation
        """
        data = pd.DataFrame(self.rasterdata.getCentroidCoordinates())
        data.columns = ['Longitude','Latitude']  
        return data
    
    def getCoordinatesAsGeometricPoints(self,srid=4326):
        """
        Returns a list of point geometries. Useful for functions that need geometries and not wkt or numpy array.
        Parameters: (Integer) EPSG code
        """ 
        coords = self.getCoordinates()
        toPoint = lambda array :'POINT(%s %s)'%(array[0],array[1])
        points = map(lambda p :GEOSGeometry(p,srid=srid), map(toPoint,coords.values))
        return points

    def toPandasDataFrame(self,aggregate_with_mean=False):
        """
        Returns the values of the raster as a pandas DataFrame with spatial column coordinates
        
        Parameters: 
            aggregate_with_mean : (Boolean) Will return the mean value of all the bands per pixel 
        """
        coords = self.getCoordinates()
        array_data = self.toNumpyArray()
        ## iterate according to numpy standard leftmost axis
        dataframes = map(lambda band : pd.DataFrame(band.flatten()),array_data)
        dataframes.append(coords)
        data = pd.concat(dataframes,axis=1)
        return data
        
    def meanLayer(self):
        """
        Returns a single layer (Matrix nxm) that represents the cellwise average value  
        """
        datacube = self.toNumpyArray()
        layer = numpy.mean(datacube, axis=0)
        return layer






class RasterData(Raster):
    """
    This class provides an interface for processing and analysing raster data stored in a postgis database
    
    FOR USE in POSTGIS
    """
    
    def __init__(self,rastermodelinstance,border,date='N.A'):
        """
        Parameters:
            rastermodel :  Is a django.contrib.db.spystats instance . An ORM in raster_data.spystats
            border : A polygon geometry. The border geometry that defines the interior of the raster.
            date : string for date. Important for matching nodes with date
        """
        super(RasterData,self).__init__(rasterdata='')
        self.model = rastermodelinstance.objects.filter(rast__intersect_with=border)
        self.geometry = border
        #self.rasterdata = ''
        self.neo_label_name = rastermodelinstance.neo_label_name
        self.number_bands = rastermodelinstance.number_bands
        self.aggregatedmodel = ''
        self.eventdate = date
        
    def getRaster(self,**bandnumber):
        """
        Returns : A GDALRaster
        """
        # First filter by border
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
        try:
            agg_dic = self.model.aggregate(raster=Union('rast',geometry=self.geometry,**bandnumber))
        except IndexError :
            return None
        raster = aggregateDictToRaster(aggregate_dic=agg_dic)
        self.rasterdata = raster
        return raster
    
    
    def processDEM(self,option=1):
        """
        Processes different products using a DEM as input.
        Currently implements:
            Parameters : 
                option : integer
                    1 : Raw DEM (Elevation)
                    2 : Slope (angle 0 - 90) 
                    3 : Aspect Orientation of facet (0, 360) 
                    4 : Hillshade (for visualising)
                    
        Returns : A GDALRaster
        """
        options = {2 : 'Slope', 4:'Hillshade', 1:'Original', 3:'Aspect'}
        key_opt = options[option]
        self.neo_label_name += ('-' + key_opt) 
        # First filter by border
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
        aggregate = aggregates_dict[key_opt]
        agg_dic = self.model.aggregate(raster=aggregate('rast',geometry=self.geometry))
        raster = aggregateDictToRaster(aggregate_dic=agg_dic)
        self.rasterdata = raster
        
        return raster

    def getValue(self,point,**bandnumber):
        """
        Returns the value in the coordinates given by the point.
        """
        band = bandnumber.get('band')
        if band:
            Z = self.model.filter(rast__intersect_with=point).aggregate(Z=aggregates_dict['getValue']('rast',geometry=point,**bandnumber))
            z = Z['Z']
            if z == None:
                z = settings.RASTERNODATAVALUE
            return z
        else:
            nbands = self.number_bands
            zs = []
            for i in range(1,nbands + 1):
                Z = self.model.filter(rast__intersect_with=point).aggregate(Z=aggregates_dict['getValue']('rast',geometry=point,band=i))
                zi = Z['Z']
                if zi == None:
                    zi = settings.RASTERNODATAVALUE
                zs.append(zi)
            return zs


    def getSummaryStats(self,**bandnumber):
        """
        Returns the summary statistics given by the function ST_SummaryStats over a ST_UNion of the blobs within the geometry.
        """
        if self.geometry.dims > 0:
        #self.model = self.model.filter(rast__intersect_with=self.geometry)
            agg_dic = self.model.aggregate(raster=SummaryStats('rast',geometry=self.geometry,**bandnumber))
            summary_str = agg_dic['raster']
            summary_str = summary_str.replace('(','').replace(')','')
            summary = summary_str.split(',')
            uniqueid = str(self.geometry.ewkt) + '-' + str(self.eventdate)
            dic_sum = {'uniqueid':uniqueid,'count':int(summary[0]),'sum':float(summary[1]),'mean':float(summary[2]),'stddev':float(summary[3]),'min':float(summary[4]),'max':float(summary[5])}        
        else:
            # It's a point.
            z = self.getValue(self.geometry,**bandnumber)
            uniqueid = str(self.geometry.ewkt) + '-' + str(self.eventdate)
            dic_sum = {'value' : z,'uniqueid':uniqueid}
            
        return dic_sum



    def rescale(self,scalexy,inplace=True,algorithm='NearestNeighbour'):
        """
        Scales the raster according to the scale parameter.
        Parameters:
            scalexy : pixelsize to scale the raster
            inplace : assigns the returned object to the current rasterdata attribute
            algorithm: resampling algorithm to use, 
            options are: NearestNeighbour,Bilinear, Cubic, CubicSpline or Lanczos         
        Returns : A GDALRaster
        """

        aggregate = aggregates_dict['Rescale']
        agg_dic = self.model.aggregate(raster=aggregate('rast',geometry=self.geometry,scalexy=scalexy,algorithm=algorithm))
        raster = aggregateDictToRaster(aggregate_dic=agg_dic)
        if inplace:
            self.rasterdata = raster
            
        return raster

        
    def getNode(self,writeDB=False,month='',**bands):
        """
        Returns a Node data structure that can be put into Neo4j
        """
        class_name = self.neo_label_name
        properties = self.getSummaryStats(**bands)
        if month:
            try:
                #Get summary uses the point data and therefore returns the value attribute
                properties['reg.val'] = self.getSummaryStats(band=month)['value']
            except:
                # In the case the data has only one band and we are ingesting the data without care
                properties['reg.val'] = self.getSummaryStats(band=1)['value']
                logger.warn("Band number selected (%s) doesn't exist. Using band one instead."%month)
        
        n0 = Node(class_name,**properties)
        #old_node = graph.find_one(class_name,property_key="uniqueid",property_value=properties['uniqueid'])
        old_node = node_selector.select(class_name,uniqueid=properties['uniqueid']).first()

        if old_node:
            return old_node
        else:
            if writeDB:
                graph.create(n0)
            return n0

    def PixelAsPolygons(self):
        """
        Returns a list of polygons (Testing) 
        """
        
        aggregate = aggregates_dict['PixelAsPolygons']
        cosa = self.model.aggregate(raster=aggregate('rast',geometry=self.geometry))
        #raster = aggregateDictToRaster(aggregate_dic=agg_dic) 
        return cosa        



class RasterContainer(Raster):
    """
    This class instantiates a full geospatial raster data structure (GDAL).
    It needs a numpy matrix and metadata obtained from a RasterData object. 
    The instance is built on this metadata and the given numpy narray.
    """
    
    def __init__(self,data,use_metadata_from='', exponential_fam="Identity"):
        """
        Parameters:
            data : (numpy narray) The data to be used for the raster.
            use_metadata_from_this_band : (GDALRaster Band) the metadata of the GDAL Raster are going to be set by this object.
        
           exponential_fam : (String) The type of link function used (GLM).
           Current implemented choices are:
            "Identity", (default)
            "Poisson",
            "Logit"
        If the family is different from Identity it will add the transformed layer as
        """
        super(RasterContainer,self).__init__(rasterdata='')
        self.metadatamodel = use_metadata_from
        self.rasterdata = self.buildRasterData(data,exponential_fam = exponential_fam)

    def buildRasterData(self,data,exponential_fam="Identity"):
        """
        Returns a GDAL Raster object (Extended).
        Parameters: 
           exponential_fam : (String) The type of link function used (GLM).
           Current implemented choices are:
            "Identity", (default)
            "Poisson",
            "Logit"
        If the family is different from Identity it will add the transformed layer as
        another band,
        """
        import numpy as np
        m = self.metadatamodel
        geotransform = m.geotransform
        band = m.bands[0]
        if exponential_fam == "Identity":
            tdata = data.flatten()
        elif exponential_fam == "Poisson" :
            tdata = np.exp(data.flatten())
            nodatav = np.exp(band.nodata_value)
        elif exponential_fam == "Bernoulli" :
            tdata = expit(data.flatten())
            nodatav = expit(band.nodata_value)
        else:
            raise ValueError("Incorrect parameter in: exponential_fam. Use options described in documentation ")
            

        if exponential_fam == "Identity":
            bands = [{'data':data.flatten(),
                     'size': (band.width, band.height),
                     'nodata_value': band.nodata_value,
                     }]
            
            
        else:
            bands = [{'data':data.flatten(),
                     'size': (band.width, band.height),
                     'nodata_value': band.nodata_value,
                      },
                      {'data' : tdata,
                       'size': (band.width, band.height),
                       'nodata_value':np.exp(band.nodata_value),
                      }
                    ]
        
        rst = GDALRasterExtended({'srid': m.srid,
                                                    'width': m.width,
                                                    'height': m.height,
                                                    'datatype': 7,
                                                    'origin' : m.origin,
                                                    'scale' : m.scale,
                                                    'bands': bands })
        return rst
    

    def display_field(self, stats_dir='default', title='', band=1, **kwargs):
        """
        Override method for displaying field. 
        Has to be done in order to display correctly the fields.
        """
        b = self.rasterdata.bands[band - 1]
        stats_dir = {'max': b.max,
                            'mean': b.min,
                            'min': b.min,
                            'nodata': b.nodata_value}
        
        return Raster.display_field(self, stats_dir=stats_dir, title=title, band=band, **kwargs)

    
meses = {'01':'Enero','02':'Febrero','03':'Marzo','04':'Abril','05':'Mayo','06':'Junio','07':'Julio','08':'Agosto','09':'Septiembre','10':'Octubre','11':'Noviembre','12':'Diciembre'}
#mex.exportToJPG('0'+name,s,title=month,band=int(name),cmap=plt.cm.inferno)
    
        
