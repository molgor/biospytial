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



from django.test import TestCase
from django.conf import settings
import logging
from gbif.models import Occurrence
from django.db import models
import dateutil.parser
from models import Count,Sum,Avg


logger = logging.getLogger('biospatial.gbif')
# Create your tests here.


# Grouping shit
r = sp.objects.values('family').annotate(total=Count('scientific_name'))
