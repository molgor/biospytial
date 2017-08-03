#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Statistical Models
======================================================================

This module combines traversal strategies for visiting and storing the spatial tree-structures.

The models range from simple linear to Gaussian Processes.

This file is intented to be big!

Some functions an methods for implementing Gaussian simulation of autocorrelated processes. 

Author :
    Juan Escamilla
    
With Great help of:
     Erick Chacón Montalván    
Date: 
   02/08/2017    
"""

import numpy as np

import scipy as sp
from functools import partial

def corr_exp_ij(distance,phi=1.0):
    """
    This function calculates the correlation function of an exponential model with parameter phi.
    Returns :
        correlation value for distance 'distance'
    """
    return np.exp(-(distance / phi))



## Generate the preimage . For this exampe will be: time \in R

time = np.linspace(0, 100, 100)
lat = np.linspace(0,100,50)
lon = np.linspace(0,100,50)


### Calculate crosws product of time for distance matrix

makeDuples = lambda list_of_points : [(i,j) for i in list_of_points for j in list_of_points]

points = map(lambda l : np.array(l),makeDuples(lat))



## This function returns a Distance Matrix given a list of pairs of the form (a,b). It will calculate de distance between (a and b) 

calculateDistanceMatrix = lambda list_of_vectors : np.array(map(lambda (a,b) : np.linalg.norm(a-b),list_of_vectors))
## note it doesn't have shape of a matrix but doesn't matter.


def generateCorrelationFunctional(function, list_parameter_space,parameter_name):
    """
    Returns a list of functions mapped with a partition.
    i.e. given a function $f$ with parameters $\theta$ for a given parameter.
    """
    f = function
    functions = map(lambda phi : partial(f,parameter_name=phi),list_parameter_space)
    return functions
#### Let's generate several correlation functions for different phis

corr_exp_list = map(lambda phi : partial(corr_exp_ij,phi=phi),np.linspace(1,100,50))
corr_exp_list = map(lambda phi : partial(corr_exp_ij,phi=phi),[0.001,20,80])
corr_exp_list = map(lambda phi : partial(corr_exp_ij,phi=phi),[20])

## Calculate correlations 
makeCorrelations = lambda model : lambda list_of_points : np.array(map(model,calculateDistanceMatrix(makeDuples(list_of_points))))





## Calculate covariances
makeCovarianceMatrix = lambda sigma : lambda model: lambda list_of_points : (makeCorrelations(model)(list_of_points) * sigma)#.reshape(100,100)


## Different models for phi
covarianceMatricesModels = lambda list_of_points : map(lambda model : makeCovarianceMatrix(1.0)(model)(list_of_points),corr_exp_list)

#covarianceMatricesModels = map(lambda model : makeCovarianceMatrix(1.0)(list_of_points)(list_of_points),corr_exp_list)


## Simulation process

zeros = lambda list_of_points : np.zeros(np.sqrt(len(list_of_points))**2)

simulateWithThisPoints = lambda list_of_points : map(lambda Sigma : sp.random.multivariate_normal(zeros(list_of_points),Sigma.reshape(len(list_of_points),len(list_of_points))),covarianceMatricesModels(list_of_points))
















