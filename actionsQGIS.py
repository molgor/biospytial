#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
This file is intented to implent selected specific comand-line tools for using it with QGIS.
This will be an interfce between biospatial and QGIS

"""

__author__ = "Juan Escamilla M�lgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"

import logging
import sys
import getopt
from mesh.models import NestedMesh,initMesh
from django.contrib.gis.db.models.query import GeoQuerySet
from gbif.models import Occurrence, Specie
from gbif.taxonomy import GriddedTaxonomy
from django.core.management.base import BaseCommand, CommandError
import os
import sys

#sys.path.append('/home/username/www/site_folder')
os.environ['DJANGO_SETTINGS_MODULE'] = 'biospatial.settings'


from django.utils import unittest

from django.test.client import Client

logger = logging.getLogger('biospatial.actionsQGIS')

from ete2 import Tree, TreeStyle


def showTreeInGrid(gid,biome,grid_level=14,taxonomic_level='sp'):
    """
    Performs a selection, spatial filter and returns an image.
    grid_level is the grid layer.
    taxonomic_level is the taxonomic level to be shown. Options are:
    sp, gns, fam, ord, cls, phy, king
    """
    
    mesh = initMesh(grid_level)
    try:
        cell = mesh.objects.get(id=id)
    except:
        logger.error("Selected id does not exist in selected grid")
        return None
    
    gb=GriddedTaxonomy(biome,cell,generate_tree_now=True)
    forest = gb.taxonomies[0].forest

    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.mode = "c"
    ts.arc_start = -180 # 0 degrees = 3 o'clock
    ts.arc_span = 360

    forest[taxonomic_level].show(tree_style=ts)
    return 'Parece que se tiene que ver algo'





class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
            
        except getopt.error, msg:
             raise Usage(msg)
        # more code, unchanged
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    biosphere = Occurrence.objects.all() 
    showTreeInGrid(argv[1],biosphere,taxonomic_level='sp')


if __name__ == "__main__":
    sys.exit(main())



  