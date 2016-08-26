#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
GBIF Models
===========
.. _gbif_models_intro:
Here it is defined the Object Relational Mapping between
the Classes Gbif Occurrences, Gbif Species, ...  , Gbif Kingdoms
that are defined in the external database.
Models for GBIF objects. 

"""
from ete2.nexml._nexml_tree import Children
from raster_api.tools import RasterData


__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2014, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db import utils
import logging
from django.test import TestCase
from django.conf import settings
import dateutil.parser
from py2neo import Node, Relationship, Graph
from django.conf import settings
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min

import drivers.neo4j_reader as neo 

import ipdb;

logger = logging.getLogger('biospatial.gbif')

graph = Graph()
from django.forms import ModelForm
# Model for GBIF as given by Raúl Jimenez


class Occurrence_CSV_Verbatim(models.Model):
    #     id_gbif = models.IntegerField()
    id = models.AutoField(primary_key=True, db_column="id_gbif")
    popo =  models.TextField(db_index=False,blank=True, null=True)
    dataset_id = models.TextField(db_index=False,blank=True, null=True)
    institution_code = models.TextField(db_index=False,blank=True, null=True)
    collection_code = models.TextField(db_index=False,blank=True, null=True)
    catalog_number = models.TextField(db_index=False,blank=True, null=True)
    basis_of_record = models.TextField(db_index=False,blank=True, null=True)
    scientific_name = models.TextField(db_index=True, blank=True, null=True)
    scientific_name_author = models.TextField(db_index=False,blank=True, null=True)
    taxon_id = models.IntegerField(blank=True, null=True)
    kingdom = models.TextField(db_index=True, blank=True, null=True)
    phylum = models.TextField(db_index=True, blank=True, null=True)
    _class = models.TextField(db_index=True, blank=True, null=True)
    _order = models.TextField(db_index=True, blank=True, null=True)
    family = models.TextField(db_index=True, blank=True, null=True)
    genus = models.TextField(db_index=True, blank=True, null=True)
    specific_epithet = models.TextField(db_index=True, blank=True, null=True)
    kingdom_id = models.IntegerField(db_index=True,blank=True, null=True)
    phylum_id = models.IntegerField(db_index=True,blank=True, null=True)
    class_id = models.IntegerField(db_index=True,blank=True, null=True)
    order_id = models.IntegerField(db_index=True,blank=True, null=True)
    family_id = models.IntegerField(db_index=True,blank=True, null=True)
    genus_id = models.IntegerField(db_index=True,blank=True, null=True)
    species_id = models.IntegerField(db_index=True,blank=True, null=True)
    country_code = models.TextField(db_index=False, max_length=7,blank=True, null=True)
    latitude = models.FloatField(db_index=True,blank=True, null=True)
    longitude = models.FloatField(db_index=True,blank=True, null=True)
    year = models.IntegerField(db_index=True,blank=True, null=True)
    month = models.IntegerField(db_index=True,blank=True, null=True)
    event_date = models.DateTimeField(db_index=True,blank=True, null=True)
    elevation_in_meters = models.TextField(db_index=False,blank=True, null=True)
    depth_in_meters = models.TextField(db_index=False,blank=True, null=True)
    verbatim_scientific_name = models.TextField(db_index=False,blank=True, null=True)
    taxon_rank = models.TextField(db_index=False,blank=True, null=True)
    verbatim_kingdom = models.TextField(db_index=False,blank=True, null=True)
    verbatim_phylum = models.TextField(db_index=False, blank=True, null=True)
    verbatim_class = models.TextField(db_index=False, blank=True, null=True)
    verbatim_order = models.TextField(db_index=False, blank=True, null=True)
    verbatim_family = models.TextField(db_index=False, blank=True, null=True)
    verbatim_genus = models.TextField(db_index=False, blank=True, null=True)
    verbatim_specific_epithet = models.TextField(db_index=False, blank=True, null=True)
    verbatim_infraspecific_epithet = models.TextField(db_index=False, blank=True, null=True)
    verbatim_latitude = models.TextField(db_index=False,blank=True, null=True)
    verbatim_longitude = models.TextField(db_index=False,blank=True, null=True)
    coordinate_precision = models.TextField(db_index=False,blank=True, null=True)
    maximum_elevation_in_meters = models.TextField(db_index=False,blank=True, null=True)
    minimum_elevation_in_meters = models.TextField(db_index=False,blank=True, null=True)
    elevation_precision = models.TextField(db_index=False,blank=True, null=True)
    minimum_depth_in_meters = models.TextField(db_index=False,blank=True, null=True)
    maximum_depth_in_meters = models.TextField(db_index=False,blank=True, null=True)
    depth_precision = models.TextField(db_index=False,blank=True, null=True)
    continent_ocean = models.TextField(db_index=False, blank=True, null=True)
    state_province = models.TextField(db_index=False,blank=True, null=True)
    county = models.TextField(db_index=False,blank=True, null=True)
    country = models.TextField(db_index=False,blank=True, null=True)
    recorded_by  = models.TextField(db_index=False,blank=True, null=True)
    locality  = models.TextField(db_index=False,blank=True, null=True)
    verbatim_year = models.TextField(db_index=False,blank=True, null=True)
    verbatim_month = models.TextField(db_index=False,blank=True, null=True)
    day = models.IntegerField(db_index=False,blank=True, null=True)
    verbatim_basis_of_record  = models.TextField(db_index=False,blank=True, null=True)
    identified_by  = models.TextField(db_index=False,blank=True, null=True)
    date_identified = models.TextField(db_index=False,blank=True, null=True)
    created = models.TextField(db_index=False,blank=True, null=True)
    modified = models.TextField(db_index=False,blank=True, null=True)
    






class Occurrence(models.Model):
    """
    .. _gbif.models.occurrece:
    This is the Base class that maps the Occurrence (and further taxonomic aggregates)
    with the spatial enabled database. The current database is built on Postgis.
    It includes the field string length definition for automatic populating the database using a standard CSV provided by GBIF.
    
    Attributes
    ----------
    id : int
        Identification value of each occurrence. Unique to any element of the GBIF dataset.
    dataset_id : int
        Identification of the collection (Currently not used)
    institution_code : int
        Identification for the institution resposible for storing, capturing or recording the occurrence.
    collection_code : int
        Identification of the collection (Currently not used)
    catalog_number : int 
        Identification for catalog number
    basis_of_record : int
        Unknown value
    scientific_name : String
        Species name in the binomial nomenclature
    kingdom : String
        Name of the kingdom to whom these occurrence belongs
    phylum : String
        Name of the phylum to whom these occurrence belongs
    _class : String
        Name of the class to whom these occurrence belongs
    _order : String
        Name of the order to whom these occurrence belongs
    family :String
        Name of the family to whom these occurrence belongs
    genus : String
        Name of the genus to whom these occurrence belongs
    specific_epithet : string
        Name of the epithet to whom these occurrence belongs   
    kingdom_id : int
        Identification number for the belonging kingdom (indexed).
    phylum_id : int
        Identification number for the belonging phylum (indexed).    
    class_id : int
       Identification number for the belonging class (indexed).
    order_id : int
       Identification number for the belonging order (indexed).
    family_id : int
       Identification number for the belonging family (indexed).
    genus_id : int
       Identification number for the belonging genus (indexed).
    species_id : int
       Identification number for the belonging species (indexed).
    country_code : string
        String representing the country's code
    latitude : Float
        Latitude in WGS84 (degrees) 
    longitude : Float
        Longitud in WGS84 (degrees)
    year : int
        Year of record
    month : int
        Month of record
    event_date : datetime
        Timestamp of record
    state_province : String
        Name of state or province
    county : String
        Name of country
    geom : Geometric Point
        Geometric Value in WKB
    objects : models.GeoManager()
        Wrapper for GeoDjango
    
    """
    chars = {'l1':55,'l2':55,'l3':55,'l4':100,'l5':60,'l6':70,'l7':100}
    id = models.AutoField(primary_key=True, db_column="id_gbif")
    #id_gf = models.IntegerField(blank=True,null=True)
    dataset_id = models.TextField(db_index=True,blank=True, null=True)
    institution_code = models.TextField(db_index=True, blank=True, null=True)
    collection_code = models.TextField(db_index=True, blank=True, null=True)
    catalog_number = models.TextField(db_index=True, blank=True, null=True)
    basis_of_record = models.TextField(db_index=True, blank=True, null=True)
    scientific_name = models.TextField(db_index=True, blank=True, null=True)
    #scientific_name_author = models.TextField(db_index=True,blank=True, null=True)
    #taxon_id = models.IntegerField(blank=True, null=True)
    kingdom = models.TextField(db_index=True, blank=True, null=True)
    phylum = models.TextField(db_index=True, blank=True, null=True)
    _class = models.TextField(db_index=True, blank=True, null=True)
    _order = models.TextField(db_index=True, blank=True, null=True)
    family = models.TextField(db_index=True, blank=True, null=True)
    genus = models.TextField(db_index=True, blank=True, null=True)
    specific_epithet = models.TextField(db_index=True, blank=True, null=True)
    kingdom_id = models.IntegerField(db_index=True,blank=True, null=True)
    phylum_id = models.IntegerField(db_index=True,blank=True, null=True)
    class_id = models.IntegerField(db_index=True,blank=True, null=True)
    order_id = models.IntegerField(db_index=True,blank=True, null=True)
    family_id = models.IntegerField(db_index=True,blank=True, null=True)
    genus_id = models.IntegerField(db_index=True,blank=True, null=True)
    species_id = models.IntegerField(db_index=True,blank=True, null=True)
    country_code = models.TextField(db_index=True, max_length=7,blank=True, null=True)
    latitude = models.FloatField(db_index=True,blank=True, null=True)
    longitude = models.FloatField(db_index=True,blank=True, null=True)
    year = models.IntegerField(db_index=True,blank=True, null=True)
    month = models.IntegerField(db_index=True,blank=True, null=True)
    day = models.IntegerField(db_index=True,blank=True, null=True)

    event_date = models.DateTimeField(db_index=True,blank=True, null=True)
    #elevation_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #depth_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #verbatim_scientific_name = models.TextField(db_index=True,blank=True, null=True)
    #taxon_rank = models.IntegerField(db_index=True,blank=True, null=True)
    #verbatim_kingdom = models.TextField(db_index=True,blank=True, null=True)
    #verbatim_phylum = models.TextField(db_index=True,blank=True, null=True)
    #verbatim_class = models.TextField(db_index=True,blank=True, null=True)
    #verbatim_order = models.TextField(db_index=True,blank=True, null=True)
    #verbatim_genus = models.TextField(db_index=True, blank=True, null=True)
    #verbatim_family = models.TextField(db_index=True, blank=True, null=True)
    #verbatim_specific_epithet = models.TextField(db_index=True,blank=True, null=True)
    #verbatim_infraspecific_epithet = models.TextField(db_index=True, blank=True, null=True)
    #verbatim_latitude = models.FloatField(db_index=True,blank=True, null=True)
    #verbatim_longitude = models.FloatField(db_index=True,blank=True, null=True)
    #coordinate_precision = models.FloatField(db_index=True,blank=True, null=True)
    #maximum_elevation_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #minimum_elevation_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #elevation_precision = models.FloatField(db_index=True,blank=True, null=True)
    #minimum_depth_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #maximum_depth_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #depth_precision = models.FloatField(db_index=True,blank=True, null=True)
    #continent_ocean = models.FloatField(db_index=True,blank=True, null=True)
    state_province = models.TextField(db_index=True,blank=True, null=True)
    county = models.TextField(db_index=True,blank=True, null=True)
    country = models.TextField(db_index=True,blank=True, null=True)
    #recorded_by  = models.TextField(db_index=True,blank=True, null=True)
    #locality  = models.TextField(db_index=True,blank=True, null=True)
    #verbatim_month = models.IntegerField(db_index=True,blank=True, null=True)
    #verbatim_year = models.IntegerField(db_index=True,blank=True, null=True)
    #day = models.IntegerField(db_index=True,blank=True, null=True)
    #verbatim_basis_of_record  = models.TextField(db_index=True,blank=True, null=True)
    #date_identified = models.DateTimeField(db_index=True,blank=True, null=True)
    #identified_by  = models.TextField(db_index=True,blank=True, null=True)
    #created = models.DateTimeField(db_index=True,blank=True, null=True)
    geom = models.PointField()
    #modified = models.DateTimeField(db_index=True,blank=True, null=True)
    objects = models.GeoManager()
    
    class Meta:
        #managed = False
        
        # remote server table name
        db_table = settings.GBIF_DATATABLE
        #db_table = "gbif_occurrence"
        # Local table name
        #db_table = "mexico_gbif_subset"
 
    def __unicode__(self):
        """
        ..
        String representation of Occurrence
        Returns
        -------
        info : string
            Name
        """
        return u'<GBIF Occurrence: %s  scientific_name: %s>\n Kingdom: %s \n,\t Phylum: %s \n,\t \t Order: %s,\n \t \t \t Class: %s, \n \t \t \t \t Family: %s, \n \t \t \t \t \t Location: s<\GBIF Occurrence>' %(self.id,self.scientific_name,self.kingdom,self.phylum,self._order,self._class,self.family) #,self.geom)
        

    def getfullDescription(self):
        """
        ..
        Retrieves the total description of the fields for the this registry.
        
        Returns
        -------
        info : string
            The information of all fields. Good for exporting raw data to CSV.
        """
        fields =  self._meta.get_all_field_names()
        cadena = ["<GBIF/: Occurrence %s --%s />\n" %(self.id,self.scientific_name)]
        for f in fields:
            c = "\t < %s: %s />\n" %(f,getattr(self,f))
            cadena.append(c)
        return reduce(lambda x,y : x+y,cadena)    
 

    def createNode(self,writeDB=False):
        """
        This method returns a Node Object based on all the attributes of the Class Level
        """
        
        #Node(Tree.level,name=Tree.name,id=Tree.id,parent_id=Tree.parent_id,abundance=Tree.abundance)    
        keys = settings.OCCURRENCE_KEYS_4NEO
        #keys = ['species_id','scientific_name','year','month','day','latitude','longitude','geom','event_date','basis_of_record']
 #       import ipdb; ipdb.set_trace()
        cd = self.__dict__
        dictio = dict([(k,cd[k]) for k in keys])
        dictio['levelname'] = "Occurrence"
        dictio['level'] = 999
        dictio['pk'] = self.pk
        dictio['geom'] = dictio['geom'].ewkt
        dictio['name'] = reduce(lambda a,b : a + ' ' +b ,self.scientific_name.split(" ")[0:2])
        dictio['event_date'] = self.event_date.isoformat()
        #labels = [str(type(self))]
        labels = ["Occurrence"]
        
        #dictio['keyword':keyword]
        
        node = Node(*labels,**dictio)
        
        ## HERE INSERT CODE FOR CHECKING IF A NEW ATTRIBUTE IS ADDED.
        
        node2 = graph.find_one("Occurrence",property_key='pk',property_value=self.pk)
        if node2:
            logger.debug("node existss")
            return node2
        else:
            if writeDB:
                graph.create(node)
            return node



    def getNode(self):
        """
        Only a wrapper for createNOde. It won't create a node 
        """
        node = self.createNode()
        return node
        
    def extractRasterDataFrom(self,RasterModel):
        """
        This is an occurrence. 
        The geom is a point. The result is the minium blob
        """
        date = reduce(lambda a,b : a + '-' + b, [str(self.day),str(self.month),str(self.year)])
        raster_data = RasterData(RasterModel,self.geom,date=date)
        #z = raster_data.getValue(self.geom)
        return raster_data



    def processDEMAs(self,DemModel,option=1):
        """
        Extracts the value from a DEM or secondary product. Based on the options are available.
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
        
        dem_data = self.extractRasterDataFrom(DemModel)
        dem_data.processDEM(option=option)
        return dem_data
    
    
    def nodeRasterData(self,RasterModel):
        """
        USes the builtin function of RasterData to return a node.
        See extractRasterDataFromDEM
        Attention:
            
            This could be Area because the definition is taken on the border.
        
        """
        date = reduce(lambda a,b : a + '-' + b, [str(self.day),str(self.month),str(self.year)])

        rd = RasterData(RasterModel,self.geom,date=date)
        month = self.month
        if isinstance(month, int):
            node = rd.getNode(month=self.month)
        else: 
            node = rd.getNode()
        return node
    
    def getNodeDEM(self,DemModel,option=1):
        """
            Parameters : 
               option : integer
                    1 : Raw DEM (Elevation)
                    2 : Slope (angle 0 - 90) 
                    3 : Aspect Orientation of facet (0, 360) 
                    4 : Hillshade (for visualising)
        """
        date = reduce(lambda a,b : a + '-' + b, [str(self.day),str(self.month),str(self.year)])

        dem_data = self.processDEMAs(DemModel, option=option)
        node = self.nodeRasterData(dem_data,date)
        return node
    
    def bind_withNodeDEM(self,DemModel,option=1,writeDB=False):
        """
        Creates a DEM nodes, calls the self.node and make a relationship
        """ 
        dem_node = self.getNodeDEM(DemModel,option=option)
        node = self.getNode()
        relation_name = DemModel.link_type_name
        rel = Relationship(node,relation_name,dem_node)
        #parent_props = {'value' : self.parent.abundance}        
        ### Check this to do not repeat relationships.
        if writeDB:
            graph.create(rel)
        #relations = graph.match(start_node=node,rel_type=relation_name,end_node=dem_node)
        return rel

    def bind_withNodeRaster(self,RasterModel,writeDB=False):
        """
        Creates a DEM nodes, calls the self.node and make a relationship
        """ 
        raster_node = self.nodeRasterData(RasterModel)
        node = self.getNode()
        relation_name = RasterModel.link_type_name
        rel = Relationship(node,relation_name,raster_node)
        #parent_props = {'value' : self.parent.abundance}        
        ### Check this to do not repeat relationships.
        if writeDB:
            graph.create(rel)
        #relations = graph.match(start_node=node,rel_type=relation_name,end_node=dem_node)
        return rel

    def getDescendingChain(self,depth,relation_type='IS_A_MEMBER_OF'):
        """
        Given the parameter depth it walks through the Subgraph Taxonomy
        Starting from the Occurrence Node to the depth specified.
        Remember that there is a loop in the LUCA node there fore, 
        """
        no = self.getNode()
        #rel = n.match(rel_type=relation_type).next()
        nodes = []
        #import ipdb; ipdb.set_trace()
        for i in range(depth):
            rel = no.match_outgoing(rel_type=relation_type).next()
            no = rel.end_node()
            nodes.append(no)
            
        return nodes
    

    def asOccurrenceOGM(self):
        """
        Relate it to the OGM implemented in neo4j_reader.
        """
        
        Occurrence = neo.Occurrence.select(neo.graph, self.pk).first()
        return Occurrence


