#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Simulation Exercises done with Mr. Erick "El Vikingo" Chacon Montalvan 
======================================================================

Some functions an ,methods for implementing Gaussian simulation of autocorrelated processes. 

Authors :

    Erick Chacon 
    Juan Escamilla
    
Date: 
   28/07/2017    
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
lat = np.linspace(0,100,10)
lon = np.linspace(0,100,10)


### Calculate crosws product of time for distance matrix

makeDuples = lambda list_of_points : [(i,j) for i in list_of_points for j in list_of_points]

## This function returns a Distance Matrix given a list of pairs of the form (a,b). It will calculate de distance between (a and b) 

calculateDistanceMatrix = lambda list_of_vectors : np.array(map(lambda (a,b) : np.linalg.norm(a-b),list_of_vectors))
## note it doesn't have shape of a matrix but doesn't matter.


#### Let's generate several correlation functions for different phis

corr_exp_list = map(lambda phi : partial(corr_exp_ij,phi=phi),np.linspace(1,100,50))
corr_exp_list = map(lambda phi : partial(corr_exp_ij,phi=phi),[0.001,20,80])

## Calculate correlations 
makeCorrelations = lambda model : lambda list_of_points : np.array(map(model,calculateDistanceMatrix(makeDuples(list_of_points))))





## Calculate covariances
makeCovarianceMatrix = lambda sigma : lambda model: lambda list_of_points : (makeCorrelations(model)(list_of_points) * sigma).reshape(100,100)


## Different models for phi
covarianceMatricesModels = map(lambda model : makeCovarianceMatrix(1.0)(model)(time),corr_exp_list)



## Simulation process

zeros = np.zeros(100)

Zs = map(lambda Sigma : sp.random.multivariate_normal(zeros,Sigma),covarianceMatricesModels)
















