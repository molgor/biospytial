#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Django settings for biospytial project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

CONDA_PREFIX = '/home/juan/miniconda2/envs/biospytial'
CONDA_PREFIX = '/opt/conda/envs/biospytial'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_7*7q^b%crsn54ojvl6n)wwqcijnvs2=74r!ke%s1%h!m4hbe9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['172.17.0.3','localhost']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'gbif',
    'mesh',
    'sketches',
    'raster_api',
    'django_pdb',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_pdb.middleware.PdbMiddleware',
)

ROOT_URLCONF = 'biospytial.urls'

WSGI_APPLICATION = 'biospytial.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        #'django.db.backends.postgresql_psycopg2',
        'NAME': 'biospytial',
        'USER': 'biospytial',
        'PASSWORD': 'biospytial.',
        #'HOST':'panthera',
        #'HOST': '10.42.17.241',
        'HOST':'postgis',
        #'NAME': 'gbif',
        #'USER': 'juan',
        #'PASSWORD': 'biospytial.',
        #'HOST': '148.88.197.8',

        #'HOST' : '172.17.0.2'
        #'HOST':'postgis'
        ## My server in ISS
        
       
    #local
        #'NAME' : 'masterthesis',                      
        #'USER' : 'juan',
        #'HOST' : 'localhost'

    
    },            
             
    #===========================================================================
    # 'local': {
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     #'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'masterthesis',                      
    #     'USER': 'juan',
    #     'PASSWORD': '',
    #     'HOST': 'localhost'
    # },
    #===========================================================================
   # 'operational': {
   #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
   #     #'django.db.backends.postgresql_psycopg2',
   #     'NAME': 'gbif',                      
   
   #     'USER': 'gbif',
   #     'PASSWORD': 'biology',
   #     'HOST': 'geodata'
   # }             
    
}

NEO4J_DATABASES = {
    'default' : {
        #'HOST':'148.88.197.8',
        'HOST':'neo4j',
        'PORT':7474,
        'ENDPOINT':'/db/data',
        'USERNAME':'neo4j',
        'PASSWORD':'perro'
        
    }
}



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'simple_raster': {
            'format': '%(levelname)s [Raster API] %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/biospytial.log',
            'formatter': 'verbose'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'gbif.taxonomy':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
                 
        'file_raster':{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/biospatial_raster.log',
            'formatter': 'verbose'
        },
        'neo4j_reader':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file_insertion': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/insertion_in_neo.log',
            'formatter': 'verbose'
        },
        'file_insertion_w1': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/w1_insertion_in_neo.log',
            'formatter': 'verbose'
        },  
        'file_insertion_w2': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/w2_insertion_in_neo.log',
            'formatter': 'verbose'
        },
        'file_insertion_w3': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR+'/logs/w2_insertion_in_neo.log',
            'formatter': 'verbose'
        },                                      
        
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': False,
            'level':'INFO',
       },
#         'biospytial.gbif.insertion': {
#             'handlers': ['file'],
#             'propagate': True,
#             'level': 'DEBUG',
#         },
#         'biospytial.gbif': {
#             'handlers': ['gbif.taxonomy'],
#             'propagate': False,
#             'level': 'DEBUG',
#         },
#         'biospytial.driver.csv_raw_loader' : {
#             'handlers': ['console'],
#             'level': 'DEBUG',                                   
#         
#         },
        'biospytial.gbif.taxonomy' :{
             'handlers': ['console'],
             'level' : 'DEBUG',
             'propagate': True,
         },       
        'biospytial.raster_api.tools':{
             'handlers': ['console'],
             'level' : 'DEBUG',         
         },
        'biospytial.insert_taxonomies' :{
            'handlers' : ['file_insertion'],
            'level' : 'DEBUG',
        },
        'biospytial.insert_taxonomies_worker1' :{
            'handlers' : ['file_insertion_w1'],
            'level' : 'DEBUG',
        },
        'biospytial.insert_taxonomies_worker2' :{
            'handlers' : ['file_insertion_w2'],
            'level' : 'DEBUG',
        },
        'biospytial.insert_taxonomies_worker3' :{
            'handlers' : ['file_insertion_w3'],
            'level' : 'DEBUG',
        },                       
