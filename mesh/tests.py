from django.test import TestCase

# Create your tests here.
from mesh import initMesh

#meshes = map(lambda i : initMesh(i),range(8,18))

m12 = initMesh(12)
mesh12= m12.objects.all()
