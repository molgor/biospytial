#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Module for the taxonomy operations.
Implementation of class and other necessary functions. 

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
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
logger = logging.getLogger('biospatial.gbif.taxonomy')
# Create your tests here.


from gbif.buildtree import getTOL
import biospatial.settings as settings 



import matplotlib.pyplot as plt
import numpy as np
  

def embedTaxonomyInGrid(biosphere,mesh,upper_level_grid_id=0,generate_tree_now=False):
    """
    This function performs a spatial intersection and initialize Taxonomy objects with the geometry given by [mesh].
    [biosphere] is a Geoqueryset of gbif occurrences. [mesh] is a mesh type.
    Returns a Taxonomy list ready to use by createShapefile.
    """
    taxs_list = []
    if isinstance(mesh,GeoQuerySet):
        cells = mesh.values('id','cell').all()
        try:
            biomes_mesh = map(lambda cell : (biosphere.filter(geom__intersects=cell['cell']),cell['cell'],cell['id']),cells)
        except:
            logger.error("[biospatial.gbif.taxonomy.embedTaxonomyinGrid] biosphere is not a Geoquery instance model of GBIF")
        taxs_list = map(lambda biome: Taxonomy(biome[0],geometry=biome[1],id=biome[2]), biomes_mesh )
        #logger.info(type(taxs_list))
        if generate_tree_now:
            logger.info("[biospatial.gbif.taxonomy.embedTaxonomyinGrid] generate_tree_now flag activated. Generating tree as well")
            map(lambda taxonomy: taxonomy.buildInnerTree(deep=True),taxs_list)
            map(lambda taxonomy: taxonomy.calculateIntrinsicComplexity(),taxs_list)        
        return taxs_list 
    else:
        cell = mesh.cell
        taxs = Taxonomy(biosphere.filter(geom__intersects=cell),geometry=cell,id=upper_level_grid_id)
        #logger.info(type(taxs_list))
        if generate_tree_now:
            logger.info("[biospatial.gbif.taxonomy.embedTaxonomyinGrid] generate_tree_now flag activated. Generating tree as well")
            map(lambda taxonomy: taxonomy.buildInnerTree(deep=True),[taxs])
            map(lambda taxonomy: taxonomy.calculateIntrinsicComplexity(),taxs_list)                 
        return [taxs]   


def embedTaxonomyInNestedGrid(id_in_grid,biosphere,start_level=10,end_level=11,generate_tree_now=False):
    """
    This function returns a nested taxonomies dictionary with the distinct gbif objects in each Cell.
    The id_in_grid is the index of the parent.
    start_level is the parent level of the mesh (See implementation in the mesh model)
    end_level is the last level in the nest. The bottom.
    [biosphere] is a Geoqueryset of gbif occurrences. 
    Returns a nested taxonomies dictionary 
    NOTE: The id_in_grid should be a valid index number in the set of the parent mesh.
    """
    meshes = NestedMesh(id_in_grid,start_level=start_level,end_level=end_level)
    nested_taxonomies ={} 
    for mesh in meshes.levels.keys():   
        logger.info("[biospatial.gbif.taxonomy.embedTaxonomyinNestedGrid] Embeding local biomes in grid ")
        m = meshes.levels[mesh]
        tablename = meshes.table_names[mesh]
        #taxs_list = embedTaxonomyInGrid(biosphere,m,upper_level_grid_id=id_in_grid,generate_tree_now=generate_tree_now)
        taxs = GriddedTaxonomy(biosphere,m,upper_level_grid_id=id_in_grid,generate_tree_now=generate_tree_now,grid_name=tablename)
        #taxs_list = taxs.taxonomies
        nested_taxonomies[mesh] = taxs
    return nested_taxonomies 