class Occurrence_CSV(models.Model):
    chars = {'l1':15,'l2':15,'l3':25,'l4':100,'l5':60,'l6':70,'l7':100}
    #     id_gbif = models.IntegerField()
    id = models.AutoField(primary_key=True, db_column="id_gbif")
    dataset_id = models.TextField(db_index=False,blank=True, null=True)
    institution_code = models.TextField(db_index=False,blank=True, null=True)
    collection_code = models.TextField(db_index=False,blank=True, null=True)
    catalog_number = models.TextField(db_index=False,blank=True, null=True)
    basis_of_record = models.TextField(db_index=False,blank=True, null=True)
    scientific_name = models.TextField(db_index=True, blank=True, null=True)
    scientific_name_author = models.TextField(db_index=False,blank=True, null=True)
    taxon_id = models.IntegerField(blank=True, null=True)
    kingdom = models.TextField(db_index=True, blank=True, null=True)
    phylum = models.TextField(db_index=True, blank=True, null=True)
    _class = models.TextField(db_index=True, blank=True, null=True)
    _order = models.TextField(db_index=True, blank=True, null=True)
    family = models.TextField(db_index=True, blank=True, null=True)
    genus = models.TextField(db_index=True, blank=True, null=True)
    specific_epithet = models.TextField(db_index=True, blank=True, null=True)
    kingdom_id = models.IntegerField(db_index=True,blank=True, null=True)
    phylum_id = models.IntegerField(db_index=True,blank=True, null=True)
    class_id = models.IntegerField(db_index=True,blank=True, null=True)
    order_id = models.IntegerField(db_index=True,blank=True, null=True)
    family_id = models.IntegerField(db_index=True,blank=True, null=True)
    genus_id = models.IntegerField(db_index=True,blank=True, null=True)
    species_id = models.IntegerField(db_index=True,blank=True, null=True)
    country_code = models.TextField(db_index=False, max_length=7,blank=True, null=True)
    latitude = models.FloatField(db_index=True,blank=True, null=True)
    longitude = models.FloatField(db_index=True,blank=True, null=True)
    year = models.IntegerField(db_index=True,blank=True, null=True)
    month = models.IntegerField(db_index=True,blank=True, null=True)
    event_date = models.DateTimeField(db_index=True,blank=True, null=True)
    elevation_in_meters = models.FloatField(db_index=False,blank=True, null=True)
    depth_in_meters = models.FloatField(db_index=False,blank=True, null=True)
    verbatim_scientific_name = models.TextField(db_index=False,blank=True, null=True)
    taxon_rank = models.TextField(db_index=False,blank=True, null=True)
    verbatim_kingdom = models.TextField(db_index=False,blank=True, null=True)
    verbatim_phylum = models.TextField(db_index=False, blank=True, null=True)
    verbatim_class = models.TextField(db_index=False, blank=True, null=True)
    verbatim_order = models.TextField(db_index=False, blank=True, null=True)
    verbatim_family = models.TextField(db_index=False, blank=True, null=True)
    verbatim_genus = models.TextField(db_index=False, blank=True, null=True)
    verbatim_specific_epithet = models.TextField(db_index=False, blank=True, null=True)
    verbatim_infraspecific_epithet = models.TextField(db_index=False, blank=True, null=True)
    verbatim_latitude = models.TextField(db_index=False,blank=True, null=True)
    verbatim_longitude = models.TextField(db_index=False,blank=True, null=True)
    coordinate_precision = models.FloatField(db_index=False,blank=True, null=True)
    maximum_elevation_in_meters = models.FloatField(db_index=False,blank=True, null=True)
    minimum_elevation_in_meters = models.FloatField(db_index=False,blank=True, null=True)
    elevation_precision = models.FloatField(db_index=False,blank=True, null=True)
    minimum_depth_in_meters = models.FloatField(db_index=False,blank=True, null=True)
    maximum_depth_in_meters = models.FloatField(db_index=False,blank=True, null=True)
    depth_precision = models.FloatField(db_index=False,blank=True, null=True)
    continent_ocean = models.TextField(db_index=False, blank=True, null=True)
    state_province = models.TextField(db_index=False,blank=True, null=True)
    county = models.TextField(db_index=False,blank=True, null=True)
    country = models.TextField(db_index=False,blank=True, null=True)
    recorded_by  = models.TextField(db_index=False,blank=True, null=True)
    locality  = models.TextField(db_index=False,blank=True, null=True)
    verbatim_year = models.TextField(db_index=False,blank=True, null=True)
    verbatim_month = models.TextField(db_index=False,blank=True, null=True)
    day = models.IntegerField(db_index=False,blank=True, null=True)
    verbatim_basis_of_record  = models.TextField(db_index=False,blank=True, null=True)
    identified_by  = models.TextField(db_index=False,blank=True, null=True)
    date_identified = models.TextField(db_index=False,blank=True, null=True)
    created = models.TextField(db_index=False,blank=True, null=True)
    modified = models.TextField(db_index=False,blank=True, null=True)
    
    geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    def __repr__(self):
        """
        String representation of the object 
        """
        a = "<GBIF/: Occurrence %s --%s />" %(self.id,self.scientific_name)
        return a
    
    def getfullDescription(self):
        """
        Retrieves the total description of the fields for the this. registry.
        """
        fields =  self._meta.get_all_field_names()
        cadena = ["<GBIF/: Occurrence %s --%s />\n" %(self.id,self.scientific_name)]
        for f in fields:
            c = "\t < %s: %s />\n" %(f,getattr(self,f))
            cadena.append(c)
        return reduce(lambda x,y : x+y,cadena)
        
        
        
        
    def preprocess(self):
        """
        This function preprocess the entry (originally from a CSV format) and cast it properly into de datatype specified by the model.
        Returns: String
        """
        # build the object as is. respecting the order of the fields.
        # I'm thinking that perhaps using R would have been more easy.
        
        keys = self._meta.get_all_field_names()
        #for k in keys:
            
        
    def validateNfix(self):
        """
        Validates and fix (if possible) the features type given by the list of string features.
        Return True if validation is correct. False otherwise. See log file if it's the case.
        """
        
        fields =  self._meta.get_all_field_names()
        status = []
        for f in fields:
            internalType = self._meta.get_field_by_name(f)[0].get_internal_type()
            if (isinstance(getattr(self,f),str) or isinstance(getattr(self, f), unicode)) and ('Char' not in internalType):
                msg = "Non character type found in: %s but need to be: %s \n Casting feature..." %(getattr(self,f),internalType)
                logger.info(msg)
                #print msg
                if 'Float' in internalType:
                    try:
                        setattr(self,f,float(getattr(self,f)))
                        status.append(True)
                    except:
                        if not getattr(self,f):
                            setattr(self,f,settings.NULL_DATA_FLOAT)
                            msg = "Cannot cast null data to Float type. Value changed to: %s" %settings.NULL_DATA_FLOAT
                            logger.warn(msg)
                            status.append(True)                        
                            #print msg
                elif 'Integer' in internalType:
                    try:
                        setattr(self,f,int(getattr(self,f)))
                        status.append(True)       
                    except:
                        if not getattr(self,f):
                            setattr(self,f,settings.NULL_DATA_INTEGER)
                            msg = "Cannot cast null data to Integer type. Value changed to: %s" %settings.NULL_DATA_INTEGER
                            logger.warn(msg)
                            status.append(True)                        
                            #print msg
                elif 'Date' in internalType:
                    try:
                        datestr = getattr(self,f).replace('\n','')
                        setattr(self,f,dateutil.parser.parse(datestr))
                        status.append(True)
                    except:
                        msg = "Cannot convert string to dateformat for this record: %s" %self.getfullDescription()
                        logger.error(msg)
                        status.append(False)                        
            else:
                msg = "Validation for %s complete" %self
                logger.debug(msg)
                status.append(True)
                #print msg
        # super cool way of making a multidimensional and!        
        #try:
        isvalid = reduce(lambda x,y : x and y, status)
        #except:
        #    logger.error("Something went wrong with this record")
        #    return status
        return isvalid
        

    def insertOccurrence(self):
        """
        Insert occurence in table if validation test is successful
        """
        isvalid = self.validateNfix()
        if isvalid:
            pnt = Point(self.longitude, self.latitude, srid=4326)
            setattr(self,'geom',pnt)
            try:
                self.save()
            except utils.DataError:
                logger.warning("Data did not fit with in the varchars limits.\n Truncating fields instead!")
                fs = self._meta.get_fields()
                chacas = filter(lambda f : f.get_internal_type() == 'TextField',fs)
                # group by size and attribute
                max_len_char = map(lambda c: (c.max_length,c),chacas)
                #import ipdb; ipdb.set_trace()
                for (maxlength,attribute) in max_len_char:
                    original_value = getattr(self, attribute.name)
                    try:
                        truncated = original_value[:maxlength]                    
                    except:
                        truncated = ''
                        logger.warning("Found empty fields")
                    setattr(self, attribute.name, truncated)
                # Here I will truncate the values
                
                #desc = self.getfullDescription()
                #msg = "Data did not fit with in the varchars limits. \n Description: %s" %desc
                #logger.critical(msg)set
         
         
         





