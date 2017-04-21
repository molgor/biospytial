#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Populate
=============
.. note::
    This module has functions that works for populating the POSTGIS database.
    Currently the two implemented methods are via GBIF API or with a CSV downloaded file.
    Both works only with the GBIF API and it's current field names.
    created on: 11 Jan 2016 at 20:14:49 by juan

"""
from posix import fpathconf
#from django.template.context_processors import request
from datetime import datetime

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2016, JEM"
__license__ = "GPL"
__version__ = "2.0.0"
__mantainer__ = "juan"
__email__ ="j.escamillamolgora@lancaster.ac.uk"
__status__ = "Prototype"



"""
Occurrence: Provides access to occurrence information crawled 
and indexed by GBIF and search services to do real time paged
search and asynchronous download services to do large batch 
downloads.
"""


from django.test import TestCase
from django.contrib.gis.geos import Point

import urllib
import urllib2
import logging
import json
import requests
import csv
import io

URLBASE = "http://api.gbif.org/v1/"
URLOCCURRENCE = URLBASE+"occurrence/search"

logger = logging.getLogger('biospytial.gbif.taxonomy')


def getOccurrencesDriver(WKT,url=URLOCCURRENCE):
    """
    Get occurrences from the GBIF API
    """
    values = {'geometry' : WKT}
    data = urllib.urlencode(values)
    fullurl = url+'?'+data
    response = urllib2.urlopen(fullurl)
   # dic = json.decoder(response.readlines())
    fp = response.fp
    return fp
    #ocrs = json.load(fp)
    
    #return ocrs['results']
    #except:
     #   logger.error("Error in URL: %s"%url)
      #  return fullurl


def getOccurrenceN(WKT,url=URLOCCURRENCE,offset=0):
    values = {'geometry' : WKT,'offset' : offset}
    r = requests.get(url,params=values)
    return r




def curateOccurrences(response_from_getOccurence):
    """
    Take only results
    """
    r = response_from_getOccurence
    j = r.json()
    return j['results']

def webGBIFtoOccurence(json_gbif):
    from gbif.models import Occurrence
    # Create the dictionary
    ## Uncoment here if you need more records
    
    try:
        occ = Occurrence(
        id = json_gbif['gbifID'],
        #dataset_id = json_gbif['datasetKey'],
        #institution_code = json_gbif['institutionCode'],
        #collection_code = json_gbif['collectionCode'],
        #catalog_number = json_gbif['catalogNumber'],
        #basis_of_record = json_gbif['basisOfRecord'],
        
        
        kingdom = json_gbif['kingdom'],
        phylum = json_gbif['phylum'],
        _class = json_gbif['class'],
        _order = json_gbif['order'],
        family = json_gbif['family'],
        genus = json_gbif['genus'],
        scientific_name = json_gbif['scientificName'],
        specific_epithet = json_gbif['specificEpithet'],
       
        kingdom_id = json_gbif['kingdomKey'],
        phylum_id = json_gbif['phylumKey'],
        class_id = json_gbif['classKey'],
        order_id = json_gbif['orderKey'],
        family_id = json_gbif['familyKey'],
        genus_id = json_gbif['genusKey'],
        species_id = json_gbif['speciesKey'],
        
        #country_code = json_gbif['countryCode'],
        latitude = json_gbif['decimalLatitude'],
        longitude = json_gbif['decimalLongitude'],
        
        year = json_gbif['year'],
        month = json_gbif['month'],
        day = json_gbif['day'],
        event_date = json_gbif['eventDate'],
        #taxon_rank = json_gbif['taxonRank'],
        #modified = json_gbif['modified'],
        #recorded_by  = json_gbif['recordedBy'],
        #country = json_gbif['country'],
        
        #locality  = json_gbif['verbatimLocality'],
        
        #date_identified = datetime.date(year=int(json_gbif['year']),month=int(json_gbif['month']),day=int(json_gbif['day'])), 
        #json_gbif['dateIdentified'],
        
        geom = Point(float(json_gbif['decimalLongitude']),float(json_gbif['decimalLatitude']), srid=4326),
        
        #taxon_id = json_gbif['taxonKey']
        )
        return occ
    except KeyError as e:
        logger.warn("Missing data in field %s:"%e)


def getAllOccurrences(WKT,url=URLOCCURRENCE,offset=0,safeinDB=False,maxdepth=0):
    """
    Get all Occurrences from the occurrence/search API
    If maxdepth == 0 it will continue until the server throws the 'endOfRecords'
    """
    list_occurrences = []
    r = getOccurrenceN(WKT, url=url, offset=offset)
    j = r.json()
    #while (not j['endOfRecords']) or ((offset < maxdepth) and (maxdepth > 0)) :
    while (not j['endOfRecords']) and ((offset <= maxdepth) or (maxdepth == 0)):    
        t = curateOccurrences(r)
        objs = map(lambda j : webGBIFtoOccurence(j),t)
        if safeinDB:
            try: 
                map(lambda oc : oc.save(),objs)
            except:
                logger.warning("No data, skiping")
            logger.debug("Writen in Database")
        else:
            list_occurrences.append(objs)
        offset += 1
        r = getOccurrenceN(WKT, url=url, offset=offset)
        j = r.json()
        logger.debug("Retrieving information from the server. Offset:%s", offset)
    return list_occurrences
# Create your tests here.



def CSVLoad(csvDictReader):
    """
    Loads a CSV file obtained by GBIF into biospytial Occurrence objects
    """
    from gbif.models import Occurrence_CSV_4insert as Occurrence
    l = []
    for i in range(100):
        t = csvDictReader.next()
        dictoccur = {#'gbifid':t['gbifid'],
        'dataset_id' : t['datasetkey'],
        #'occurrenceid' : t['occurrenceid'],
        'kingdom' : t['kingdom'],
        'phylum' : t['phylum'],
        '_class' : t['class'],
        '_order' : t['order'],
        'family' : t['family'],
        'genus' : t['genus'],
        'scientific_name' : t['species'],
        'country_code' : t['countrycode'],
        'locality' : t['locality'],
        'latitude' : t['decimallatitude'],
        'longitud' : t['decimallongitude'],
        'elevation_in_meters' : t['elevation'],
        #'elevationaccuracy' : t['elevationaccuracy'],
        'depth_in_meters' : t['depth'],
        #'depthaccuracy' : t['depthaccuracy'],
        'event_date' : t['eventdate'],
        'day' : t['day'],
        'month' : t['month'],
        'year' : t['year'],
        #'taxonkey' : t['taxonkey'],
        'species_id' : t['specieskey'],
        'basis_of_record' : t['basisofrecord']
        }
        O = Occurrence(*dictoccur)
        l.append(O)
    return l
        
        
        
        
        
        
        
def CSVReadfrom(FILE,with_delimiter='\t'):
    f = open(FILE,'r')
    csvDictReader = csv.DictReader(f,delimiter=with_delimiter)
    
    #lista = CSVLoad(csvDictReader)
    #fieldnames = csvDictReader.fieldnames
    #f.close()
    return (csvDictReader,f)


def CSVLoadfrom(FILE,with_delimiter='\t'):
    f = open(FILE,'r')
    csvDictReader = csv.DictReader(f,delimiter=with_delimiter)
    csvout = list(csvDictReader)
    f.close()
    #lista = CSVLoad(csvDictReader)
    #fieldnames = csvDictReader.fieldnames
    #f.close()
    return (csvout)

WKT_big = "POLYGON((-100.94609147800035487 19.36818845857660065,-99.37564350134034896 19.35208362503138346,-99.3158981978804718 18.2857029670664275,-100.87781113118906262 18.22896530284194938,-100.94609147800035487 19.36818845857660065))"

WKT_small = "POLYGON((-101.47099664411226172 19.11838542365211779,-101.30456329875971733 19.11435323280499432,-101.32163338546253328 18.94491262920351105,-101.47526416578797637 18.9328031251580029,-101.47099664411226172 19.11838542365211779))"

WKT_lancanshire = "POLYGON((-2.80557791795337286 54.06638106541203825,-2.65342150624366369 54.06698849374796367,-2.64979873453629011 53.98642680841847863,-2.80557791795337286 53.98642680841847863,-2.80557791795337286 54.06638106541203825))"


#r=getOccurrenceN(WKT_big)
#t=curateOccurrences(r)
#a=t[0]
#x=webGBIFtoOccurence(a)

#occurrences = map(lambda j : webGBIFtoOccurence(j),t)


#CSVPATH = "/home/juan/gbif/0024366-151016162008034.csv"

from gbif.models import Occurrence_CSV_4insert as  Occurrence_CSV
from multiprocessing import Pool


def instantiateOccurrence(keyvalues):
    duples = keyvalues.viewitems()
    occ = Occurrence_CSV()
    map(lambda (key,val) : setattr(occ,key,val.decode('UTF-8','replace')),duples)
    occ.insertOccurrence()
    return occ

def createOccurrenceFromCSVFile(list_csv_dic,numcores=1):
    #listoccs = []
    

    p = Pool(numcores)
    listoccs = p.map( instantiateOccurrence,list_csv_dic)
    p.close()
    #for row in list_csv_dic:
    
        #listoccs.append(occ)
        #f.close()   
    #f.close()
    return listoccs



