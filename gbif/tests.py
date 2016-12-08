
#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Models for GBIF objects. 

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2014, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



from django.test import TestCase
from django.conf import settings
import logging
from gbif.models import Occurrence, Specie
from django.db import models
from sketches.models import Sketch
import dateutil.parser
#from models import Count,Sum,Avg
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min
from gbif.models import Specie,Genus,Family,Order,Class,Phylum,Kingdom
from mesh.models import NestedMesh
from django.contrib.gis.db.models.query import GeoQuerySet
logger = logging.getLogger('biospytial.gbif.general_test')
import biospytial.settings as settings
# Create your tests here.

from ete2 import Tree, TreeStyle
t = Tree()
ts = TreeStyle()
ts.show_leaf_name = True
ts.mode = "c"
ts.arc_start = -180 # 0 degrees = 3 o'clock
ts.arc_span = 360



    
from gbif.taxonomy import Taxonomy,embedTaxonomyInGrid,embedTaxonomyInNestedGrid,NestedTaxonomy    
    
def createShapefile(taxonomy_list,name='default_name',store='out_maps'):
    """
    This function creates a shapefile for a given list of Taxonomies.
    Do note that the list of taxonomies is a mapping to the cells in a mesh.
    """
    #Method for generating the shapefile object
    from osgeo import ogr
    #from shapely.geometry import Polygon    
    # Now convert it to a shapefile with OGR    
    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource(store)
    layer = ds.CreateLayer(name, None, ogr.wkbPolygon)
    # Add one attribute
    layer.CreateField(ogr.FieldDefn('gid', ogr.OFTInteger))
    
    layer.CreateField(ogr.FieldDefn('occurrence', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('species', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('genera', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('families', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('orders', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('classes', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('phyla', ogr.OFTInteger))
    layer.CreateField(ogr.FieldDefn('kingdoms', ogr.OFTInteger))
    
    defn = layer.GetLayerDefn()
    
    logger.info('Map layer initialized')
    ## If there are multiple geometries, put the "for" loop here
    for tax in taxonomy_list:
        try:
            d = tax.richness
            feat = ogr.Feature(defn)
            feat.SetField('gid', tax.gid)
            #logger.info('gid')
            feat.SetField('occurrence',d['occurrences'])
            feat.SetField('species', d['species'])
            #logger.info('occ')
            #logger.info('sp')
            feat.SetField('genera', d['genera'])
            #logger.info('gn')
            feat.SetField('families', d['families'])
            #logger.info('fam')
            feat.SetField('orders', d['orders'])
            #logger.info('ord')
            feat.SetField('classes', d['classes'])
            #logger.info('cls')
            feat.SetField('phyla', d['phyla'])
            #logger.info('phy')
            feat.SetField('kingdoms', d['kingdoms'])
            #logger.info('king')
            geom = ogr.CreateGeometryFromWkt(tax.biomeGeometry)
            feat.SetGeometry(geom)
            #logger.info('geom')
            layer.CreateFeature(feat)
            feat = geom = None
        except:
            logger.error('Something occurred with the feature definition')
            return False
    # Save and close everything
    ds = layer = feat = geom = None
    logger.info('Shapefile Created in %s/%s' %(store,name))
    return True

def analizeBiomeinMesh(biosphere,mesh):
    """
    This function analizes the occurrences of the gbif database with a mesh.
    Biosphere is a Geoqueryset of gbif occurrences. Mesh is a mesh type.
    Returns a Taxonomy list ready to use by createShapefile.
    """
    cells = mesh.objects.values('id','cell').all()
    #cells = map(lambda m : m.cell , m64.objects.all())
    biomes_mesh = map(lambda cell : (biosphere.filter(geom__intersects=cell['cell']),str(cell['cell']),cell['id']),cells)
    taxs_list = map(lambda biome: Taxonomy(biome[0],geometry=biome[1],id=biome[2]), biomes_mesh )
    
    map(lambda tax: tax.summary(),taxs_list)
    return taxs_list    

def TaxonomyInGrid(biosphere,mesh):
    """
    This function performs a spatial intersection and initialize Taxonomy objects with the geometry given by [mesh].
    [biosphere] is a Geoqueryset of gbif occurrences. [mesh] is a mesh type.
    Returns a Taxonomy list ready to use by createShapefile.
    """
    taxs_list = []
    if isinstance(mesh,GeoQuerySet):
        cells = mesh.values('id','cell').all()
        biomes_mesh = map(lambda cell : (biosphere.filter(geom__intersects=cell['cell']),str(cell['cell']),cell['id']),cells)
        taxs_list = map(lambda biome: Taxonomy(biome[0],geometry=biome[1],id=biome[2]), biomes_mesh )
        #logger.info(type(taxs_list))
        return taxs_list 
    else:
        cell = mesh.cell
        taxs = Taxonomy(biosphere.filter(geom__intersects=cell),geometry=cell,id=0)
        #logger.info(type(taxs_list))
        return [taxs]

def obtainAllPartialTreesInThe(nested_taxonomy):
    """
    Once a nested taxonomy has been generated. 
    (See embedTaxonomyInNestedGrid )
    This function will calculate all the partial trees for each level.
    """
    for level in nested_taxonomy.keys():
        for each_taxonomy in nested_taxonomy[level]:
            each_taxonomy.obtainPartialTree()
    return True

def calculateRelativeDistancesToParentIn(nested_taxonomy):
    """
    """
    pass


from mesh.models import mesh,initMesh



biosphere = Occurrence.objects.all()

import pickle 

nested_taxonomies = NestedTaxonomy(10417,biosphere,start_level=12,end_level=16,generate_tree_now=True)

nested_taxonomies.parent.calculateIntrinsicComplexity()

for level in range(12,17):
    nested_taxonomies.getDistancesAtLevel(level)



nt = nested_taxonomies


dets16_f = open('data_out/dets16_f.out','w')  
#parent = nested_taxonomies[12][0]
sm_f=nested_taxonomies.levels[14].taxonomies[0].forest
diff_dets_16 = map(lambda tax : [str(tax.gid)] + map(lambda n : str(n),(tax.vectorIntrinsic - tax.vectorJacobi).tolist()),nt.levels[16].taxonomies)
dets16_f.write('gid,species,genera,families,orders,classes,phyla,kingdoms\n')

from numpy import linalg as ln
import numpy as np
#first analysis was made with ...
#svd_16 = map(lambda mat : (mat.gid,ln.svd(mat.JacobiM)),nt.levels[16].taxonomies)
# for writing into a csv file
#svd_16_st = map(lambda entry : reduce(lambda a,b : a+','+b, entry),map(lambda entry : [str(entry[0])]+map(lambda t : str(t),entry[1][1].tolist()),svd_16))

p = nested_taxonomies.parent

M = p.intrinsicM

L,S,R = ln.svd(M)

I = np.identity(7)

Is = np.matrix(I*S)

lower_level = nt.levels[16]

richnesses = map(lambda t : (t.gid,t.richness.values()),lower_level.taxonomies)
for r in richnesses:
    r.sort(reverse=True)
    
# Take away occurrences

map(lambda r : r.pop(0),richnesses)
transformed_richnesses = map(lambda r : np.array(r)*L*Is,richnesses)

tr_rih_str = map(lambda l: reduce(lambda a,b : str(a)+','+str(b),l),map(lambda m : m.tolist(),transformed_richnesses))
    
rich_string = map(lambda l : reduce(lambda a,b : str(a)+','+str(b),l),tr_rih_str)

#svd_16_st = map(lambda entry : (str(entry[0]),entry[1][1].tolist()),svd_16)

df2 = open('data_out/red_dim_svd.out','w')
df2.write('gid,species,genera,families,orders,classes,phyla,kingdoms\n')
for t in rich_string:
    df2.write(t + '\n')
df2.close()

    


#vectors  = map(lambda m : m.intrinsicM*L*Is,lower_level.taxonomies)



big_tree=nested_taxonomies.parent.forest


#for d in diff_dets_16:
#    dets16_f.write(reduce(lambda a,b : a+','+b,d) + '\n')




#svd_16_st = map(lambda entry : (str(entry[0]),entry[1][1].tolist()),svd_16)

#df2 = open('data_out/dets_16_svd.out','w')
#df2.write('gid,species,genera,families,orders,classes,phyla,kingdoms\n')
#for t in svd_16_st:
#    df2.write(t + '\n')


#df2.close()




#turu =NestedMesh(528,start_level=14,end_level=14)