#         'biospytial.mesh.tools':{
#             'level': 'DEBUG',
#             'handlers': ['console'],    
#             },

},
}

#######################
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

NULL_DATA_FLOAT = -99999.9
NULL_DATA_INTEGER = -99999

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = '/var/tmp/trees/'

TEMPLATE_DIRS = (
    '/Users/juan/git_projects/biospytial/templates/',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/tmp/trees/',
)

STATICFILES_FINDERS = ( 
    'django.contrib.staticfiles.finders.FileSystemFinder', 
    'django.contrib.staticfiles.finders.AppDirectoriesFinder', 

)

###### EXTENDED SETTINGS
TAXONOMIC_LEVELS = ['gid','occurrence','species','families','genera','orders','classes','phyla','kingdoms']
TAXONOMIC_TREE_KEYS = ['sp','gns','fam','ord','cls','phy','kng']
TAXONOMIC_MAPPER_KEYS = {'gid' : 'gid','oc':'occurrence','sp':'species','gns':'genera','fam':'families','ord':'orders','cls':'classes','phy':'phyla','kng':'kingdoms'}



# Prefix for caching
NESTED_TAXONOMY_PREFIX = 'nstax'
GRIDDED_TAXONOMY_PREFIX = 'gdtax'
TAXONOMY_PREFIX = 'tax'

# Uncomment if it's local
#GBIF_DATATABLE = "mexico_gbif_subset"

#Uncomment for remote host
GBIF_DATATABLE = "gbif_occurrence_csv"
        # Local table name
        #db_table = "mexico_gbif_subset"
 
# Mesh table settings. provisional. expected to have it's on config file
BRAZ_SCALES = { 8 : 'mesh\".\"braz_grid8a',
          9 : 'mesh\".\"braz_grid16a',
          10 : 'mesh\".\"braz_grid32a',
          11 : 'mesh\".\"braz_grid64a',
          12 : 'mesh\".\"braz_grid128a',
          13 : 'mesh\".\"braz_grid256a',
          14 : 'mesh\".\"braz_grid512a',
          15 : 'mesh\".\"braz_grid1024a',
          16 : 'mesh\".\"braz_grid2048a',
          17 : 'mesh\".\"braz_grid4096a'
          }



MEX_SCALES = { 0 : 'mesh"."mexico_grid1',
        1: 'mesh"."mexico_grid2',
        2: 'mesh"."mexico_grid4',
        3: 'mesh"."mexico_grid8',
        4: 'mesh"."mexico_grid16',
        5: 'mesh"."mexico_grid32',
        6: 'mesh"."mexico_grid64',
        7: 'mesh"."mexico_grid128',
        8: 'mesh"."mexico_grid256',
        9: 'mesh"."mexico_grid512',
        10: 'mesh"."mexico_grid1024'
        }


# MEX_SCALES = {0: 'mesh"."testnested1',
#  1: 'mesh"."testnested2',
#  2: 'mesh"."testnested4',
#  3: 'mesh"."testnested8',
#  4: 'mesh"."testnested16',
#  5: 'mesh"."testnested32',
#  6: 'mesh"."testnested64'}


#ANALYSIS ON GRID SET: 
MESH_TABLENAMESPACE = MEX_SCALES
#MESH_TABLENAMESPACE = BRAZ_SCALES


GDAL_LIBRARY_PATH = CONDA_PREFIX+'/lib/libgdal.so'

#CSVABSOLUTEPATH = "/home/juan/gbif/all_gbif/splitted_gbif/header"
CSVABSOLUTEPATH = "/home/juan/gbif/mexico/bigdatabase_subset/pieces"
CSVABSOLUTEPATH = "/RawDataCSV"
## KEYS FOR WRITING AS PROPERTIES IN THE NEo4j NODE OCCURRENCE

OCCURRENCE_KEYS_4NEO = ['species_id','scientific_name','year','month','day','latitude','longitude','event_date','geom']

PATH_IMAGES = '/Users/juan/git_projects/biospytial/static/trees/'

PATH_OUTPUT = '/home/juan/Research/biospytial-output/'

RASTERNODATAVALUE = -9999

NOTEBOOK_ARGUMENTS = [
    # exposes IP and port
    '--ip=0.0.0.0',
    '--port=8888',
    # disables the browser
    '--no-browser',
]




