#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

NAME
=============
.. note::
    Algunas notillas
    created on: 5 Jan 2016 at 20:14:49 by juan
"""
from posix import fpathconf
from django.template.context_processors import request
from datetime import datetime
from drivers.neo4j_reader import TreeNeo

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2016, JEM"
__license__ = "GPL"
__version__ = "2.0.0"
__mantainer__ = "juan"
__email__ ="j.escamillamolgora@lancaster.ac.uk"
__status__ = "Beta"



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

URLBASE = "http://api.gbif.org/v1/"
URLOCCURRENCE = URLBASE+"occurrence/search"

logger = logging.getLogger('biospytial.gbif.drivers.populate')


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
    try:
        occ = Occurrence(
        id = json_gbif['gbifID'],
        dataset_id = json_gbif['datasetKey'],
        institution_code = json_gbif['institutionCode'],
        collection_code = json_gbif['collectionCode'],
        catalog_number = json_gbif['catalogNumber'],
        basis_of_record = json_gbif['basisOfRecord'],
        
        
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
        
        country_code = json_gbif['countryCode'],
        latitude = json_gbif['decimalLatitude'],
        longitude = json_gbif['decimalLongitude'],
        
        year = json_gbif['year'],
        month = json_gbif['month'],
        day = json_gbif['day'],
        event_date = json_gbif['eventDate'],
        #taxon_rank = json_gbif['taxonRank'],
        #modified = json_gbif['modified'],
        #recorded_by  = json_gbif['recordedBy'],
        country = json_gbif['country'],
        
        #locality  = json_gbif['verbatimLocality'],
        
        #date_identified = datetime.date(year=int(json_gbif['year']),month=int(json_gbif['month']),day=int(json_gbif['day'])), 
        #json_gbif['dateIdentified'],
        
        geom = Point(float(json_gbif['decimalLongitude']),float(json_gbif['decimalLatitude']), srid=4326),
        
        #taxon_id = json_gbif['taxonKey']
        )
        return occ
    except KeyError as e:
        logger.warn("Missing data in field %s:"%e)

"""
    geom = 
    scientific_name_author = 
    elevation_in_meters = 
    depth_in_meters = 
    verbatim_scientific_name = 
    verbatim_kingdom =
    verbatim_phylum =
    verbatim_class = 
    verbatim_order =
    verbatim_family = 
    verbatim_genus =
    verbatim_specific_epithet
    verbatim_infraspecific_epithet 
    verbatim_latitude = 
    verbatim_longitude =
    coordinate_precision =
    maximum_elevation_in_meters =
    minimum_elevation_in_meters = 
    elevation_precision =
    minimum_depth_in_meters =
    maximum_depth_in_meters =
    depth_precision =
    continent_ocean = 
    state_province =
    county =
    
   
    
    verbatim_year =
    verbatim_month =
    
    verbatim_basis_of_record  =
    identified_by  = 
    
    created = 
    'geodeticDatum',
    species = 'species'
"""

def getAllOccurrences(WKT,url=URLOCCURRENCE,offset=0,safeinDB=False):
    """
    Get all Occurrences from the occurrence/search API
    """
    list_occurrences = []
    r = getOccurrenceN(WKT, url=url, offset=offset)
    j = r.json()
    while not j['endOfRecords']:
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
        logger.debug("Retrieving information to the server. Offset:%s", offset)
    return list_occurrences
# Create your tests here.



def get_distribution_per_level(gridded_taxonomy):
    g = gridded_taxonomy
    n = len(g)
    l = []
    for i,t in enumerate(g):
        ocs = extractOccurrencesFromTaxonomies([t])
        t = TreeNeo(ocs)
        logger.info('Done %s/%s'%(i,n))
        l.append(t)
    return l




WKT_big = "POLYGON((-100.94609147800035487 19.36818845857660065,-99.37564350134034896 19.35208362503138346,-99.3158981978804718 18.2857029670664275,-100.87781113118906262 18.22896530284194938,-100.94609147800035487 19.36818845857660065))"

WKT_small = "POLYGON((-101.47099664411226172 19.11838542365211779,-101.30456329875971733 19.11435323280499432,-101.32163338546253328 18.94491262920351105,-101.47526416578797637 18.9328031251580029,-101.47099664411226172 19.11838542365211779))"

r=getOccurrenceN(WKT_big)
t=curateOccurrences(r)
a=t[0]
x=webGBIFtoOccurence(a)

occurrences = map(lambda j : webGBIFtoOccurence(j),t)


