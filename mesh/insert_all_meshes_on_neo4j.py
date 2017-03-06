#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Insert all meshes in the Neo4J database
========================================
This module implements tools for generating grids based on the Postgis models into the NEO4J database.

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2017, JEM"
__license__ = "GPL"
__version__ = "0.0.8"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"


from gbif.taxonomy import GriddedTaxonomy
from gbif.models import Occurrence
from mesh.models import initMesh
from mesh.models import MexMesh
from mesh.tools import migrateGridToNeo
import logging


logger = logging.getLogger('biospytial.mesh.tools')

biosphere = Occurrence.objects.all()

## Selecting Mexico Border
from sketches.models import Country
mexico_border = Country.objects.filter(name__contains='exico').get()
mexbiosphere = biosphere.filter(geom__intersects=mexico_border.geom)


for i in range(1,11):
    # Initialize a model Mesh
    m =  initMesh(i)
    # Extract data for labeling nodes
    c = m.objects.all()[0]
    logger.info("INSERTING MESH %s IN THE GRAPH DATABASE"%c.getScaleLevel())
    # Ready... Migrate the Mesh
    migrateGridToNeo(m,intersect_with=mexico_border.geom)
     
    