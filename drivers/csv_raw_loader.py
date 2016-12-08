#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
csv_raw_loader
=============
.. note::
    This module has functions that works for populating the POSTGIS database.
    This uses RAW SQL statements to load the data into de the DBMS.
    It is way - way- way faster than using the GBIF / Biospytial API
"""


import os
from gbif.taxonomy import Occurrence
import logging
from django.db import connection





cursor = connection.cursor()
logger = logging.getLogger('biospytial.driver.csv_raw_loader')




def LoadFile(PATH,filename,RAWSQL,cursor):
    FILE = PATH + '/' + filename
    SQLCODE = RAWSQL %FILE
    FILE_STORE = "/home/juan/gbif/all_gbif/splitted_gbif/header"
    PATH_OUTPUT = "/home/juan/gbif/all_gbif/splitted_gbif/processed"
    FILE_OUTPUT = "bad_csv.txt"
    bugfile = FILE_STORE + "/" + FILE_OUTPUT
    writetofile = open(bugfile,'a')
    try:
        exito = cursor.cursor.execute(SQLCODE)
        logger.info("File %s successfully inserted!" %filename)
        os.rename(FILE_STORE + '/' +filename, PATH_OUTPUT + '/' + filename)
        return exito
    except Exception, e:
        #logger.error("Something occurred with this file: %s need to reload it manually." %filename)   
        error_message =  " In file %s : %s \n" %(filename,str(e))
        logger.error(error_message)
        writetofile.write(error_message)
        writetofile.close()
        return error_message



FILE_OUTPUT = "bad_csv.txt"

FILE_STORE = "/home/juan/gbif/all_gbif/splitted_gbif/header"

PATH,subdir,files = os.walk(FILE_STORE).next()

bugfile = FILE_STORE + "/" + FILE_OUTPUT


RAW_SQL = "COPY gbif_occurrence_csv (id_gbif, dataset_id, institution_code, collection_code, catalog_number,   basis_of_record , scientific_name, scientific_name_author, taxon_id, kingdom, phylum, _class, _order, family, genus, specific_epithet, kingdom_id, phylum_id, class_id, order_id, family_id, genus_id, species_id, country_code, latitude, longitude, year, month, event_date, elevation_in_meters, depth_in_meters, verbatim_scientific_name, taxon_rank, verbatim_kingdom, verbatim_phylum, verbatim_class, verbatim_order, verbatim_family, verbatim_genus, verbatim_specific_epithet, verbatim_infraspecific_epithet, verbatim_latitude, verbatim_longitude, coordinate_precision, maximum_elevation_in_meters, minimum_elevation_in_meters, elevation_precision, minimum_depth_in_meters, maximum_depth_in_meters, depth_precision, continent_ocean, state_province, county, country, recorded_by, locality, verbatim_year, verbatim_month, day, verbatim_basis_of_record, identified_by, date_identified, created, modified) FROM '%s' DELIMITER E'\t' CSV HEADER; "

RAW_SQL = "COPY gbif_occurrence_csv_verbatim  FROM '%s' DELIMITER E'\t' CSV HEADER; "



"""
RAW_SQL = \""" COPY gbif_less_data(id_gbif,
dataset_id, 
institution_code, 
--collection_code, 
--catalog_number,
--basis_of_record , 
scientific_name, 
--scientific_name_author, 
taxon_id, 
kingdom, 
phylum, 
_class, 
_order, 
family, 
genus, 
specific_epithet, 
kingdom_id, 
phylum_id, 
class_id, 
order_id, 
family_id, 
genus_id, 
species_id, 
country_code, 
latitude, 
longitude, 
year, 
month, 
event_date, 
elevation_in_meters, 
depth_in_meters, 
--verbatim_scientific_name, 
--taxon_rank, 
--verbatim_kingdom, 
--verbatim_phylum, 
--verbatim_class, 
--verbatim_order, 
--verbatim_family, 
--verbatim_genus, 
--verbatim_specific_epithet, 
--verbatim_infraspecific_epithet,
--verbatim_latitude, 
--verbatim_longitude, 
coordinate_precision, 
--maximum_elevation_in_meters, 
--minimum_elevation_in_meters, 
--elevation_precision, 
--minimum_depth_in_meters, 
--maximum_depth_in_meters, 
depth_precision, 
continent_ocean, 
state_province, 
--county, 
country, 
--recorded_by,
locality,
--verbatim_year,
--verbatim_month,
day, 
--verbatim_basis_of_record, 
--identified_by, 
date_identified, 
created) 
--modified) 
FROM '%s'
DELIMITER E'\t' CSV HEADER; 
\"""
"""