class Level(object):
    """
    ..
    Class
    -----
    Auxiliary class for data aggregation.
    
    Basic level class
    
    Attributes
    ----------
    abundance : int
        The abundance (count) values
    levelname : string
        The aggregation of the taxonomic level name (e.g. species,genus,etc)
    level : int
        The id f the level
    Queryset : django.contrib.gis.models.GeoQuerySet
        The Geoqueryset of the mapped objects
    name : string
        Aggregation name at some taxonomic level (e.g. Solanacea).
    
    """
    def __init__(self,LocalQuerySet,n=0, levelname='',level=0, idnum=0):
        self.abundance = 0
        self.levelname = levelname
        self.level = level
        self.QuerySet = LocalQuerySet
        self.name = 'N.A'
        self.id = idnum
        self.children = []
        self.parent = self
        self.visited = False


    ## This is an experiment for making iterable
    def __iter__(self):
        return iter(self.children)



    def traverse(self,parent):
        while not isinstance(self,Occurrence):
            # Because Occurrence has no children
            nodos = map(lambda c : c.createNode(),self.children)
            

                

    def setParent(self):
        for c in self.children:
            c.parent = self
            try:
                c.setParent()
            except:
                return None
            
            
            
    def bindParent(self,writeDB=True,parent_child_name="IS_PARENT_OF"):
        parent = self.parent.createNode()
        this = self.createNode()
        #parent = self.parent.createNode()
        #this = self.createNode()
        
        
        parent_props = {'ab' : self.parent.abundance}
        
        PAR_REL = parent_child_name

        rel = Relationship(parent,PAR_REL,this,**parent_props)
        relations = graph.match(start_node=parent,rel_type=PAR_REL,end_node=this)
        #relations = [r for r in relations]
        try: 
            relations = [r for r in relations]
        except:
            if writeDB:
                graph.create(rel)
        ## This is the aggregate method when the node has an already existing relation. 
        ## It aggregates by summing the abundance average.
        
        if relations:        
            for r in relations:
                r.properties['ab'] += self.parent.abundance
                r.push()
        else:
            if writeDB:
                graph.create(rel)            
        
        
        
        for c in self.children:
            try:
                c.bindParent()
            except:
                return None



    def bindChildren(self,writeDB=True,child_parent_name="IS_A_MEMBER_OF",deepth_limit=8):
        parent = self.parent.createNode(writeDB=writeDB)
        this = self.createNode(writeDB=writeDB)
        parent_props = {'ab' : self.abundance}
        
        
        PAR_REL_INV = child_parent_name
        rel = Relationship(this,PAR_REL_INV,parent,**parent_props)
        relations = graph.match(this,PAR_REL_INV,parent)       
        try: 
            relations = [r for r in relations]
        except:
            if writeDB:
                graph.create(rel)
        ## This is the aggregate method when the node has an already existing relation. 
        ## It aggregates by summing the abundance average.
        
        if relations:        
            for r in relations:
                r.properties['ab'] += self.abundance
                r.push()
        else:
            if writeDB:
                graph.create(rel)            
        
        
        
        for c in self.children:
            try:
                c.bindChildren()
            except:
                return None        

        
        


    def bindExternalNode(self,node,relationship_type="IS_IN"):
        this = self.createNode()
        try:
            properties = {'ab' : self.abundance}
        except:
            properties = {}
        rel = Relationship(this,relationship_type,node,**properties)
        graph.create(rel)
        
        for c in self.children:
            try:
                c.bindExternalNode(node,relationship_type=relationship_type)
            except:
                return None


    def migrateToNeo4J(self,withParent=True,withChildren=True):
        
        
        self.setParent()

        # TO go down and follow links very efficient in traversing
        if withChildren:
            self.bindChildren()
        
        # Also, for an obfuscated recursion reason the order matters. First the children then the parent.    
        if withParent:
            self.bindParent()
        
        return True 
        
    
    def preorder(self):
        ## DEEP FIRST TRAVERSAL
        c = self.getChild().next()
        return c

    def getChild(self):
        # Get the children
        for i in range(len(self.children)+1):
            i += 1
            yield self.children[i-1].next()

        
    def createNode(self,writeDB=False):
        """
        just a wrapper for getNode because it's used in other methods
        """
        x = self.getNode(writeDB=writeDB)
        return x

        
    def getNode(self,writeDB=False):
        """
        This method returns a Node Object based on all the attributes of the Class Level
        """
        
        #Node(Tree.level,name=Tree.name,id=Tree.id,parent_id=Tree.parent_id,abundance=Tree.abundance)    
        ordered_diction = [self.id,self.level,self.levelname,self.name.encode('utf-8')]
        keyword = reduce(lambda a,b : str(a)+'--'+str(b),ordered_diction)
        dictio = {'abundance':self.abundance,'levelname':self.levelname,'name':self.name,'id':self.id,'level':self.level,'keyword':keyword}
        labels = [self.levelname]
        #dictio['keyword':keyword]
        
        node = Node(*labels,**dictio)
        
        node2 = graph.find_one(self.levelname,property_key='keyword',property_value=keyword)
        if node2:
            logger.debug("Node exists. \n Aggregating abundance values.")
            #node2['abundance'] += 1
            #node2.push()
            return node2
        else:
            if writeDB:
                graph.create(node)
            return node
    
    
    def getChildrenNodes(self):
        """
        Get the nodes of the children (Children in NEo4J form)
        """
        nodos = map(lambda c : c.createNode(),self.children)
        return nodos
    
    
    
    
    
