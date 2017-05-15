# coding: utf-8
from django.contrib.gis.db.models import Collect,Count
from ecoregions.models import InegiIV
coberturas = InegiIV.objects.values('name').annotate(num=Count('cov'),polys=Collect('geom'))
coberturas[1]
coberturas[1:10]
chiq = coberturas[1:10]
chiq
chiq = list(coberturas[1:10])
chiq
chiq[2]
chiq[5]
chiq[6]
chiq[7]
chiq[8]
chiq[9]
chiq[4]
bosque_pino_encino = chiq[4]
import mesh.tools as mt
import mesh.models as mm
mm.initMesh(10)
mm.initMesh(12)
m12 = mm.initMesh(12)
m12
m11 = mm.initMesh(11)
m11
bosque_pino_encino
bosque_pino_encino['polys']
polys = bosque_pino_encino['polys']
m11.objects.filter(cell__intersects=polys)
from django.contrib.gis.db.models import Union
coberturas = InegiIV.objects.values('name').annotate(num=Count('cov'),polys=Union('geom'))
chiq = list(coberturas[1:10])
bosque_pino_encino = chiq[4]
bosque_pino_encino
celdajis = m11.objects.filter(cell__intersects=polys)
celdajis
polys = bosque_pino_encino['polys']
celdajis = m11.objects.filter(cell__intersects=polys)
celdajis
celdas= list(celdajis)
celdajis.count()
celdas= list(celdajis)
celdas
celdas[1]
celdas[1].id
ids = map(lambda l : l.id,celdas)
ids
from drivers.graph_models import Cell
Cell.select(?
Cell.select(?
get_ipython().magic(u'pinfo Cell.select')
Cell.select(graph)
from drivers.graph_models import graph
getCell = lambda pk : Cell.select(graph,primary_value=pk)
celdas
ids
cell_nodes = map(getCell,ids)
cell_nodes
getCell = lambda pk : Cell.select(graph,primary_value=pk).first()
cell_nodes = map(getCell,ids)
getCell = lambda pk : Cell.select(graph,primary_value=pk)
cell_nodes = map(getCell,ids)
cell_nodes[0]
c = cell_nodes[0]
c.first
c.first()
graph
graph
c = cell_nodes[0]
c
c.first()
list(cell_nodes)
get_ipython().magic(u'script')
get_ipython().magic(u'save')
get_ipython().magic(u'save tree_pino_encino')
get_ipython().magic(u'ls ')
get_ipython().magic(u'save tree_pino_encino')
get_ipython().magic(u"save 'tree_pino_encino'")
get_ipython().magic(u"save 'tree_pino_encino.txt'")
get_ipython().magic(u"save 'tree_pino_encino.txt'")
get_ipython().magic(u"save 'tree_pino' 'tree_pino_encino.txt'")
get_ipython().magic(u"save 'tree_pino_encino.txt'")
get_ipython().magic(u'pinfo %save')
get_ipython().magic(u"save 'pino-encino.txt' 1 84")
