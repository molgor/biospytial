from django.test import TestCase

# Create your tests here.
from mesh import initMesh

import mesh.tools as mt
#meshes = map(lambda i : initMesh(i),range(8,18))
#m12 = initMesh(12)
#mesh12= m12.objects.all()
from mesh.tools import createRegionalNestedGrid


a_p = (-119,33)

b_p = (-85,1)

p1 = (-119,33)
p2 = (-85,33)
p3 = (-85,1)
p4 = (-119,1)
p5 = p1
coords = (p1,p2,p3,p4,p5)
poly2 = mt.Polygon(coords)


d = mt.create_square_from_two_points(b_p,a_p,)

## For creating Regional Nested grid just do :
scales = createRegionalNestedGrid(parent_square=poly2.wkt,store_prefix='mexico_grid',n_levels=9)