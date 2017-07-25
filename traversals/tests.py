from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry 
# Create your tests here.
######
## Here I'm testing how to extract data in the Diggle's format, 2017 letter to Pete, Luigi and Me.

from drivers.graph_models import TreeNode, Order, Family, graph, pickNode
from traversals.strategies import sumTrees, UniformRandomSampleForest,PolygonToTrees
from mesh.models import initMesh
polystr = 'POLYGON((-92.24837214921502948 16.53658521768252854,-92.11186028915844304 16.52849027585105901,-92.10623093410457329 16.37327180168962926,-92.25118682674197146 16.37462206197250225,-92.24837214921502948 16.53658521768252854))'
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