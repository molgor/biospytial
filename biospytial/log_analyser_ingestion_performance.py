#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Log Analyser
============

This script is only intented to provide information of performance for each worker within a host.
The task is to insert data in the neo4j database. 
i.e. look-up constantly to the postgis backend.

note: The worker are running so I'll work on copies of the current executions.


.. 
 
"""
import datetime as dt
import pandas as pd
__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2017, JEM"
__license__ = "GPL"
__version__ = "0.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"


W1_FILE = open("logs/w1.log",'r')

W2_FILE = open("logs/w2.log",'r')
W3_FILE = open("logs/w3.log",'r')


w1_list = W1_FILE.readlines()
w2_list = W2_FILE.readlines()
w3_list = W3_FILE.readlines()
W1_FILE.close()
W2_FILE.close()
W3_FILE.close()

#Remove header info
w1 = w1_list[1:]
w2 = w2_list[1:]
w3 = w3_list[1:]

limpia1 = lambda y : (y[0],y[1],y.pop())



limpia2 = lambda (fecha,hora,porcentaje) : (fecha.replace("[","") + "|" + 
                                            hora.replace("]",""), 
                                            porcentaje.replace("\n","")
                                            )

totime = lambda (hora,porcentaje) : ( dt.datetime.strptime(hora, "%d/%b/%Y|%H:%M:%S"),
                                       float(porcentaje)
                                      )


def getIntervals(dataframe):
    a = list(dataframe[0])
    b = list(dataframe[0][1:])
    ab = zip(a,b)
    
    interval = map( lambda (a,b) : b - a, ab)
    # add something to be concordant with array shape
    interval.append(interval[ len(interval) - 1 ] )
    dataframe['interval_s'] = map(lambda s : s.seconds, interval)
    return dataframe


superlimpia = lambda l : totime(limpia2(limpia1(l.split(" "))))

toPandas = lambda lista : pd.DataFrame(map(superlimpia,lista))

toIntevals =  lambda lista : getIntervals(toPandas(lista))

d1 = toIntevals(w1)
d2 = toIntevals(w2)
d3 = toIntevals(w3)
#datos1 = map(superlimpia, w1)
#datos2 = map(superlimpia,w2)

#d1 = pd.DataFrame(datos1)
#d2 = pd.DataFrame(datos2)


