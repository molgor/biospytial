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



logger = logging.getLogger('biospatial.gbif')
# Create your tests here.


# Occurrences file

PATH = '/Users/juan/GEM/MasterTesis/data/0001286-131023101652840'

NAME = 'first_occurrences'

RESOURCE = PATH + '/' + NAME

f = open(RESOURCE,'r')






header = f.readline()
line = f.readline()
counter = 0
cnt = 1
while line:    
    l_uno = line.split('\t')
    c = Occurrence(*l_uno)
    line = f.readline()
    c.insertOccurrence()
    counter += 1
    if counter == 1000:
        r = cnt * counter
        print "Llevo %s" %r
        counter = 0
        cnt += 1



def OLDvalidateNfix(c):
    fields =  c._meta.get_all_field_names()
    for f in fields:
        internalType = c._meta.get_field_by_name(f)[0].get_internal_type()
        if isinstance(getattr(c,f),str) and ('Char' not in internalType):
            logger.warn("inv�lido")
            print "esta definido como: %s pero debe ser %s" %('str',internalType)
            if 'Float' in internalType:
                try:
                    setattr(c,f,float(getattr(c,f)))
                except:
                    if not getattr(c,f):
                        setattr(c,f,settings.NULL_DATA_FLOAT)
                    print "es %s y su valor es: %s" %(internalType,getattr(c,f))
                    logger.error("Se encontró valor vacio. Se cambia el valor a -9999.999")
            elif 'Integer' in internalType:
                try:
                    setattr(c,f,int(getattr(c,f)))       
                except:
                    if not getattr(c,f):
                        setattr(c,f,settings.NULL_DATA_INTEGER)
                    print "es %s y su valor es: %s" %(internalType,getattr(c,f))
                    logger.warn("Se encontró valor vacio. Se cambia el valor a -9999")
            elif 'Date' in internalType:
                #try:
                datestr = getattr(c,f).replace('\n','')
                setattr(c,f,dateutil.parser.parse(datestr))     
                            
        else:
            logger.debug("correcto ")
            print 'esta bien'


print "This is a test for git"

# #===============================================================================
#for i in c._meta.get_all_field_names():
#    print "%s : %s | %s internal: %s" %(i,getattr(c,i),type(getattr(c,i)),c._meta.get_field_by_name(i)[0].get_internal_type())
#===============================================================================