#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gbif.taxonomy as tax
import mesh.tools as mt
from gbif.taxonomy import Occurrence, Taxonomy, GriddedTaxonomy
from py2neo import Node, Relationship, Graph
from mesh.models import initMesh
from gbif.models import Specie
from mesh.tools import migrateGridToNeo
#g = Graph("http://localhost:7474/db/data/")
#tx = g.begin()



def bindNode(Tree,node=False):
    child = Node(Tree.level,name=Tree.name,id=Tree.id,parent_id=Tree.parent_id,abundance=Tree.abundance)    
    if node:
        relation = Relationship(child, "IS_MEMBER_OF", node)  
        return relation  
    else:
        return child



def getNeighbours(cell_center,mesh):
    neighbours = mesh.objects.filter(cell__touches=cell_center.cell)
    
    return (cell_center,neighbours)



def createNetworkOnNode(duple_center_neighbour,writeInDB=False):
    center = duple_center_neighbour[0]
    neighbours = duple_center_neighbour[1]
    n0 = Node("Cell",**center.describeWithDict())
    nn = [ Relationship(n0,"IS_NEIGHBOUR_OF",Node("Cell", **n.describeWithDict())) for n in neighbours]
    if writeInDB:
        for relationship in nn:
            g.create(relationship)
    return nn


a_p = (-106,30)

b_p = (-103,33)


d = mt.create_square_from_two_points(a_p,b_p)


biosphere = Occurrence.objects.all()

mex = biosphere.filter(geom__intersects=d['polygon'].wkt)



#mextax.buildInnerTree(deep=True,only_id=False)


#dics = mt.createRegionalNestedGrid(d['polygon'].wkt,'testmesh',7)
#################
### GENERATE  
{0: 'mesh"."testmesh1',
 1: 'mesh"."testmesh2',
 2: 'mesh"."testmesh4',
 3: 'mesh"."testmesh8',
 4: 'mesh"."testmesh16',
 5: 'mesh"."testmesh32',
 6: 'mesh"."testmesh64'}


    
#ttt = mextax.forest['sp']    


#Problems found!
#First bring mesh 

mmm = initMesh(4)
ggg = GriddedTaxonomy(mex,mmm.objects.all(),generate_tree_now=False,use_id_as_name=False)

mextax = Taxonomy(mex,geometry=d['polygon'],build_tree_now=False)

#sys.path.append("/home/juan/miniconda2/pkgs/gdal-2.0.0-py27_1/lib/python2.7/site-packages/osgeo")

#t =  ggg.taxonomies[0]

#vecinos = [getNeighbours(c,mmm) for c in mmm.objects.all()]

#nodos = [Node("Cell",**n.describeWithDict()) for n in mmm.objects.all()]

#If an attempt is made to create two nodes with similar unique property values, an exception will be raised and no new node will be created. To ‘get or create’ a node with a particular label and property, the merge_one method can be used instead:

#m = map(createNetworkOnNode,vecinos)

## Create unique constraint with concatenated labels
g = Graph()

g.schema.create_uniqueness_constraint("Root","id")
g.schema.create_uniqueness_constraint("Kingdom","keyword")
g.schema.create_uniqueness_constraint("Phylum","keyword")
g.schema.create_uniqueness_constraint("Class","keyword")
g.schema.create_uniqueness_constraint("Order","keyword")
g.schema.create_uniqueness_constraint("Family","keyword")
g.schema.create_uniqueness_constraint("Genus","keyword")
g.schema.create_uniqueness_constraint("Specie","keyword")
g.schema.create_uniqueness_constraint("Occurrence","pk")





#t =  ggg.taxonomies[0]
#t.TREE.migrateToNeo4J()


def bindTaxonomyToMesh(gridded_taxonomy,graph_driver):
    l = []
    for t in gridded_taxonomy:
        nodecell = graph_driver.find_one("Cell","id",t.gid)
        rel = Relationship( t.TREE.getNode(),"IS_IN",nodecell)
        l.append(rel)
    return l


#PARA CREAR EL GRID VE A TOOLS EN MESH Y CHECA migrateGridToNeo    

#g.schema.create_uniqueness_constraint("Cell","uniqueid")
#t=[[g.merge(i) for i in n] for n in m]
#
#m = map(lambda rel : createNetworkOnNode(rel,writeInDB=True),vecinos)