class Taxonomy:
    """
    Defines the taxonomic groups within one biome.
    The objective here is to make it elegant enough so everything are aueries without execution.
    """
    def __init__(self,biome,geometry='',id=0):
        """
        Biome is a query set of the gbif occurrence instance modulus a geometry in Earth.
        Geometry is a geometric attribute that could be independent of biome.
        id is an attribute for indexing the object (not in use right now).
        """
        #Initialize different aggregation levels.
        self.occurrences = biome.all()
        self.species =  biome.values('species_id').annotate(points=Collect('geom'),ab=Count('species_id'),name=Min('scientific_name'),parent_id=Min('genus_id'))
        self.genera  = biome.values('genus_id').annotate(points=Collect('geom'),ab=Count('genus_id'),name=Min('genus'),parent_id=Min('family_id'))
        self.families = biome.values('family_id').annotate(points=Collect('geom'),ab=Count('family_id'),name=Min('family'),parent_id=Min('order_id'))
        self.orders = biome.values('order_id').annotate(points=Collect('geom'),ab=Count('order_id'),name=Min('_order'),parent_id=Min('class_id'))
        self.classes  = biome.values('class_id').annotate(points=Collect('geom'),ab=Count('class_id'),name=Min('_class'),parent_id=Min('phylum_id'))
        self.phyla = biome.values('phylum_id').annotate(points=Collect('geom'),ab=Count('phylum_id'),name=Min('phylum'),parent_id=Min('kingdom_id'))
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
        self.forest = {}
        self.JacobiM = [] #This is the attribute of the Jacobian matrix calculated with respect to the distance of another matrix.
        self.vectorJacobi = [] # This is the vector form of the determinants at each submatrix.
        self.intrinsicM = []
        self.vectorIntrinsic = []
        
        
    def calculateRichness(self):
        """
        Calculates richness at all levels
        """
        inf = logger.info
        noc = self.occurrences.count()
        inf('Number of occurrences in this biome: %s' %noc)
        nsp = self.species.count()
        ngn = self.genera.count()
        inf('Number of species in this biome: %s' %nsp)
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


    def calculateIntrinsicComplexity(self):
        """
        Intrinsic Complexity is a "measure (need to proof is a measure)" of variabibility from one toxonomic level to another.
        It is makes reference only to the given (current) tree and not other external object (therefore intrinsic)
        Returns Matrix
        """
        dist = lambda i,j : 1 - float(j - i / j + i)
        dic = self.calculateRichness()
        keys = dic.keys()
        mat = []
        for i,keyi in enumerate(keys):
            rows = []
            for j , keyj in enumerate(keys):
                i = self.richness[keyi]
                j = self.richness[keyj]
                try:
                    d = dist(i,j)
                except:
                    d = float('nan')
                rows.append(d)
            mat.append(rows)
        mat = np.matrix(mat)
        self.intrinsicM = mat
        submatrices = map(lambda i : self.intrinsicM[0:i,0:i],range(1,len(self.intrinsicM)))
        self.vectorIntrinsic = map(lambda M :np.linalg.det(M),submatrices) 
        return mat





    def distanceToTree_deprec(self,taxonomic_forest,update_inner_attributes=True):
        """
        Deprecated: This method does the Robinson_foulds metric. It has been found to be not a good metric for the purposes of measuring diffrence accros scales.
        This function calculates the distance from this object to the taxonomic_forest given as input.
        The distance is based on an a given metric between all the partial trees.
        """
        #Thankfully the distance is symmetric by definition so order doesn't matter.
        Jacobian = []
        logger.warning('[FOR DEVELOPER] This is not optimized. Should be necessary to use attr_t1 and attr_t2 with name_id (integer)')
        for i in settings.TAXONOMIC_TREE_KEYS:
            F1 = []
            for j in settings.TAXONOMIC_TREE_KEYS:
                d = self.forest[i].robinson_foulds(taxonomic_forest[j],unrooted_trees=True)[0]
                F1.append(float(d))
            Jacobian.append(F1)
        if update_inner_attributes:
            self.JacobiM = np.matrix(Jacobian)
            self.Jacobi = np.linalg.det(self.JacobiM)
        return np.matrix(Jacobian)  


    def distanceToTree(self,parent_taxonomic_forest,update_inner_attributes=True):
        """
        This method implements the metric scale tree distance proposed by Escamilla-Mólgora (2015).
        parent_taxonomic_forest is the forest that is going to be compared with. 
        """ 
        Jacobian =[]
        for level_j in settings.TAXONOMIC_TREE_KEYS :
            # gradient at level level
            gradLevel = []
            for level_i in settings.TAXONOMIC_TREE_KEYS:
                # nj is the number of elements in the big scale J
                nj = float(len(parent_taxonomic_forest[level_j].get_leaves()))                
                # ni is the number of elements in the current tree (forest)
                ni = float(len(self.forest[level_i].get_leaves()))
                d_ij = ((nj - ni)/(nj + ni))
                if d_ij < 0:
                    logger.info("[biospatial.gbif.taxonomy.distanceToTree] The parent tree has less nodes than the current one.\n Perhaps the analysis is not spatially nested.")
                gradLevel.append(d_ij)
            Jacobian.append(gradLevel)
        if update_inner_attributes:
            self.JacobiM = np.matrix(Jacobian)
            submatrices_of_jacobian = map(lambda i : self.JacobiM[0:i,0:i],range(1,len(settings.TAXONOMIC_LEVELS)))
            self.vectorJacobi = map(lambda M :np.linalg.det(M),submatrices_of_jacobian) 
            
        return np.matrix(Jacobian) 
        
    #def distanceToTree


    
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
                logger.error("[biospatial.gbif.taxonomy.distanceToTree] level selected non existent (used %s)" %level)
               
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
            logger.error("[biospatial.gbif.taxonomy.getFreq] No data values for richness. \n Hint: Run Summary()")
        else:
            logger.error("[biospatial.gbif.taxonomy.getFreq] Selection not valid")
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
        
    def buildInnerTree(self,deep=False):
        """
        Calculates the tree. Is a ETE2 data type
        flag: deep=True means that is going to build all the partial trees as well.
        Partial tree is the pruned version at phylum, class, order,...,or, species
        See: taxonomy.tree attribute. 
        """
        if deep:
            self.obtainPartialTrees()
        else:
            self.forest['sp'] = getTOL(self)

    def obtainPartialTrees(self):
        """
        This method defines the partial trees for the selected taxonomic level.
        """
        
        def prune_level(tree):
            import copy
            new_tree = copy.deepcopy(tree)
            for leaf in new_tree:
                leaf.detach()
            return new_tree       
                    
        #logger.info('Pruning to genus level')
        try:
            self.forest['gns']= prune_level(self.forest['sp'])
        except:
            logger.info('[gbif.taxonomy.obtainPartialTrees()] Species level does not exist for this taxonomy (grid cell). Calculating it now!')
            self.forest['sp'] = getTOL(self)
            self.obtainPartialTrees()
        logger.info('[gbif.taxonomy.obtainPartialTrees()] Pruning trees')
        self.forest['fam']= prune_level(self.forest['gns'])
        #logger.info('Pruning to order level')
        self.forest['ord']= prune_level(self.forest['fam'])
        #logger.info('Pruning to class level')
        self.forest['cls']= prune_level(self.forest['ord'])        
        #logger.info('Pruning to phylum level')
        self.forest['phy']= prune_level(self.forest['cls'])
        #logger.info('Pruning to kingdom level')
        self.forest['kng']= prune_level(self.forest['phy'])                

    def maximumDistance(self):
        """
        This method calculates the maximum distance considering an empty tree.
        """
        from ete2 import Tree
        t = Tree(name='LUCA_root')
        empty_forest = {'sp':t,'gns':t,'fam':t,'ord':t,'cls':t,'phy':t,'kng':t}
        return self.distanceToTree(empty_forest,update_inner_attributes=False)


