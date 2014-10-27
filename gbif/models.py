#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
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

logger_ins = logging.getLogger('biospatial.gbif.insertion')


from django.forms import ModelForm
# Model for GBIF as given by Raúl Jimenez



class Occurrence_test(models.Model):
    chars = {'l1':15,'l2':15,'l3':25,'l4':100,'l5':60,'l6':70,'l7':100}
    id = models.AutoField(primary_key=True, db_column="id_gbif")
#     id_gbif = models.IntegerField()
    dataset_id = models.CharField(db_index=True, max_length=chars['l5'],blank=True, null=True)
    institution_code = models.CharField(db_index=True, max_length=chars['l1'],blank=True, null=True)
    collection_code = models.CharField(db_index=True, max_length=chars['l1'],blank=True, null=True)
    catalog_number = models.CharField(db_index=True, max_length=chars['l2'],blank=True, null=True)
    basis_of_record = models.CharField(db_index=True, max_length=chars['l2'],blank=True, null=True)
    scientific_name = models.CharField(db_index=True, max_length=chars['l7'],blank=True, null=True)
    scientific_name_author = models.CharField(db_index=True, max_length=chars['l4'],blank=True, null=True)
    taxon_id = models.IntegerField(blank=True, null=True)
    kingdom = models.CharField(db_index=True, max_length=chars['l2'],blank=True, null=True)
    phylum = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    _class = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    _order = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    family = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    genus = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    specific_epithet = models.CharField(db_index=True, max_length=chars['l4'],blank=True, null=True)
    kingdom_id = models.IntegerField(db_index=True,blank=True, null=True)
    phylum_id = models.IntegerField(db_index=True,blank=True, null=True)
    class_id = models.IntegerField(db_index=True,blank=True, null=True)
    order_id = models.IntegerField(db_index=True,blank=True, null=True)
    family_id = models.IntegerField(db_index=True,blank=True, null=True)
    genus_id = models.IntegerField(db_index=True,blank=True, null=True)
    species_id = models.IntegerField(db_index=True,blank=True, null=True)
    country_code = models.CharField(db_index=True, max_length=7,blank=True, null=True)
    latitude = models.FloatField(db_index=True,blank=True, null=True)
    longitude = models.FloatField(db_index=True,blank=True, null=True)
    year = models.IntegerField(db_index=True,blank=True, null=True)
    month = models.IntegerField(db_index=True,blank=True, null=True)
    event_date = models.DateTimeField(db_index=True,blank=True, null=True)
    elevation_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    depth_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    verbatim_scientific_name = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    taxon_rank = models.IntegerField(db_index=True,blank=True, null=True)
    verbatim_kingdom = models.CharField(db_index=True,max_length=chars['l3'],blank=True, null=True)
    verbatim_phylum = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    verbatim_class = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    verbatim_order = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    verbatim_family = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    verbatim_genus = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    verbatim_specific_epithet = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    verbatim_infraspecific_epithet = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    verbatim_latitude = models.FloatField(db_index=True,blank=True, null=True)
    verbatim_longitude = models.FloatField(db_index=True,blank=True, null=True)
    coordinate_precision = models.FloatField(db_index=True,blank=True, null=True)
    maximum_elevation_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    minimum_elevation_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    elevation_precision = models.FloatField(db_index=True,blank=True, null=True)
    minimum_depth_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    maximum_depth_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    depth_precision = models.FloatField(db_index=True,blank=True, null=True)
    continent_ocean = models.FloatField(db_index=True,blank=True, null=True)
    state_province = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    county = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    country = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    recorded_by  = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    locality  = models.CharField(db_index=True,max_length=chars['l6'],blank=True, null=True)
    verbatim_year = models.IntegerField(db_index=True,blank=True, null=True)
    verbatim_month = models.IntegerField(db_index=True,blank=True, null=True)
    day = models.IntegerField(db_index=True,blank=True, null=True)
    verbatim_basis_of_record  = models.CharField(db_index=True,max_length=chars['l4'],blank=True, null=True)
    identified_by  = models.CharField(db_index=True,max_length=chars['l6'],blank=True, null=True)
    date_identified = models.DateTimeField(db_index=True,blank=True, null=True)
    created = models.DateTimeField(db_index=True,blank=True, null=True)
    modified = models.DateTimeField(db_index=True,blank=True, null=True)
    geom = models.PointField()
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
            if isinstance(getattr(self,f),str) and ('Char' not in internalType):
                msg = "Non character type found in: %s but need to be: %s \n Casting feature..." %(getattr(self,f),internalType)
                logger_ins.info(msg)
                #print msg
                if 'Float' in internalType:
                    try:
                        setattr(self,f,float(getattr(self,f)))
                        status.append(True)
                    except:
                        if not getattr(self,f):
                            setattr(self,f,settings.NULL_DATA_FLOAT)
                            msg = "Cannot cast null data to Float type. Value changed to: %s" %settings.NULL_DATA_FLOAT
                            logger_ins.warn(msg)
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
                            logger_ins.warn(msg)
                            status.append(True)                        
                            #print msg
                elif 'Date' in internalType:
                    try:
                        datestr = getattr(self,f).replace('\n','')
                        setattr(self,f,dateutil.parser.parse(datestr))
                        status.append(True)
                    except:
                        msg = "Cannot convert string to dateformat for this record: %s" %self.getfullDescription()
                        logger_ins.error(msg)
                        status.append(False)                        
            else:
                msg = "Validation for %s complete" %self
                logger_ins.debug(msg)
                #print msg
        # super cool way of making a multidimensional and!        
        isvalid = reduce(lambda x,y : x and y, status)
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
                desc = self.getfullDescription()
                msg = "Data did not fit with in the varchars limits. \n Description: %s" %desc
                logger_ins.critical(msg)
         
         
         
