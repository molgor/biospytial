#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
Guideline for Manipulating Biospytial Data Types

"""

# Go to QGIS, Connect the database (postgis) 
# Explore the scale and cell we want.

#E.g. Cell 627 in Mesh6 (mexico_grid32) 

from mesh.models import initMesh

m = initMesh(6)
cell = m.objects.get(id=625)

border = cell.cell

### Now, lets get a Taxonomy out of this.



from gbif.taxonomy import Taxonomy
from gbif.models import Biome






## Init signature: 
  ### Taxonomy(self, biome, geometry='', id=-999, build_tree_now=True, grid_label_name='generic')
## init 
# But we need to define previously biome and geometry

#biome_in_cell = Occurrence.objects.filter(geom_border)

## Ok now we can load it
biome = Biome(intersects_with=border).selection


tax0 = Taxonomy(biome=biome,geometry=border,build_tree_now=False)
## Note the build_tree_now flag on

## We can build the tree from the Rel. DB
#%time tax0.generateTREE()
#CPU times: user 12.2 s, sys: 388 ms, total: 12.6 s
#Wall time: 32.7 s

#tax0 = Taxonomy(biome=biome,geometry=border)#