class GriddedTaxonomy:
    """
    This class instantiates a model based on a given grid and defines in each cell a Taxonomy object.
    There are certain attributes that gives spatial information.
    """
    def __init__(self,biosphere,mesh,upper_level_grid_id=0,generate_tree_now=False,grid_name='N.A.'):
        """
        Constructor.
        This function performs a spatial intersection and initialize Taxonomy objects with the geometry given by [mesh].
        [biosphere] is a Geoqueryset of gbif occurrences. [mesh] is a mesh type.
        Upper_level_grid is a parameter reserved for the id of the parent mesh cell.
        """
        self.taxonomies = embedTaxonomyInGrid(biosphere,mesh,upper_level_grid_id=upper_level_grid_id,generate_tree_now=generate_tree_now)
        self.extent = 'N.A.'
        self.area = 'N.A'
        self.geometry = 'N.A'
        self.grid_name = grid_name
        self.parent_id = upper_level_grid_id
        self.dArea = self.taxonomies[0].biomeGeometry.area
        #self.mesh = ''
        #FALTA ACABAR ESTO A CADA NIVEL DARLE ATRIBUTOS DE NOMBRE DEL MESH, DIFERENCIAL DE AREA , id del mesh tal vez.
        # Distancia a la referencia ,etc. 
        #Matriz jacobiana de distancias.
        # aqui habra que meterle un constructor que regrese matrices o tensores.

    def __str__(self):
        return u"GriddedTaxonomy layer: \n Extent: %s" %self.geometry.extent     
        
    def __repr__(self):
        cad = "<GriddedTaxonomy instance: %s@%s >" %(self.parent_id,self.grid_name)
        return cad
        
   
    def createShapefile(self,option='richness',store='out_maps'):
        """
        This function creates a shapefile using a selected attribute.
        option is the attribute to export.
        Currently implemented:
            richness (default) gives the counts of occurrences at each taxonomic level.
            jacobi: gives the determinant of the distance (Escamilla) matrix and sub-matrices from the 7x7 size to the 2x2.
                    a layer for each determinant of each submatrix.
        """
        import ipdb
        def selectRichness(layer):
            # This is for option richness
            for key in settings.TAXONOMIC_LEVELS:
                layer.CreateField(ogr.FieldDefn(key,ogr.OFTInteger))        
            defn = layer.GetLayerDefn()
                   
            ## If there are multiple geometries, put the "for" loop here
            for tax in self.taxonomies:
                #logger.debug("there are %s taxonomies" %(len(self.taxonomies)))
                tax.calculateRichness()
                try:
                    #ipdb.set_trace()
                    d = tax.richness
                    feat = ogr.Feature(defn)
                    feat.SetField('gid', tax.gid)
                    
                    #logger.debug('gid')
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
                    geom = ogr.CreateGeometryFromWkt(tax.biomeGeometry.wkt)
                    feat.SetGeometry(geom)
                    #logger.info('geom')
                    layer.CreateFeature(feat)
                    feat = geom = None
                except:
                    logger.error('[biospatial.gbif.taxonomy.GriddedTaxonomy]\n\n Something occurred with the feature definition \n See: gbif.GriddedTaxonomy.createShapefile')
                    return False
            return True
            
                    
        #Method for generating the shapefile object
        
        
        def selectJacobi(layer):
            # Calculate distance.
            keys = ['s','sg','sgf','sgfo','sgfoc','sgfocp','sgfocpk']
            for key in keys:
                layer.CreateField(ogr.FieldDefn(key,ogr.OFTReal))        
            defn = layer.GetLayerDefn()
                   
            ## If there are multiple geometries, put the "for" loop here
            for idx,tax in enumerate(self.taxonomies):
                #logger.debug("there are %s taxonomies" %(len(self.taxonomies)))
                if not isinstance(tax.JacobiM,np.matrixlib.defmatrix.matrix):
                    logger.error("[biospatial.gbif.taxonomy.NestedTaxonomy] \nDistance Matrix hasn't been defined.\n Try running NestedTaxonomy.getDistancesAtLevel(level) or GriddedTaxonomy.distanceToTree(arbitray_tax_forest)")
                    raise Exception("Distance Matrix not defined")
                    return None
                else:
                    try:
                        #ipdb.set_trace()
                        d = tax.vectorJacobi
                        feat = ogr.Feature(defn)
                        
                        for i,key in enumerate(keys):
                            feat.SetField(key,d[i] )
                        geom = ogr.CreateGeometryFromWkt(tax.biomeGeometry.wkt)
                        feat.SetGeometry(geom)
                        #logger.info('geom')
                        layer.CreateFeature(feat)
                        feat = geom = None
                    except:
                        logger.error('[biospatial.gbif.taxonomy.NestedTaxonomy] \nSomething occurred with the feature definition \n See: gbif.GriddedTaxonomy.createShapefile')
                        return False
            return True
        

        def selectIntrisic(layer):
            # Calculate distance.
            keys = ['o','os','osg','osgf','osgfo','osgfoc','osgfocp','osgfocpk']
            for key in keys:
                layer.CreateField(ogr.FieldDefn(key,ogr.OFTReal))        
            defn = layer.GetLayerDefn()
                   
            ## If there are multiple geometries, put the "for" loop here
            for idx,tax in enumerate(self.taxonomies):
                #logger.debug("there are %s taxonomies" %(len(self.taxonomies)))
                if not isinstance(tax.intrinsicM,np.matrixlib.defmatrix.matrix):
                    logger.error("[biospatial.gbif.taxonomy.NestedTaxonomy] \n Intrinsic Matrix hasn't been defined.")
                    raise Exception("Intrinsic Matrix not defined")
                    return None
                else:
                    try:
                        #ipdb.set_trace()
                        d = tax.vectorIntrinsic
                        feat = ogr.Feature(defn)
                        
                        for i,key in enumerate(keys):
                            feat.SetField(key,d[i] )
                        geom = ogr.CreateGeometryFromWkt(tax.biomeGeometry.wkt)
                        feat.SetGeometry(geom)
                        #logger.info('geom')
                        layer.CreateFeature(feat)
                        feat = geom = None
                    except:
                        logger.error('[biospatial.gbif.taxonomy.NestedTaxonomy] \nSomething occurred with the feature definition \n See: gbif.GriddedTaxonomy.createShapefile')
                        return False
            return True


        
        
        from osgeo import ogr
        #from shapely.geometry import Polygon    
        # Now convert it to a shapefile with OGR    
        driver = ogr.GetDriverByName('Esri Shapefile')
        ds = driver.CreateDataSource(store+self.grid_name)
        layer = ds.CreateLayer(option, None, ogr.wkbPolygon)
        logger.info('[biospatial.gbif.taxonomy.GriddedTaxonomy]\n Creating Shapefile %s' %option+'@'+store)
        
        if option == 'richness':
            selectRichness(layer)  
        elif option == 'jacobi':
            selectJacobi(layer)
        # Save and close everything
        ds = layer = feat = geom = None
        logger.info('[biospatial.gbif.taxonomy.GriddedTaxonomy]\n Shapefile Created in %s/%s' %(store,option))
        return True
    
    def mergeGeometries(self):
        """
        Return a polygon made by the union of all the cells in the gridded taxonomy.
        """
        self.geometry = reduce(lambda p1,p2 : p1.union(p2) ,map(lambda tax : tax.biomeGeometry,self.taxonomies))
        return self.geometry
        
    def getArea(self):
        try:
            self.area = self.geometry.area
            return self.area
        except:
            logger.error('Geometry hasn\'t been defined (instantiate mergeGeometries first!)')
            return None
        
    def distanceToTree(self,taxonomic_forest):
        """
        Calculates the distance from each taxonomy in the grid compared with an arbitrary taxonomic tree.
        See gbif.taxonomy.distanceToTree()
        Note: taxonomic_forest is a dictionary which uses keys: ['sp','gns','fam','ord','cls','phy','kng']
        This can be seen in the biospatial.settings file.
        """
        
        matrices = map(lambda tax : tax.distanceToTree(taxonomic_forest),self.taxonomies)
        return matrices

        
    
