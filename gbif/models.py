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
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min


logger = logging.getLogger('biospatial.gbif')


from django.forms import ModelForm
# Model for GBIF as given by Raúl Jimenez


class Occurrence_CSV_Verbatim(models.Model):
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
    id_gf = models.IntegerField(blank=True,null=True)
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
 



#No se, hara algo el puto migartions


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
         
         
         



class Level:
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
    def __init__(self,LocalQuerySet,n=0,levelname='',level=0):
        self.abundance = 0
        self.levelname = levelname
        self.level = level
        self.QuerySet = LocalQuerySet
        self.name = 'N.A'
        self.id = 'N.A'


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
        self.occurrences = 'N.A.'
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
            self.occurrences = self.QuerySet.filter(species_id=self.id)
        except:
            logger.error("This is not a GBIF Query Set")
            return False

    
    def setNeighbors(self,list_occurrences):
        """
        A list of occurrences 
        """
        #self.occurrences = list_occurrences
        pass
    
    
    def __repr__(self):
        
        cad =  u'<gbif:Specie> Id = %s </gbif:Specie>\n \t <gbif:Name> %s </gbif:Name>\n \t \t <gbif:n_occurrences> %s </gbif:n_occurrences>\n' %(self.id,self.name,self.abundance)
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
        self.abundance = self.QuerySet.filter(genus_id=self.id).distinct('species_id').count()
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
        self.abundance = self.QuerySet.filter(family_id=self.id).distinct('genus_id').count()
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
        self.abundance = self.QuerySet.filter(order_id=self.id).distinct('family_id').count()
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
        self.abundance = self.QuerySet.filter(class_id=self.id).distinct('order_id').count()
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
        self.abundance = self.QuerySet.filter(phylum_id=self.id).distinct('class_id').count()
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
        self.abundance = self.QuerySet.filter(kingdom_id=self.id).distinct('phylum_id').count()
        return True
    
    def __repr__(self):
        head = u'<gbif.Kingdom: Id = %s > %s \n' %(self.id,self.name)
        body = str(reduce(lambda sp1,sp2: str(sp1)+str(sp2)+'\n',self.phyla))
        feet = u'\t <N.Phyla> %s </> \n </gbif.Kingdom>' %self.abundance
        return head.encode('utf-8') + body + feet.encode('utf-8')     
 
    