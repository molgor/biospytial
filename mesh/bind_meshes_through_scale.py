#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Bind meshes through scale
=========================
This script will create the links (edges) into the Neo database to bind CELL nodes through
scale based on the topological relationship: IS_CONTAINED_IN.

Check thath the bottom mesh (mex4km) is not a "standard" meshed derived from partitioning the mesh in
a quadtree but it's one created at 4km resolution (approx).

To see the logic behind in selecting the parent polygon (because it's not a funcion , originally) see the method:
rankIntersections in mesh.models.MexMesh

This module implements tools for generating grids based on polygons.

"""


__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "0.0.8"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Unstable"




from gbif.taxonomy import GriddedTaxonomy, NestedTaxonomy
from gbif.models import Occurrence
from mesh.models import initMesh
from mesh.models import MexMesh
from mesh.tools import migrateGridToNeo
import logging
import biospytial.settings as settings
from py2neo import Graph, NodeSelector,Relationship

logger = logging.getLogger('biospytial.mesh.tools')


neoparams = settings.NEO4J_DATABASES['default']
uri = "http://%(HOST)s:%(PORT)s%(ENDPOINT)s" % neoparams
graph = Graph(uri)
node_selector = NodeSelector(graph)



#m1 = initMesh(7)
#m1
#m1.objects.all()
biosphere = Occurrence.objects.all()


from sketches.models import Country
mexico_border = Country.objects.filter(name__contains='exico').get()
mexbiosphere = biosphere.filter(geom__intersects=mexico_border.geom)


meshes = map(lambda i : initMesh(i), range(1,12))
logger.info("Creating and filtering Meses with the Mexico border.")

filtermex = lambda mesh_ : mesh_.objects.filter(cell__intersects=mexico_border.geom)

## list of filetered meshes.
mexmeshes = map(filtermex,meshes)



    
## This get the nodes cell and parent
getRelations_per_cell = lambda cell : (cell,cell.parentCell)

# This constructs the Relation object for each part.
defineRelation =  lambda (cell,parent) : Relationship(cell.getNode(),"IS_CONTAINED_IN",parent.getNode())

# wraps two functions
giveEdge = lambda cell : defineRelation(getRelations_per_cell(cell))

# Do this for all the cells in the map.
relations_in_mesh = lambda single_mesh : map(giveEdge,single_mesh)



## Insert the relations into the database
def insertRelationship(relations_in_mesh,graph_driver):
    list_ = relations_in_mesh
    n = len(list_)
    graph = graph_driver
    for i,r in enumerate(list_):
        graph.create(r)
        logger.info("Created. rel %s of %s"%(i,n))
    return None


main_for_single_mesh = lambda mesh_ : insertRelationship(relations_in_mesh(mesh_),graph)

Insert_ALL_meshes = lambda list_meshes : map(main_for_single_mesh,list_meshes)

upper = mexmeshes.pop(0)

## Just RUn this!
#Insert_ALL_meshes(mexmeshes)



