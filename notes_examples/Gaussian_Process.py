#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Here I´m using 
# Gaussian Processes examples with SciKit learn.
I´m following de documentation in Scikit-learn Gaussian Process examples.
\url{http://scikit-learn.org/stable/modules/gaussian_process.html}

#@Author: Juan Escamilla 
#@Date: 9/08/2017

"""

# First thing first, Let´s load some data.

def loadData1():
    from traversals import dataExtractionExamples as data
    reload(data)
    d = data.main()
    return d
    
    
d = loadData1    
trees = d['LTrees']
T = d['BTREE']
data = d['Table']


 


# visualizing and analysing