# def bindNode(Tree,node=False):
#     child = Node(Tree.level,name=Tree.name,id=Tree.id,parent_id=Tree.parent_id,abundance=Tree.abundance)    
#     if node:
#         relation = Relationship(child, "IS_MEMBER_OF", node)  
#         return relation  
#     else:
#         return child

class Individual(Level):
    """
    ..
    Individual
    ==========
    ..
    This is the individual (occurrence) class definition.
    It's just a wrapper of the gbif.model.Occurrence
    ..
    Parameters
    ----------
    localQuerySet : gbif.models.Occurrence.Geoqueryset
    species_metadata : dictionary
        The dictionary obtained from the GeoquerySet annotation
        See also
        --------
        
    
    Attributes
    ----------
    occurrences : gbif.models.Level.QuerySet
        The QuerySet of the filtered at occurrence level
    geometry : geometry
        WKB representation
    """
    
    def __init__(self,localQuerySet,occurrence_metadata):
        """
        ..
        Basic constructor       
        """
        Level.__init__(self,localQuerySet,level=8,levelname='Occurrence')
        self.occurrences = 'N.A.'
        self.geometry = 'N.A.'
        self.setInfo(occurrence_metadata)


    def setInfo(self,dict_from_queryset_annotation):
        """
        ..
        Given a QuerySet it fills all the occurrences and performs the aggregation.
        
        Returns
        -------
        nothing :
            It sets the class' attributes.
        """
        try:
            ok = dict_from_queryset_annotation
            self.abundance = ok['ab']
            self.name = ok['name']
            self.id = ok['pk']
            self.geometry = ok['points']
            self.occurrences = self.QuerySet.filter(pk=self.id)
            self.children = self.occurrences
        except:
            logger.error("This is not a GBIF Query Set")
            return False

    
    def setNeighbors(self,list_occurrences):
        """
        A list of occurrences 
        """
        #self.occurrences = list_occurrences
        pass
    

    def createNode(self,writeDB=True):
        yo = self.children.get()
        #import ipdb; ipdb.set_trace()
        nodoyo = yo.createNode(writeDB=writeDB)
        return nodoyo

    
    def __repr__(self):
        
        cad =  u'<gbif:Occurrence> Id = %s \n \t <gbif:Name> %s </gbif:Name>\n \t \t <gbif:n_occurrences> %s </gbif:n_occurrences>\n  </gbif:Occurrence>\n' %(self.id,self.name,self.abundance)
        return cad.encode('utf-8')
    
    
    def __str__(self):
        return self.__repr__()



