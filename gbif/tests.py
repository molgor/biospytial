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

logger = logging.getLogger('biospatial.gbif')
# Create your tests here.






def aggregateTaxons(GBIF_QuerySet,taxonomic_level=1):
    """
    This function aggregates the GBIF objects according to the given taxonomic level.
    The taxonomic level is an integer which ranges from:
    Kingdom : 0
    Phylum : 1
    Order : 2
    Class : 3
    Family : 4
    Genus : 5
    Species : 6
    Default value is 6 [species]
    It return a list with the aggregated classes, the number of aggregated items per class and a Multipolygon geometry that comprises the aggregation.
    """
    levels = [{'kingdom':['kingdom_id','kingdom']},
              {'phylum' : ['phylum_id','phylum']},
              {'order' : ['order_id','_order']},
              {'class' : ['class_id','_class']},
              {'family' : ['family_id','family']},
              {'genus' : ['genus_id','genus']},
              {'species' : ['species_id','scientific_name']}
              ]
    try:
        selection = levels[taxonomic_level]
    except:
        logger.error("Chosen taxonomic level not existing %s. See documentation" %taxonomic_level)
        return False          
    level = selection.keys().pop()
    logger.debug('Aggregation level selected %s \n' %level)
    gqs = GBIF_QuerySet
    tax_id = selection[level][0]
    tax_featurename = selection[level][1]
    try: 
        taxons = gqs.values(tax_id).annotate(occurrences=Collect('geom'),num_occur=Count(tax_id),species_name=Min(tax_featurename))
    except:
        logger.error("Bad request on GBIF_QuerySet. Either is not a QuerySet object from Occurrence Class or there is something wrong. Check code.")
        return False
    return taxons

# species = biome.values('species_id').annotate(occurrences=Collect('geom'),num_occur=Count('species_id'),species_name=Min('scientific_name'))
#orders = families.values('order_id').annotate(Collect('geom'),num_fams=Count('order_id'),order_name=Min('_order'))
#classes = orders.values('class_id').annotate(Collect('geom'),num_orders=Count('class_id'),class_name=Min('_class'))
#phylums = classes.values('phylum_id').annotate(Collect('geom'),num_class=Count('phylum_id'),phylum_name=Min('phylum'))
#kingdoms = phylums.values('kingdom_id').annotate(Collect('geom'),num_phylums=Count('kingdom_id'),kingdom_name=Min('kingdom'))



def getTaxonomicQueries(biome):
    tq= {}
    tq['species']= biome.values('species_id').annotate(points=Collect('geom'),ab=Count('species_id'),name=Min('scientific_name'))

    tq['genuses'] = biome.values('genus_id').annotate(points=Collect('geom'),ab=Count('genus_id'),name=Min('genus'))

    tq['families'] = biome.values('family_id').annotate(points=Collect('geom'),ab=Count('family_id'),name=Min('family'))

# kingdoms = biome.values('kingdom_id').values('phylum_id').values('order_id').values('class_id').values('family_id').values('genus_id').values('species_id').annotate(Collect('geom'),num_phylums=Count('kingdom_id'),kingdom_name=Min('kingdom'))

    tq['classes'] = biome.values('class_id').annotate(points=Collect('geom'),ab=Count('class_id'),name=Min('_class'))

    tq['orders'] = biome.values('order_id').annotate(points=Collect('geom'),ab=Count('order_id'),name=Min('_order'))

    tq['phyla'] = biome.values('phylum_id').annotate(points=Collect('geom'),ab=Count('phylum_id'),name=Min('phylum'))

    tq['kingdoms'] = biome.values('kingdom_id').annotate(points=Collect('geom'),ab=Count('kingdom_id'),name=Min('kingdom'))

    return tq

import matplotlib.pyplot as plt
import numpy as np
  

