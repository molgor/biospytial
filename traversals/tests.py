
from external_plugins.spystats.models import *
from django.contrib.gis.geos import GEOSGeometry 
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt                                                             
# Create your tests here.
######
## Here I'm testing how to extract data in the Diggle's format, 2017 letter to Pete, Luigi and Me.

from drivers.graph_models import TreeNode, Order, Family, graph, pickNode
from traversals.strategies import sumTrees, UniformRandomSampleForest,PolygonToTrees
from mesh.models import initMesh
from traversals.strategies import getEnvironmentalCovariatesFromListOfTrees,getPresencesForListOfNodes,getCentroidsFromListofTrees


## Small area.
polystr = 'POLYGON((-92.24837214921502948 16.53658521768252854,-92.11186028915844304 16.52849027585105901,-92.10623093410457329 16.37327180168962926,-92.25118682674197146 16.37462206197250225,-92.24837214921502948 16.53658521768252854))'
## Bigger Area
#polystr = 'POLYGON((-92.54989447928841173 16.93450143453089396,-91.70267654367958698 16.9021871200489322,-91.68015912346406537 16.28717344210308937,-92.56396786692310741 16.31959139053146757,-92.54989447928841173 16.93450143453089396))'
trees = PolygonToTrees(polystr)
big_t = reduce(lambda a,b : a+b, trees)
polygon = GEOSGeometry(polystr)
mesh = initMesh(11) 
cells = list(mesh.objects.filter(cell__intersects=polygon)) 
x = big_t.associatedData.getAssociatedRasterAreaData('MeanTemperature')
cts = zip(cells,trees)
c0,t0 = cts[2]
c1,t1 = cts[1]


rd = getEnvironmentalCovariatesFromListOfTrees(trees)
s = getPresencesForListOfNodes(big_t.to_Animalia.to_Chordata.to_Aves.to_Falconiformes,trees)

X = rd[["WindSpeed_mean","Elevation_mean"]]
y = s.Falconidae
centroids = list(s[["Longitude","Latitude"]].as_matrix())
phis =np.linspace(0.01,1.0,100)
sigmas =np.linspace(0.01,2.0,100)

phis_sigma = [(phi , sigma) for phi in phis for sigma in sigmas]

x0 = np.array([0.1,0.22,0.001,0.001,0.001])  
Xs = np.matrix(X)


#superfunciones = np.array(map(lambda (phi,sigma) : likelihoodFunction(phi,sigma,y,centroids),phis_sigma))