class Specie(Level):
    """
    ..
    Class
    =====
    ..
    This is the Species class definition
    ..
    Parameters
    ----------
    localQuerySet : gbif.models.Occurrence.Geoqueryset
    species_metadata : dictionary
        The dictionary obtained from the GeoquerySet annotation
        See also
        --------
        
    
    Attributes
    ----------
    occurrences : gbif.models.Level.QuerySet
        The QuerySet of the filtered at occurrence level
    geometry : geometry
        WKB representation
    """
    
    def __init__(self,localQuerySet,species_metadata):
        """
        ..
        Basic constructor       
        """
        Level.__init__(self,localQuerySet,level=7,levelname='Specie')
        self.occurrences = []
        self.geometry = 'N.A.'
        self.setInfo(species_metadata)


    def setInfo(self,dict_from_queryset_annotation):
        """
        ..
        Given a QuerySet it fills all the occurrences and performs the aggregation.
        
        Returns
        -------
        nothing :
            It sets the class' attributes.
        """
        try:
            ok = dict_from_queryset_annotation
            self.abundance = ok['ab']
            self.name = ok['name']
            self.id = ok['species_id']
            self.geometry = ok['points']
        except:
            logger.error('This is not a metadata object for species')
            return False            
            
        occurrences = self.getOccurrenceMetadata()
        for occurrence_metadata in occurrences:
            self.occurrences.append(Individual(self.QuerySet,occurrence_metadata))
        self.abundance = self.QuerySet.filter(species_id=self.id).distinct('pk').count()
        self.children = self.occurrences
        return True


    
    def getOccurrenceMetadata(self):
        """
        Returns metadata for all species at a specific genus
        """
        occurrence = self.QuerySet.filter(species_id=self.id).values('pk').annotate(points=Collect('geom'),ab=Count('pk'),name=Min('scientific_name'))
        return occurrence
    
    def setNeighbors(self,list_occurrences):
        """
        A list of occurrences 
        """
        #self.occurrences = list_occurrences
        pass
    
    
    def __repr__(self):
        
        cad =  u'<gbif:Specie> Id = %s \n \t <gbif:Name> %s </gbif:Name>\n \t \t <gbif:n_occurrences> %s </gbif:n_occurrences>\n  </gbif:Specie>\n' %(self.id,self.name,self.abundance)
        return cad.encode('utf-8')
    
    
    def __str__(self):
        return self.__repr__()