class NestedTaxonomy:
    """
    This class instantiates nested taxonomies.
    Parameters:
    id = Cell's id of the parent level (start_level).
    gbif_queryset = an instance of the gbif database, could be a prefiltered one (e.g. a biome )
    start_level = level id of the parent mesh level. See: gbif.mesh.NestedMesh and biospatial.settings
    end_level = level id for the bottom of the stack.
    generate_tree_now = [True,False] to generate the trees and subtrees of eac taxonomic level in each cell.
    """  
    def __init__(self,id,gbif_geoqueryset,start_level=12,end_level=14,generate_tree_now=True):
        self.levels = embedTaxonomyInNestedGrid(id,gbif_geoqueryset,start_level=start_level,end_level=end_level,generate_tree_now=generate_tree_now) 
        self.parent = self.levels[self.levels.keys()[0]].taxonomies[0]
        self.maxdistances = self.getMaximumDistances()
        
    def __repr__(self):
        cad = '<gbif.taxonomy.NestedTaxonomy instance with levels: %s>' %str(self.levels)    
        return cad
    
    def getLevels(self):
        """
        Gives the available zooming levels in the current Nested Taxonomy.
        """
        a = str(self.levels.keys())
        logger.info('[biospatial.gbif.taxonomy.NestedTaxonomy]\n Available Levels %s' %a)
        return a
        

    def getDistancesAtLevel(self,level,parent_forest='Top'):
        """
        This method calculates all the Jacobian matrices comparing the parent tree woth the specfied level.
        """
        if parent_forest == 'Top':
            parent_forest = self.parent.forest
        try:
            mats = self.levels[level].distanceToTree(parent_forest)
            return mats
        except:
            logger.error('[biospatial.gbif.taxonomy.NestedTaxonomy] \nSomethng went wrong. Perhaps the selected level doesn\'t exist for this NestedTaxonomy')
            return None
        

    def getMaximumDistances(self):
        """
        This method calculates the maximum distance that a tree has 
        """
        pass