class Taxonomy:
    """
    DEfines the taxonomic groups within one biome.
    The objective here is to make it elegant enough so everything are aueries without execution.
    """
    def __init__(self,biome,geometry='',id=0):
        """
        Biome is a local query set of the gbif occurrence instance
        """
        self.occurrences = biome.all()
        self.species =  biome.values('species_id').annotate(points=Collect('geom'),ab=Count('species_id'),name=Min('scientific_name'))
        self.genera  = biome.values('genus_id').annotate(points=Collect('geom'),ab=Count('genus_id'),name=Min('genus'))
        self.families = biome.values('family_id').annotate(points=Collect('geom'),ab=Count('family_id'),name=Min('family'))
        self.classes  = biome.values('class_id').annotate(points=Collect('geom'),ab=Count('class_id'),name=Min('_class'))
        self.orders = biome.values('order_id').annotate(points=Collect('geom'),ab=Count('order_id'),name=Min('_order'))
        self.phyla = biome.values('phylum_id').annotate(points=Collect('geom'),ab=Count('phylum_id'),name=Min('phylum'))
        self.kingdoms = biome.values('kingdom_id').annotate(points=Collect('geom'),ab=Count('kingdom_id'),name=Min('kingdom'))
        self.rich_occurrences = 0
        self.rich_species = 0
        self.rich_genera = 0
        self.rich_families = 0
        self.rich_classes = 0
        self.rich_orders = 0
        self.rich_phyla = 0
        self.rich_kingdoms = 0
        self.richness ={ 'occurrences' : self.rich_occurrences,
            'species' : self.rich_species,
            'genera' : self.rich_genera,
            'families': self.rich_families,
            'classes' : self.rich_classes,
            'orders' : self.rich_orders,
            'phyla' : self.rich_phyla,
            'kingdoms' : self.rich_kingdoms
            }
        self.biomeGeometry = geometry
        self.gid = id
        

    def summary(self):
        """
        Gives the summary of the biome.
        """
        inf = logger.info
        noc = self.occurrences.count()
        inf('Number of occurrences in this biome: %s' %noc)
        nsp = self.species.count()
        inf('Number of species in this biome: %s' %nsp)
        ngn = self.genera.count()
        inf('Number of genera in this biome: %s' %ngn)   
        nfa = self.families.count()
        inf('Number of families in this biome: %s' %nfa)
        nor = self.orders.count()
        inf('Number of orders in this biome: %s' %nor)        
        ncl = self.classes.count()
        inf('Number of classes in this biome: %s' %ncl)
        nph = self.phyla.count()
        inf('Number of orders in this biome: %s' %nph)
        nki = self.kingdoms.count()
        inf('Number of kingdoms in this biome %s' %nki)
        self.richness ={ 'occurrences' : noc,
               'species' : nsp,
            'genera' : ngn,
            'families': nfa,
            'classes' : ncl,
            'orders' : nor,
            'phyla' : nph,
            'kingdoms' : nki
            }
        
        return self.richness
    

    def generatePDI(self,level='species',type='richness'):
        """
        This method calculates partial diversity index based on the index level and the type.
        type =  richness :: richness index.
                abundance :: 
                relative_abundance
        """
        if type == 'richness':
            import biodiversity.richness as rich
            pdi = rich(self)
            try:
                return pdi[level]
            except:
                logger.error("level selected non existent (used %s)" %level)
            
    
    
    def getFreqs(self,sel='richness'):
        """
        This function returns a graph of richness, abundance or relative abundance.
        The abundance function depends on the total number of occurrences within that polygon.
        The relative abundance function depends on the number of the lower taxonomic level.
        """
        dic_tax = self.richness
        N = 7
        ind = np.arange(N)
        #width = 0.35
        width = 0.90
        noc = dic_tax['occurrences']  
        l = ['species','genera','families','orders','classes','phyla','kingdoms']
        try:
            if sel == 'abundance':
                values = map(lambda x : dic_tax[x] / float(noc),l)
                color = 'b'
            elif sel == 'richness':
                values = map(lambda x : dic_tax[x],l)
                color = 'r'
            elif sel == 'rel_abundance':
                val1 = map(lambda x : dic_tax[x],l)
                ## WARNING THISIS ASSUMIG THE MAXIMUM NUMBER OF KINGDOMS IN EARTH
                val2 = (val1[1:7] + [5])
                values = map(lambda tup : tup[0] / float(tup[1]) , zip(val2,val1))
                color = 'g'
        except:
            logger.error("No data values for richness. \n Hint: Run Summary()")
        else:
            logger.error("Selection not valid")
            return False
        fig, ax = plt.subplots()
        bar = ax.bar(ind, values, width, color=color)
        #bar = ax.bar(ind, values, color='r')

        # add some text for labels, title and axes ticks
        ax.set_ylabel(sel)
        ax.set_title('Scores by taxonomic level')
        ax.set_xticks(ind+(width/2))
        ax.set_xticklabels( l )
        plt.show()
        return ax
        

    
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
    







from mesh.models import mesh,initMesh
#mp = mesh.objects.filter(hemi__intersects=cell)
mesh._meta.db_table = 'mesh"."grid8a'
polygon=mesh.objects.filter(pk=44)[0].cell


sketches = Sketch.objects.all()
plgn = sketches[1].geom

# Grouping shit
#r = sp.objects.values('family').annotate(total=Count('scientific_name'))

biosphere = Occurrence.objects.all()

#newPoints=biome.values('kingdom').values('species_id').annotate(points=Collect('geom'))

#biome = biosphere.filter(geom__intersects=plgn)

#biome1 = biosphere.filter(geom__intersects=polygon)
#m64 = initMesh(11)
#cells = m64.objects.values('id','cell').all()
#cells = map(lambda m : m.cell , m64.objects.all())

#for i in range(8,17):
 #   logger.info("Comenzando con mesh %s" %i)
  #  mesh = initMesh(i)
   # taxs_list = analizeBiomeinMesh(biosphere,mesh)
    #createShapefile(taxs_list,name='taxs_'+str(i))



#tax = Taxonomy(biome1) 


#r=species[0]
#s=Specie(biome,r)

#genus = map(lambda g : Genus(biome,g),genuses[1:10])

#fams = map(lambda f : Family(biome,f),families)

#classex = map(lambda c: Class(biome,c),classes[1:6])
#phyls = map(lambda p: Phylum(biome,p),phylums[1:2])
#kings = map(lambda k : Kingdom(biome,k),kingdoms[1:2])
#orderes = map(lambda o: Order(biome,o),orders[1:10])