class Occurrence(models.Model):
    chars = {'l1':15,'l2':15,'l3':25,'l4':100,'l5':60,'l6':70,'l7':100}
    id = models.AutoField(primary_key=True, db_column="id_gbif")
#     id_gbif = models.IntegerField()
    dataset_id = models.CharField(db_index=True, max_length=chars['l5'],blank=True, null=True)
    institution_code = models.CharField(db_index=True, max_length=chars['l1'],blank=True, null=True)
    collection_code = models.CharField(db_index=True, max_length=chars['l1'],blank=True, null=True)
    catalog_number = models.CharField(db_index=True, max_length=chars['l2'],blank=True, null=True)
    basis_of_record = models.CharField(db_index=True, max_length=chars['l2'],blank=True, null=True)
    scientific_name = models.CharField(db_index=True, max_length=chars['l7'],blank=True, null=True)
    #scientific_name_author = models.CharField(db_index=True, max_length=chars['l4'],blank=True, null=True)
    #taxon_id = models.IntegerField(blank=True, null=True)
    kingdom = models.CharField(db_index=True, max_length=chars['l2'],blank=True, null=True)
    phylum = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    _class = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    _order = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    family = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    genus = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    specific_epithet = models.CharField(db_index=True, max_length=chars['l4'],blank=True, null=True)
    kingdom_id = models.IntegerField(db_index=True,blank=True, null=True)
    phylum_id = models.IntegerField(db_index=True,blank=True, null=True)
    class_id = models.IntegerField(db_index=True,blank=True, null=True)
    order_id = models.IntegerField(db_index=True,blank=True, null=True)
    family_id = models.IntegerField(db_index=True,blank=True, null=True)
    genus_id = models.IntegerField(db_index=True,blank=True, null=True)
    species_id = models.IntegerField(db_index=True,blank=True, null=True)
    country_code = models.CharField(db_index=True, max_length=7,blank=True, null=True)
    latitude = models.FloatField(db_index=True,blank=True, null=True)
    longitude = models.FloatField(db_index=True,blank=True, null=True)
    year = models.IntegerField(db_index=True,blank=True, null=True)
    month = models.IntegerField(db_index=True,blank=True, null=True)
    event_date = models.DateTimeField(db_index=True,blank=True, null=True)
    #elevation_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #depth_in_meters = models.FloatField(db_index=True,blank=True, null=True)
    #verbatim_scientific_name = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    #taxon_rank = models.IntegerField(db_index=True,blank=True, null=True)
    #verbatim_kingdom = models.CharField(db_index=True,max_length=chars['l3'],blank=True, null=True)
    #verbatim_phylum = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    #verbatim_class = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    #verbatim_order = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    #verbatim_genus = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    #verbatim_family = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    #verbatim_specific_epithet = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
    #verbatim_infraspecific_epithet = models.CharField(db_index=True, max_length=chars['l3'],blank=True, null=True)
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
    state_province = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    county = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    country = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    #recorded_by  = models.CharField(db_index=True,max_length=chars['l5'],blank=True, null=True)
    #locality  = models.CharField(db_index=True,max_length=chars['l6'],blank=True, null=True)
    #verbatim_month = models.IntegerField(db_index=True,blank=True, null=True)
    #verbatim_year = models.IntegerField(db_index=True,blank=True, null=True)
    #day = models.IntegerField(db_index=True,blank=True, null=True)
    #verbatim_basis_of_record  = models.CharField(db_index=True,max_length=chars['l4'],blank=True, null=True)
    #date_identified = models.DateTimeField(db_index=True,blank=True, null=True)
    #identified_by  = models.CharField(db_index=True,max_length=chars['l6'],blank=True, null=True)
    #created = models.DateTimeField(db_index=True,blank=True, null=True)
    geom = models.PointField()
    #modified = models.DateTimeField(db_index=True,blank=True, null=True)
    objects = models.GeoManager()
    
    class Meta:
        managed = False
        db_table = "gbif_occurrence"
 
    def __unicode__(self):
        return u'<GBIF Occurrence: %s  scientific_name: %s>\n Kingdom: %s \n,\t Phylum: %s \n,\t \t Order: %s,\n \t \t \t Class: %s, \n \t \t \t \t Family: %s, \n \t \t \t \t \t Location: %s<\GBIF Occurrence>' %(self.id,self.scientific_name,self.kingdom,self.phylum,self._order,self._class,self.family,self.geom)
        
                