class Genus(Level):
    """
    ..
    Genus
    =====
    ..
    This is the Genus class definition
    ..
    Parameters
    ----------
    Level : See also Level
    
    Attributes
    ----------
    species : gbif.models.Level.QuerySet
        The QuerySet of the filtered at occurrence level
    geometry : geometry
        WKB representation    

    """
    def __init__(self,localQuerySet,genus_metadata):
        """
        Basic constructor
        """
        Level.__init__(self,localQuerySet,level=6,levelname='Genus')
        self.species = []
        self.geometry = 'N.A.'
        self.setInfo(genus_metadata)      
    
    
    def getSpeciesMetadata(self):
        """
        Returns metadata for all species at a specific genus
        """
        species = self.QuerySet.filter(genus_id=self.id).values('species_id').annotate(points=Collect('geom'),ab=Count('species_id'),name=Min('scientific_name'))
        return species
    
    
    def setInfo(self,genus_metadata):
        """
        Set the data for genus as a list of species.
        """
        try:
            self.id = genus_metadata['genus_id']
            self.name = genus_metadata['name']
            self.geometry = genus_metadata['points']
            self.abundance = genus_metadata['ab']
        except:
            logger.error('This is not a metadata object for genus')
            return False
        species = self.getSpeciesMetadata()
        for specie_metadata in species:
            self.species.append(Specie(self.QuerySet,specie_metadata))
        #self.abundance = self.QuerySet.filter(genus_id=self.id).distinct('species_id').count()
        self.abundance = self.QuerySet.filter(genus_id=self.id).distinct('pk').count()
        self.children = self.species
        return True
    
    def getChildrenNames(self):
        """
        Returns the list of species
        """
        return map(lambda bicho : bicho['name'],self.species)
        
    #===========================================================================
    # def __repr__(self):
    #     head = u'<gbif.Genus: Id = %s > %s \n' %(self.id,self.name)
    #     body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.species))
    #     feet = u'\t <N.Species> %s </> \n </gbif.Genus>' %self.abundance
    #     cad = head.encode('utf-8') + body+ feet.encode('utf-8')
    #     return cad
    #===========================================================================

    def __repr__(self):
        head = u'<gbif:genus> \n <gbif:genus_id> %s </gbif:genus_id>\n \t <gbif:name> %s </gbif:name>\n' %(self.id,self.name)
        body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.species))
        feet = u'\t <gbif:n_especies> %s </gbif:n_especies> \n </gbif.genus>' %self.abundance
        cad = head.encode('utf-8') + body+ feet.encode('utf-8')
        return cad

 
    def __str__(self):
        return self.__repr__()
     
