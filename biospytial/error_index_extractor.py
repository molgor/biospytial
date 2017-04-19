#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Error_index extractor
=====================
This script has functions for extracting the taxonomy (cellid) where disconnections from the database were found and therefore skipped from the main insertion process.
It only specifies the functions. For running see: insert_failed_taxonomies.

.. 
 
"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2017, JEM"
__license__ = "GPL"
__version__ = "0.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



#W3_FILE.close()


#w1 = w1_list[1:]
#w2 = w2_list[1:]

"""
This is the shape of each line (INFO lines) for ERRORS is a bit different but the first indexes are the same, which are the ones that matter.
['[12/Mar/2017',
 '23:20:30]',
 'INFO',
 '[biospytial.insert_taxonomies_worker1:72]',
 '[PROCESS:',
 '1',
 ']',
 'Taxonomy',
 '141272',
 'inserted.',
 '0',
 '/',
 'N.',
 'Completed:',
 '0.0\n']

"""

cleandata = lambda datafile : filter(lambda l : len(l.split(" ")) > 10,datafile)



extract_data = lambda line : [ line.split(" ")[i] for i in [2,8,10]]

toList = lambda raw_text : map(extract_data,raw_text)

prepare1 = lambda raw_text : map(lambda (i,l) : l + [i] ,enumerate(toList(raw_text)))




def extractIdx(prepared_list):
    l = prepared_list
    idx = 0
    idw = 0 
    lx = []
    for (word,taxid,id,id2) in l :
        if "INFO" == word :
            idw = int(taxid)
            idx = int(id)
            continue
        elif "ERROR" == word :
            idw += 1
            idx += 1
            lx.append([word,idw,idx,id2])
    return lx

Only = lambda list : map(lambda e : e[1],list)







