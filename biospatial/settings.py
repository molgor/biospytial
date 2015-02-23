"""
Django settings for biospatial project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_7*7q^b%crsn54ojvl6n)wwqcijnvs2=74r!ke%s1%h!m4hbe9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
    'django_pdb',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_pdb.middleware.PdbMiddleware',
)

ROOT_URLCONF = 'biospatial.urls'

WSGI_APPLICATION = 'biospatial.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        #'django.db.backends.postgresql_psycopg2',
        'NAME': 'gbif',                      
        'USER': 'gbif',
        'PASSWORD': 'biology',
        'HOST': 'geodata'
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
    'operational': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        #'django.db.backends.postgresql_psycopg2',
        'NAME': 'gbif',                      
        'USER': 'gbif',
        'PASSWORD': 'biology',
        'HOST': 'geodata'
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
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/biospatial.log',
            'formatter': 'verbose'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'ERROR',
        },
        'biospatial.gbif.insertion': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
        'biospatial.gbif': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

###### EXTENDED SETTINGS
TAXONOMIC_LEVELS = ['gid','occurrence','species','families','genera','orders','classes','phyla','kingdoms']
TAXONOMIC_TREE_KEYS = ['sp','gns','fam','ord','cls','phy','kng']
TAXONOMIC_MAPPER_KEYS = {'gid' : 'gid','oc':'occurrence','sp':'species','gns':'genera','fam':'families','ord':'orders','cls':'classes','phy':'phyla','kng':'kingdoms'}

PATH_IMAGES = '/Users/juan/git_projects/biospatial/static/trees/'

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
    '/Users/juan/git_projects/biospatial/templates/',
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/tmp/trees/',
)

STATICFILES_FINDERS = ( 
    'django.contrib.staticfiles.finders.FileSystemFinder', 
    'django.contrib.staticfiles.finders.AppDirectoriesFinder', 

) 
