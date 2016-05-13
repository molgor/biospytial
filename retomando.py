import gbif.taxonomy as tax
import mesh.tools as mt
from gbif.taxonomy import Occurrence, Taxonomy
from py2neo import Node, Relationship




def bindNode(Tree,node=False):
    child = Node(Tree.level,name=Tree.name,id=Tree.id,parent_id=Tree.parent_id,abundance=Tree.abundance)    
    if node:
        relation = Relationship(child, "IS_MEMBER_OF", node)  
        return relation  
    else:
        return child




a_p = (-106,30)

b_p = (-103,33)


d = mt.create_square_from_two_points(a_p,b_p)


biosphere = Occurrence.objects.all()

mex = biosphere.filter(geom__intersects=d['polygon'].wkt)

mextax = Taxonomy(mex,geometry=d['polygon'])


mextax.buildInnerTree(deep=True,only_id=False)


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


    
ttt = mextax.forest['sp']    