#id_gbif integer, kingdom character varying, _order character varying, _class character varying, family character varying, scientific_name character varying, kingdom_id integer, phylum_id integer, order_id integer, class_id integer, family_id integer, species_id integer, n_occurs bigint, geom geometry) AS

class Family(Level):
    """
    Basic class for Family Level
    """
    def __init__(self,localQuerySet,family_metadata):
        """
        Basic constructor
        """
        Level.__init__(self,localQuerySet,level=5,levelname='Family')
        self.genera = []
        self.geometry = 'N.A.'
        self.setInfo(family_metadata)  
        
    def getGenusMetadata(self):
        """
        Returns metadata for all genus of a specific family
        """
        genera = self.QuerySet.filter(family_id=self.id).values('genus_id').annotate(points=Collect('geom'),ab=Count('genus_id'),name=Min('genus'))
        return genera
    
    def setInfo(self,family_metadata):
        """
        Set family features as a list of f.
        """
        try:
            self.id = family_metadata['family_id']
            self.name = family_metadata['name']
            self.geometry = family_metadata['points']
            self.abundance = family_metadata['ab']
        except:
            logger.error('This is not a metadata object for family')
            return False
        genera = self.getGenusMetadata()
        for genus_metadata in genera:
            self.genera.append(Genus(self.QuerySet,genus_metadata))
        #self.abundance = self.QuerySet.filter(family_id=self.id).distinct('genus_id').count()
        self.abundance = self.QuerySet.filter(family_id=self.id).distinct('pk').count()
        self.children = self.genera
        return True
    
    def __repr__(self):
        head = u'<gbif.Family: Id = %s > %s \n' %(self.id,self.name)
        body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.genera))
        feet = u'\t <N.Genera> %s </> \n </gbif.Family>' %self.abundance
        return head.encode('utf-8') + body + feet.encode('utf-8')
    
    
class Order(Level):
    """
    Basic class for the Order Level
    """
    def __init__(self,localQuerySet,order_metadata):
        """
        Basic constructor
        """
        Level.__init__(self,localQuerySet,level=4,levelname='Order')
        self.families = []
        self.geometry = 'N.A.'
        self.setInfo(order_metadata)  
        
    def getFamiliesMetadata(self):
        """
        Returns metadata for all families of a specific class
        """
        families = self.QuerySet.filter(order_id=self.id).values('family_id').annotate(points=Collect('geom'),ab=Count('family_id'),name=Min('family'))
        return families
    
    def setInfo(self,order_metadata):
        """
        Set family features as a list of f.
        """
        try:
            logger.debug('\t \t'+str(order_metadata))
            self.id = order_metadata['order_id']
            self.name = order_metadata['name']
            self.geometry = order_metadata['points']
            self.abundance = order_metadata['ab']
        except:
            logger.error('This is not a metadata object for Order')
            return False
        families = self.getFamiliesMetadata()
        for family_metadata in families:
            self.families.append(Family(self.QuerySet,family_metadata))
        #self.abundance = self.QuerySet.filter(order_id=self.id).distinct('family_id').count()
        self.abundance = self.QuerySet.filter(order_id=self.id).distinct('pk').count()
        self.children = self.families
        return True
    
    def __repr__(self):
        head = u'<gbif.Order: Id = %s > %s \n' %(self.id,self.name)
        body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.families))
        feet = u'\t <N.Families> %s </> \n </gbif.Order>' %self.abundance
        return head.encode('utf-8') + body + feet.encode('utf-8')
        

class Class(Level):
    """
    Basic class for the Class Level
    """
    def __init__(self,localQuerySet,class_metadata):
        """
        Basic constructor
        """
        Level.__init__(self,localQuerySet,level=3,levelname='Class')
        self.orders = []
        self.geometry = 'N.A.'
        self.setInfo(class_metadata)  
        
    def getOrdersMetadata(self):
        """
        Returns metadata for all classes of a specific order
        """
        orders = self.QuerySet.filter(class_id=self.id).values('order_id').annotate(points=Collect('geom'),ab=Count('order_id'),name=Min('_order'))
        return orders    

    def setInfo(self,class_metadata):
        """
        Set family features as a list of f.
        """
        try:
            logger.debug('\t'+str(class_metadata))
            self.id = class_metadata['class_id']
            self.name = class_metadata['name']
            self.geometry = class_metadata['points']
            self.abundance = class_metadata['ab']
        except:
            logger.error('This is not a metadata object for Class')
            return False
        orders = self.getOrdersMetadata()
        for order_metadata in orders:
            self.orders.append(Order(self.QuerySet,order_metadata))
        #self.abundance = self.QuerySet.filter(class_id=self.id).distinct('order_id').count()
        self.abundance = self.QuerySet.filter(class_id=self.id).distinct('pk').count()
        self.children = self.orders
        return True
    
    def __repr__(self):
        head = u'<gbif.Class: Id = %s > %s \n' %(self.id,self.name)
        body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.orders))
        feet = u'\t <N.Orders> %s </> \n </gbif.Class>' %self.abundance
        return head.encode('utf-8') + body + feet.encode('utf-8')


class Phylum(Level):
    """
    Basic class for the Phylum Level 
    """
    def __init__(self,localQuerySet,phylum_metadata):
        """
        Basic constructor
        """
        Level.__init__(self,localQuerySet,level=2,levelname='Phylum')
        self.classes = []
        self.geometry = 'N.A.'
        self.setInfo(phylum_metadata)  
        
    def getClassesMetadata(self):
        """
        Returns metadata for all classes of a specific order
        """
        classes = self.QuerySet.filter(phylum_id=self.id).values('class_id').annotate(points=Collect('geom'),ab=Count('class_id'),name=Min('_class'))
        return classes    

    def setInfo(self,phylum_metadata):
        """
        Set family features as a list of f.
        """
        try:
            logger.debug(phylum_metadata)
            self.id = phylum_metadata['phylum_id']
            self.name = phylum_metadata['name']
            self.geometry = phylum_metadata['points']
            self.abundance = phylum_metadata['ab']
        except:
            logger.error('This is not a metadata object for Phylum')
            return False
        classes = self.getClassesMetadata()
        for class_metadata in classes:
            self.classes.append(Class(self.QuerySet,class_metadata))
        #self.abundance = self.QuerySet.filter(phylum_id=self.id).distinct('class_id').count()
        self.abundance = self.QuerySet.filter(phylum_id=self.id).distinct('pk').count()
        self.children = self.classes
        return True
    
    def __repr__(self):
        head = u'<gbif.Phylum: Id = %s > %s \n' %(self.id,self.name)
        body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.classes))
        feet = u'\t <N.Classes> %s </> \n </gbif.Phylum>' %self.abundance
        return head.encode('utf-8') + body + feet.encode('utf-8')    
 
    

class Kingdom(Level):
    """
    Basic class for Kingdom Level
    """
    
    def __init__(self,localQuerySet,kingdom_metadata):
        """
        Basic constructor
        """
        Level.__init__(self,localQuerySet,level=1,levelname='Kingdom')
        self.phyla = []
        self.geometry = 'N.A.'
        self.setInfo(kingdom_metadata)  
        
    def getPhylaMetadata(self):
        """
        Returns metadata for all phyla of a specific kingdom
        """
        phyla = self.QuerySet.filter(kingdom_id=self.id).values('phylum_id').annotate(points=Collect('geom'),ab=Count('phylum_id'),name=Min('phylum'))
        return phyla    

    def setInfo(self,kingdom_metadata):
        """
        Set kingdom features as a list of features.
        """
        try:
            logger.debug(kingdom_metadata)
            self.id = kingdom_metadata['kingdom_id']
            self.name = kingdom_metadata['name']
            self.geometry = kingdom_metadata['points']
            self.abundance = kingdom_metadata['ab']
        except:
            logger.error('This is not a metadata object for Kingdom')
            return False
        phyla = self.getPhylaMetadata()
        for phylum_metadata in phyla:
            self.phyla.append(Phylum(self.QuerySet,phylum_metadata))
        #self.abundance = self.QuerySet.filter(kingdom_id=self.id).distinct('phylum_id').count()
        self.abundance = self.QuerySet.filter(kingdom_id=self.id).distinct('pk').count()
        self.children = self.phyla
        return True
    
    def __repr__(self):
        head = u'<gbif.Kingdom: Id = %s > %s \n' %(self.id,self.name)
        body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.phyla))
        feet = u'\t <N.Phyla> %s </> \n </gbif.Kingdom>' %self.abundance
        return head.encode('utf-8') + body + feet.encode('utf-8')     
 

class Root(Level):
    """
    Basic class for Kingdom Level
    """
    
    def __init__(self,localQuerySet,idnum=-999):
        """
        Basic constructor
        """
        Level.__init__(self,localQuerySet,level=0,levelname='Root',idnum=idnum)
        self.kingdoms = []
        self.geometry = 'N.A.'
        self.setInfo()
        self.id = idnum

        
    def getKingdomMetadata(self):
        """
        Returns metadata for all phyla of a specific kingdom
        """
        kingdoms = self.QuerySet.filter().values('kingdom_id').annotate(points=Collect('geom'),ab=Count('kingdom_id'),name=Min('kingdom'))
        return kingdoms    

    def setInfo(self):
        """
        Set kingdom features as a list of features.
        """
        try:
            logger.debug("Reconstructing Tree")
            self.id = 0
            self.name = 'LUCA'
            self.geometry = 'all_points'
            self.abundance = 'NA'
        except:
            logger.error('This is not a metadata object for Kingdom')
            return False
        kingdoms = self.getKingdomMetadata()
        for kingdom_metadata in kingdoms:
            self.kingdoms.append(Kingdom(self.QuerySet,kingdom_metadata))
        metadata = self.QuerySet.aggregate(points=Collect('geom'),ab=Count('kingdom_id'))
        self.children = self.kingdoms
   
        self.abundance = metadata['ab']
        self.geometry = metadata['points']
                
        return True


     
    def bindParent(self,writeDB=True,parent_child_name="IS_PARENT_OF"):
        parent = self.createNode()
        this = self.createNode()
        #parent = self.parent.createNode()
        #this = self.createNode()
        parent_props = {'ab' : self.parent.abundance}
        
        PAR_REL = parent_child_name

        rel = Relationship(parent,PAR_REL,this,**parent_props)
        relations = graph.match(start_node=parent,rel_type=PAR_REL,end_node=this)
        #relations = [r for r in relations]
        try: 
            relations = [r for r in relations]
        except:
            if writeDB:
                try:
                    graph.create(rel)
                except:
                    return None
        ## This is the aggregate method when the node has an already existing relation. 
        ## It aggregates by summing the abundance average.
        
        if relations:        
            for r in relations:
                r.properties['ab'] += self.parent.abundance
                r.push()
        else:
            if writeDB:
                graph.create(rel)                    
        for c in self.children:
            try:
                c.bindParent()
            except:
                return None

    def bindChildren(self,writeDB=True,child_parent_name="IS_A_MEMBER_OF",deepth_limit=8):
        parent = self.createNode(writeDB=writeDB)
        this = self.createNode(writeDB=writeDB)
        parent_props = {'ab' : self.parent.abundance}
        
        
        PAR_REL_INV = child_parent_name
        rel = Relationship(this,PAR_REL_INV,parent,**parent_props)
        relations = graph.match(this,PAR_REL_INV,parent)       
        try: 
            relations = [r for r in relations]
        except:
            if writeDB:
                graph.create(rel)
        ## This is the aggregate method when the node has an already existing relation. 
        ## It aggregates by summing the abundance average.
        
        if relations:        
            for r in relations:
                r.properties['ab'] += self.abundance
                r.push()
        else:
            if writeDB:
                graph.create(rel)            
        
        
        
        for c in self.children:
            try:
                c.bindChildren()
            except:
                return None        





    
    def __repr__(self):
    
        head = u'<gbif.Root: Id = %s > %s \n' %(self.id,self.name)
        try:    
            body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.kingdoms))
        except:
            body = u' EMPTY TAXONOMY '
        
        feet = u'\t <N.Kingdom> %s </> \n </gbif.Root>' %self.abundance
        return head.encode('utf-8') + body + feet.encode('utf-8')    






    