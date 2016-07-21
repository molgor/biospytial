#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Taxonomy module
===============

.. Taxonomy_module_intro:
This is the core module of the Biospytial suite.

In this module you will find the definition for classes, and nested taxonomies
for data aggregation, hierarchication and processing.
 
"""
from django.db.models.aggregates import Aggregate


__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "0.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"


from py2neo import Graph, Relationship 
from django.test import TestCase
from django.conf import settings
import logging
from gbif.models import Occurrence, Specie, Genus, Family, Order, Class, Phylum, Kingdom
from django.db import models
from sketches.models import Sketch
import dateutil.parser
#from models import Count,Sum,Avg
from django.contrib.gis.db.models import Extent, Union, Collect,Count,Min
from gbif.models import Specie,Genus,Family,Order,Class,Phylum,Kingdom,Root
from mesh.models import NestedMesh
from django.contrib.gis.db.models.query import GeoQuerySet
logger = logging.getLogger('biospatial.gbif.taxonomy')
# Create your tests here.

from raster_api.tools import RasterData
from gbif.buildtree import getTOL
import biospatial.settings as settings 

import pickle

#import matplotlib.pyplot as plt
import numpy as np

graph_driver = Graph()
  

def embedTaxonomyInGrid(biosphere,mesh,upper_level_grid_id=0,generate_tree_now=False,use_id_as_name=True):
    """
    .. embedTaxonomyInGrid:
    This function performs a spatial intersection and initializes Taxonomy objects with the geometry given by a mesh.
    
    
    Parameters
    ----------
    biosphere : Geoqueryset
        Is the Geoqueryset of gbif occurrences
    mesh : mesh type
        The mesh (grid) where the taxonomy is going to be defined

    generate_tree_now : Boolean (default True)
        This is a flag and when True means that it will create on the flag the Tree representation.
        This is computationally intensive because, in order to do so, it will query all the objects 
        in all the Cells in the Gridded Taxonomies in all the Gridded Levels in the Nested Grid.


    use_id_as_name: boolean (default True)
        This is a flag and when True means that the nodes in the trees are going to be named
        according to the identifier (Integer) instead of the full string name.
        Saves memory.

    
    Returns
    -------    
    taxs_list : list
        A taxonomies list
        
    See also
    --------
    gbif.taxonomy.GriddedTaxonomy
    """
    taxs_list = []
    if isinstance(mesh,GeoQuerySet):
        cells = mesh.values('id','cell').all()
        try:
            biomes_mesh = map(lambda cell : (biosphere.filter(geom__intersects=cell['cell']),cell['cell'],cell['id']),cells)
        except:
            logger.error("[biospatial.gbif.taxonomy.embedTaxonomyinGrid] biosphere is not a Geoquery instance model of GBIF")
        taxs_list = map(lambda biome: Taxonomy(biome[0],geometry=biome[1],id=biome[2],build_tree_now=generate_tree_now), biomes_mesh )
        #logger.info(type(taxs_list))
        if generate_tree_now:
            logger.info("[biospatial.gbif.taxonomy.embedTaxonomyinGrid] generate_tree_now flag activated. Generating tree as well")
            map(lambda taxonomy: taxonomy.buildInnerTree(deep=True,only_id=use_id_as_name),taxs_list)
            map(lambda taxonomy: taxonomy.calculateIntrinsicComplexity(),taxs_list)        
        return taxs_list 
    else:
        cell = mesh.cell
        taxs = Taxonomy(biosphere.filter(geom__intersects=cell),geometry=cell,id=upper_level_grid_id,build_tree_now=generate_tree_now)
        #logger.info(type(taxs_list))
        if generate_tree_now:
            logger.info("[biospatial.gbif.taxonomy.embedTaxonomyinGrid] generate_tree_now flag activated. Generating tree as well")
            map(lambda taxonomy: taxonomy.buildInnerTree(deep=True,only_id=use_id_as_name),[taxs])
            map(lambda taxonomy: taxonomy.calculateIntrinsicComplexity(),taxs_list)                 
        return [taxs]   


def embedTaxonomyInNestedGrid(id_in_grid,biosphere,start_level=10,end_level=11,generate_tree_now=False,use_id_as_name=True):
    """
    .. embedTaxonomyInNestedGrid:
    
    Summary
    -------
    This function returns a nested taxonomies dictionary with distinct gbif objects in each gridcell.
    
    Parameters
    ----------
    id_in_grid : int
        This is the index of the cell corresponding to the top level grid (i.e. parent cell).
    biosphere : Geoqueryset
        This is the Geoqueryset of gbif occurrences
    start_level : int
        This is the scale level to start, the parent level of the mesh :ref: mesh.models    
    end_level : int 
        This is the last level in the nested grid stack, i.e. the bottom

    generate_tree_now : Boolean (default True)
        This is a flag and when True means that it will create on the flag the Tree representation.
        This is computationally intensive because, in order to do so, it will query all the objects 
        in all the Cells in the Gridded Taxonomies in all the Gridded Levels in the Nested Grid.
    
    use_id_as_name: boolean (default True)
        This is a flag and when True means that the nodes in the trees are going to be named
        according to the identifier (Integer) instead of the full string name.
        Saves memory.

    Returns
    -------
    nested taxomies : dictionary
    
    Note
    ----
    The id_in_grid should be a valid index number in the set of the parent mesh.
    
    See also
    --------
    gbif.taxonomy.NestedGriddedTaxonomy

    """
    meshes = NestedMesh(id_in_grid,start_level=start_level,end_level=end_level)
    nested_taxonomies ={} 
    for mesh in meshes.levels.keys():   
        logger.info("[biospatial.gbif.taxonomy.embedTaxonomyinNestedGrid] Embeding local biomes in grid ")
        m = meshes.levels[mesh]
        tablename = meshes.table_names[mesh]
        #taxs_list = embedTaxonomyInGrid(biosphere,m,upper_level_grid_id=id_in_grid,generate_tree_now=generate_tree_now)
        taxs = GriddedTaxonomy(biosphere,m,upper_level_grid_id=id_in_grid,generate_tree_now=generate_tree_now,grid_name=tablename,use_id_as_name=use_id_as_name)
        #taxs_list = taxs.taxonomies
        nested_taxonomies[mesh] = taxs
    return nested_taxonomies 


"""



"""

class Presence:
    
    
    def __init__(self,presence_list):
        self.map = presence_list
        self.keys = map(lambda x : x[0] ,self.map)
        self.list = map(lambda x : x[1] ,self.map)

    
    def __str__(self):
        """
        String representation (cast) of the Presence Class
        """
        
        return reduce(lambda a,b : str(a)+str(b),self.list)
        
    def BitArray(self):
        """
        ..
        
        Returns a BitArray representation of the current Presence.
        The maximum being the integer represented by all the entries = 1 in the 'list' attribute.
        
        .. note:: This method converts the presence/absence list to a BinaryString data.
        """
        from bitstring import BitArray,BitStream
        b = BitArray(bin=str(self))
        return b
    
    def __int__(self):
        return self.BitArray().uint
    
    def __repr__(self):
        head = '<gbif.taxonomy.Presence instance %s >' %str(self)
        return head
    
    def __list__(self):
        return self.list
        

class Presences:
    """
    ..
    This class implements the features and operations needed to explore the integer representation
    of the assemblage of taxa.
    
    """
    def __init__(self,dictionary_of_presence_list):
        """
        ..
        """
        d = dictionary_of_presence_list
        self.species = Presence(d['sp'])
        self.genera = Presence(d['gns'])
        self.families = Presence(d['fam'])
        self.orders = Presence(d['ord'])
        self.classes = Presence(d['cls'])
        self.phyla = Presence(d['phy'])
        self.kingdoms = Presence(d['kng'])
        
        
    def toDict(self):
        """
        ..
        
        Convert Presences into a dictionary.
        
        Returns
        -------
            
            dic : A dictionary 
                that uses as key the settings.TAXONOMIC_TREE_KEYS and values the presence/absence list.
                

        """
        
        d = {}
        d['sp'] = self.species
        d['gns'] = self.genera
        d['fam'] = self.families
        d['ord'] = self.orders
        d['cls'] = self.classes
        d['phy'] = self.phyla
        d['kng'] = self.kingdoms
        
        return d
    

    def __repr__(self):
        """
        The representation in console
        
        """
        dic = self.toDict()
        body = '<gbif.taxonomy.Presences instance: \n'
        for key,value in dic.iteritems():
            c = 'key %s : %i  \n' %(key,int(value))
            body += c
        body += '\>'
        return body


class Taxonomy:
    """
    .. Taxonomy:
    
    Class Taxonomy
    ==============
    ..
    
    Summary
    -------
    Defines the taxonomic groups within one biome. 
    A biome is a Subset of GBIF data built as the interior of a simple closed curve contained in the surface of the Earth.
    
    Attributes
    ----------
    occurrences : Gbif.models.Occurence
        All the occurrences within the geometry of the biome
    species : Gbif.models.Occurence.aggregated(species)
        All the occurrences aggregated by the relationship of being a member of the species S. 
    genera  : Gbif.models.Occurence.aggregated(genera)
        All the species aggregated by the relationship of being a member of the genus G.
    families : Gbif.models.Occurence.aggregated(families)
        All the genera aggregated by the relationship of being a member of the family F.
    orders : Gbif.models.Occurence.aggregated(orders)
        All the families aggregated by the relationship of being a member of the order O. 
    classes  : Gbif.models.Occurence.aggregated(classes)
        All the orders aggregated by the relationship of being a member of the class C.
    phyla : Gbif.models.Occurence.aggregated(phyla)
        All the classes aggregated by the relationship of being a member of the phylum P. 
    kingdoms : Gbif.models.Occurence.aggregated(kingdoms)
        All the phyla aggregated by the relationship of being a member of the kingdom K. 
    
    richness : dictionary
        A dictionary containing the counts of all the aggregated objects at the different taxonomic scales.
        
        {'occurrences' : number of occurrences,
        'species' : number of species,
        'genera' : number of genera,
        'families': number of families,
        'classes' : number of classes,
        'orders' : number of orders,
        'phyla' : number of phyla,
        'kingdoms' : number of kingdoms
        }
    biomeGeometry : geometry
        The geometry inherited by the geometric attribute of the biome
    gid : int
        The identification value inherited by the cell in a mesh that defines the biome (if applicable)
    forest : dictionary of trees 
        A dictionary that has as keys:
        {'sp' : Local taxonomic tree at specie level,
        'gns' : Local taxonomic tree at genus level
        'fam' : Local taxonomic tree at family level
        'ord' : Local taxonomic tree at order level
        'cls' : Local taxonomic tree at class level
        'phy' : Local taxonomic tree at phylum level
        'kng' : Local taxonomic tree at kingdom level
        Each local taxonomic tree is an instance of the class ete2.TreeNode()
        This is the *morphism* that changes the objects from the SQL-Table structure to the graph (Tree) structure.
    JacobiM : numpy.Matrix
        The *extrinsic* matrix derived from the change from level to level (distance) from another external taxonomic structure.
        In most cases it could be the parent taxonomic tree at a bigger scale, i.e. The top grid in an NestedTaxonomyGrid instance.
    vectorJacobi : numpy.array / list
        An array derived from a projection into R of the JacobiM at different submatrices.
        The common projection is the determinant in which the first element will be the determinant of the submatrix of JacobiM given by
        i,j = {1,2} and the last one will be the complete submatrix = JacobiM
    intrinsicM : numpy.Matrix
        The *intrinsic* matrix is derived as the change in richness (or any other taxonomic measure) from one level to another givin a 7x7 matrix 
        in which each row (column) represent a toxonomic level. This matrix is calculated only with the information given by the taxonomy itself,
        therefore the name *intrinsic*
    vectorIntrinsic : numpy.array / list
        An array derived from a projection into R of the intrisicM at different submatrices.
        The common projection is the determinant in which the first element will be the determinant of the submatrix of intrisicM given by
        i,j = {1,2} and the last one will be the complete submatrix = intrisicM
    presences : A presence type
        An object that has attributes in the taxonomic level key word (as in forest)
        As values has lists that defines the presence or absences of species based on other taxonomy.
        
        .. note:: if the lists are full of 1's it means that this is the maximum level of representativeness, possible is a parent taxonomy.
  
    Parameters
    ----------
    biome : gbif.models.GeoQuerySet
        Biome is a query set of the gbif occurrence instance modulus a 2-d geometry in Earth.
    geometry : geometry WKB
        It is a geometric attribute that could be independent of biome.
    id : int 
        It is an attribute for indexing the object (generaly inherited by the gid of the grid cell).
    

    
    
    Notes
    -----
    The objective here is to make it elegant enough so everything are queries without execution (LazyQueries).
    
    The aggregations in occurrence, species, etc, has the form of a dictionary in which the following key:values are defined:
    
    Defined by
    ----------
    points : Collection of points
    ab : abundance / richness
    name : name of the aggregated class
    parent_id : id of the aggregated parent

  
    
    
    """
    def __init__(self,biome,geometry='',id=-999,build_tree_now=True):
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
        
        #self.Species = [ Specie(biome,aggregated_dictionary) for aggregated_dictionary in self.species ]
        #self.Genera = [ Genus(biome,aggregated_dictionary)for aggregated_dictionary in self.genera ]
        #self.Families = [ Family(biome,aggregated_dictionary) for aggregated_dictionary in self.families ]
        #self.Orders = [ Order(biome,aggregated_dictionary) for aggregated_dictionary in self.orders ]
        #self.Classes = [ Class(biome,aggregated_dictionary) for aggregated_dictionary in self.classes ]
        #self.Phyla = [ Phylum(biome,aggregated_dictionary) for aggregated_dictionary in self.phyla]

        
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
        self.JacobiM = [] #This is the attribute of the Jacobian matrix calculated with respect to the distance of another taxonomy.
        self.vectorJacobi = [] # This is the vector form of the determinants at each submatrix.
        self.intrinsicM = []
        self.vectorIntrinsic = []
        self.presences = {}
        self.shannon_entropy ={ 'occurrences' : 0,
            'species' : 0,
            'genera' : 0,
            'families': 0,
            'classes' : 0,
            'orders' : 0,
            'phyla' : 0,
            'kingdoms' : 0
            }        
        
        ## New attributes added for the new version
        self.TREE = None
        self.associated_data = {}
        
        if build_tree_now:
            self.generateTREE()
            


    def generateTREE(self):
        self.TREE = Root(self.occurrences,idnum=int(self.gid))
        return self.TREE

    def removeQuerySets(self):
        """
        This method removes the GeoQueryValueSet specified in the attributes:
        * occurrences,
        * species,
        * genera,
        * families,
        * classes,
        * orders,
        * phyla
        * kingdoms
        
        .. note:: Why ? Because it's necessary to pickle this and other derived 
        classes and the use of LazyQueries doesn't allow pickling.
        The pickling is used for creating the Cache via Redis.
        
        """
        self.occurrences = []
        self.species =  []
        self.genera  = []
        self.families = []
        self.orders = []
        self.classes  = []
        self.phyla = []
        self.kingdoms = [] 

    def restoreQuerySets(self,biome):
        """
        This method restores the GeoqueryValuesSet for the occurrences, species
        genera, families, classes, orders, phyla and kingdoms which are aggregates of 
        the Occurrence object.
        """
        self.occurrences = biome.all()
        self.species =  biome.values('species_id').annotate(points=Collect('geom'),ab=Count('species_id'),name=Min('scientific_name'),parent_id=Min('genus_id'))
        self.genera  = biome.values('genus_id').annotate(points=Collect('geom'),ab=Count('genus_id'),name=Min('genus'),parent_id=Min('family_id'))
        self.families = biome.values('family_id').annotate(points=Collect('geom'),ab=Count('family_id'),name=Min('family'),parent_id=Min('order_id'))
        self.orders = biome.values('order_id').annotate(points=Collect('geom'),ab=Count('order_id'),name=Min('_order'),parent_id=Min('class_id'))
        self.classes  = biome.values('class_id').annotate(points=Collect('geom'),ab=Count('class_id'),name=Min('_class'),parent_id=Min('phylum_id'))
        self.phyla = biome.values('phylum_id').annotate(points=Collect('geom'),ab=Count('phylum_id'),name=Min('phylum'),parent_id=Min('kingdom_id'))
        self.kingdoms = biome.values('kingdom_id').annotate(points=Collect('geom'),ab=Count('kingdom_id'),name=Min('kingdom'))
       
    def calculateRichness(self):
        """
        Calculates richness at all levels
        
        Returns
        -------
        richness : dictionary
            A dictionary containing the abundance or richness values at every taxonomic level.
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

    def calculateShannonEntropy(self):
      
        
        if not self.richness:
            richness = calculateRichness()
        
        
        entropies = {}
        # For species
        Noc =  len(self.occurrences)     
        probs = map(lambda species : species['ab'] / float(Noc), self.species)
        probs = filter(lambda s : s != 0,probs)
        ents = map(lambda px : px *((-1)* np.log(px)),probs)
        spent = sum(ents)
        entropies['species'] = spent
        # For genus
        Nsp = len(self.occurrences)
        probs = map(lambda gns : gns['ab'] / float(Nsp), self.genera)
        probs = filter(lambda s : s != 0,probs)
        ents = map(lambda px : px *((-1)* np.log(px)),probs)
        gnent = sum(ents)
        entropies['genera'] =  gnent
        
        
        # For families
        Ngn = len(self.occurrences)
        probs = map(lambda fm : fm['ab'] / float(Ngn), self.families)
        probs = filter(lambda s : s != 0,probs)
        ents = map(lambda px : px *((-1)* np.log(px)),probs)
        fment = sum(ents)
        entropies['families'] =  fment 
        # For order
        Nfm = len(self.occurrences)
        probs = map(lambda ords : ords['ab'] / float(Nfm), self.orders)
        probs = filter(lambda s : s != 0,probs)        
        ents = map(lambda px : px *((-1)* np.log(px)),probs)
        ordent = sum(ents)                        
        entropies['orders'] =  ordent
        
        # For class
        Nord = len(self.occurrences)
        probs = map(lambda cls : cls['ab'] / float(Nord), self.classes)
        probs = filter(lambda s : s != 0,probs)        
        ents = map(lambda px : px *((-1)* np.log(px)),probs)
        clsent = sum(ents)
        entropies['classes'] =  clsent


        # For phyla
        Ncls = len(self.occurrences)
        probs = map(lambda phy : phy['ab'] / float(Ncls), self.phyla)
        probs = filter(lambda s : s != 0,probs)        
        ents = map(lambda px : px *((-1)* np.log(px)),probs)
        phyent = sum(ents)
        entropies['phyla'] =  phyent

        
        # For kingdoms
        Nphys =len(self.occurrences)
        probs = map(lambda kng : kng['ab'] / float(Nphys), self.kingdoms)
        probs = filter(lambda s : s != 0,probs)        
        ents = map(lambda px : px *((-1)* np.log(px)),probs)
        kngment = sum(ents)
        entropies['kingdoms'] =  kngment
        
        self.shannon_entropy = entropies

        return entropies

    def calculateIntrinsicComplexity(self):
        """
        .. calculateIntrinsicComplexity:
        Intrinsic Complexity is a "measure (still need to proof is a measure)" of variabibility from one taxonomic level to another.
        It makes reference only to the current tree and not other external object (therefore intrinsic)
        Also it sets the intrinsicM attribute.
        
        Returns
        -------
        intrinsicM : numpy.Matrix
        
        """
        #dist = lambda i,j : (1 - (float(j - i) / (j + i)))
        dist = lambda i,j : (float(i) / j)
        dic = self.calculateRichness()
        # Needed for order the stupid unordered by default dictonary type :P
        ordered_keys = settings.TAXONOMIC_TREE_KEYS
        map_keys = settings.TAXONOMIC_MAPPER_KEYS
        # NOTE there are not occurrences right now!!
        keys = dic.keys()
        mat = []
        for keyi in ordered_keys:
            rows = []
            for keyj in ordered_keys:
                i = self.richness[map_keys[keyi]]
                j = self.richness[map_keys[keyj]]
                try:
                    d = dist(i,j)
                except:
                    d = float('nan')
                rows.append(d)
            mat.append(rows)
        mat = np.matrix(mat)
        self.intrinsicM = mat
        submatrices = map(lambda i : self.intrinsicM[0:i,0:i],range(1,len(self.intrinsicM) + 1))
        self.vectorIntrinsic = np.array(map(lambda M :np.linalg.det(M),submatrices))
        return mat

    def distanceToTree_deprec(self,taxonomic_forest,update_inner_attributes=True):
        """
        This function calculates the distance from this object to the taxonomic_forest given as input.
        The distance is based on an a given metric between all the partial trees.
        
        .. note:: Deprecated because it uses Robinson-Foulds distance.
        This method does the Robinson_foulds metric. It has been found to be not a good metric for the purposes of measuring diffrence accros scales.
        Not working for comparing between scales.

        Parameters
        ----------
        taxonomic_forest : dictionary of trees
            The dictionary obtained by the pruning of the taxonomic tree at species level to obtain the other levels.
        update_inner_attributes : Boolean
            When true it will set the attributes (like forest) to be this value.
            
        Returns
        -------
        Jacobian : numpy.matrix
            The matrix obtained from the comparison (distance) between the two taxonomies
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
        This method calculated the taxonomic distance between the current taxonomy and qn external taxonomy.
        
        .. note:: This method implements the metric scale tree distance proposed by Escamilla-Mólgora (2015)
        This method does the Robinson_foulds metric. It has been found to be not a good metric for the purposes of measuring diffrence accros scales.
        Not working for comparing between scales.

        Parameters
        ----------
        parent_taxonomic_forest : It's the forest (in dictionary type) that is going to be compared with.
            The dictionary obtained by the pruning of the taxonomic tree at species level to obtain the other levels.
        update_inner_attributes : Boolean
            When true it will set the attributes (like forest) to be this value.
            
        Returns
        -------
        Jacobian : numpy.matrix
            The matrix obtained from the comparison (distance) between the two taxonomies
         
        """ 
        Jacobian =[]
        for level_i in settings.TAXONOMIC_TREE_KEYS :
            # gradient at level level
            gradLevel = []
            for level_j in settings.TAXONOMIC_TREE_KEYS:
                # nj is the number of elements in the big scale J
                nj = float(len(parent_taxonomic_forest[level_j].get_leaves()))                
                # ni is the number of elements in the current tree (forest)
                ni = float(len(self.forest[level_i].get_leaves()))
                d_ij = 1 - ((nj - ni)/(nj + ni))
                if d_ij < 0:
                    logger.info("[biospatial.gbif.taxonomy.distanceToTree] The parent tree has less nodes than the current one.\n Perhaps the analysis is not spatially nested.")
                gradLevel.append(d_ij)
            Jacobian.append(gradLevel)
        if update_inner_attributes:
            self.JacobiM = np.matrix(Jacobian)
            submatrices_of_jacobian = map(lambda i : self.JacobiM[0:i,0:i],range(1,len(settings.TAXONOMIC_LEVELS) - 1))
            self.vectorJacobi = map(lambda M :np.linalg.det(M),submatrices_of_jacobian) 
            
        return np.matrix(Jacobian) 
        
    #def distanceToTree
   
    def generatePDI(self,level='species',type='richness'):
        """
        This method calculates partial diversity index (PDI) based on the taxonomic level and the diversity measure.
        
        .. note:: Not complete, need to refactor, if needed.
        
        Parameters
        ----------
        level : string
            The taxonomic level
        
        type \in ['richness', 'abundance', 'relative_abundance']
        
        Returns
        -------
        PDI : float
            The Partial diversity index
        
        
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
        .. getFreqs:
        This function returns a graph of richness, abundance or relative abundance.
        
        .. note:: This method only works in interactive environments because makes use of the matplotlib.plot.show() function.
        

        * Example of usage 
        .. sourcecode:: ipython
        
            In[69]: tx = Taxonomy(biome,cell.geom,cell.id)
            In[70]: tx.getFreqs() #Default value sel = richness
            
        .. image:: ../../../../modules/_static/rel_freq.png  
        
        Parameters
        ----------
        Could be one of the following:
        sel : 'richness'
            The count data obtained from the richness attribute.
        sel : 'abundance'
            The abundance function depends on the total number of occurrences within that polygon.
        sel : 'rel_abundance'
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
            else:
                logger.error("[biospatial.gbif.taxonomy.getFreq] Selection not valid")
                return False
        except:
            logger.error("[biospatial.gbif.taxonomy.getFreq] No data values for richness. \n Hint: Run Summary()")
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
        
    def buildInnerTree(self,deep=False,only_id=True):
        """
        .. buildInnerTree:
        Calculates the tree generating a ETE2 data type.
        
        note:
            Deprecated in new version. Changed method to own class type, for avoiding problematic ETE2.
            Check generateTREE()
        
        .. seealso:: 
            
            gbif.taxonomy.Taxonomy 
        
        Parameters
        ----------
            
            deep : Boolean (flag) 
                True means that is going to build all the partial trees as well.
                Partial tree is the pruned version at phylum, class, order,...,or, species
                
            only_id : Boolean (flag)
                True (default) means that is going to append the full name of the taxons.
                This is a string and can be vary in length. If it is used in big data sets it will 
                impact the amount of memory used because of the heavy load of information.
        
        Returns
        -------
            Void

        
        """
        if deep:
            self.obtainPartialTrees(only_id=only_id)
        else:
            self.forest['sp'] = getTOL(self,only_id=only_id)

    def obtainPartialTrees(self,only_id=True):
        """
        .. obtainPartialTrees:
    
        This method defines the partial trees for the selected taxonomic level.
        It prunes the species tree to generate seven distinct trees at each taxonomic level.
        
        Parameters
        ----------
        
            only_id : Boolean (flag)
                True (default) means that is going to append the full name of the taxons.
                This is a string and can be vary in length. If it is used in big data sets it will 
                impact the amount of memory used because of the heavy load of information.

        
        
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
            self.forest['sp'] = getTOL(self,only_id=only_id)
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
        This method calculates the maximum possible distance considering an empty tree as a reference.
        
        Returns
        -------
        Jacobian Matrix : numpy.Matrix
        
        
        """
        from ete2 import Tree
        t = Tree(name='LUCA_root')
        empty_forest = {'sp':t,'gns':t,'fam':t,'ord':t,'cls':t,'phy':t,'kng':t}
        return self.distanceToTree(empty_forest,update_inner_attributes=False)

    def singlePresenceAbsenceRepr(self,reference='parent',taxonkey='sp'):
        """
        .. presenceAbsenceRepr
        
        This method gives a (binary) lazylist (generator) of presence/absence of taxons based on a referenced list passed
        as the parameter 'reference_list'.

        This parameter should be an 'ordered' integer list of present taxons.
        
        Parameters
        ----------
            
                reference : list of integers
                    The list of taxon ids to compare.
                    If refererence list is the default ('parent')
                    this means that the reference_list is  itself. 
                    Useful in a nested taxonomy when refered to a parent level.
                    
                    All the values in the list should be 1.
                    
                taxonkey : string
                    The value used to specify which taxonomic level is refering to.
                    Options are (sp,gns,fam,ord,cls,phy,kng). 
                    The same as the attribute forest.

                    
        Returns
        -------
        
            list generator : binary 
                This object is a generator but can easily be traslated to list via a cast.
                This is to avoid intensive load of data, if there is the case.
        
        .. note:: 
            
            In order for this method to work properly, it is important that the reference_list is in the same
            referencing system as the target taxonomy. By this I mean that if the taxonkey is 'sp' (for instance) the reference_list 
            should be composed of ids retrieved from the species_id feature.
             
        """
        try:
            leaf_ids = self.forest[taxonkey].get_leaf_names()
        except:
            logger.error('Requested taxonkey value %s doesn\'t exist. Hint: load from cache or check the taxonkey value')
            raise Exception('Requested taxonkey value %s doesn\'t exist. Hint: load from cache or check the taxonkey value')

        #Sort the values
        leaf_ids.sort()
        # Use list comprehension to generate the presence/absence list.
        if reference == 'parent':
            l = (1 for x in leaf_ids if x > 0)
            l2 = zip(leaf_ids,l)
        else:
            l1 = (x if x in leaf_ids else 'x' for x in reference.keys)
            l2 = (1 if x in leaf_ids else 0 for x in reference.keys)
            #but this zip ruins the generator
            l2 = zip(l1,l2)
        return l2

    def setPresenceAbsenceFeature(self,reference_dict='parent'):
        """
        .. setPresenceAbsenceFeature

        This method sets the presences attribute. A dictionary of presence/absence taxons based on a referenced list passed
        as the parameter 'reference_list'.

        This parameter should be an 'ordered' integer list of present taxons.
        
        Parameters
        ----------
            
                reference_dict : dictionary of presences
                    Each value in the dictionary is a list of taxa ids to compare.
                    If the refererence dict is the default value ('parent')
                    this means that the reference_dict is itself. 
                    Useful in a nested taxonomy when refered to a parent level.
                    
                    All the values in the list will be 1.
                

                    
        Returns
        -------
        
            Null : nothing 
                This method sets the presences attribute.
        
        .. note:: 
            
            In order for this method to work properly, it is important that the reference_list is in the same
            referencing system as the target taxonomy. This means that the reference_list 
            should be composed of ids retrieved from the same taxonomic_id level feature.        
        
        """
        
        

        presences_dic = {}
        if isinstance(reference_dict,dict): 
            for key,reference_list in reference_dict.iteritems():
                presences_dic[key] = self.singlePresenceAbsenceRepr(reference=reference_list,taxonkey=key)            
            self.presences = Presences(presences_dic)
        else:
            if reference_dict == 'parent':
                keys = settings.TAXONOMIC_TREE_KEYS
                for key in keys:

                    presences_dic[key] = self.singlePresenceAbsenceRepr(taxonkey=key)            
                self.presences = Presences(presences_dic)
            else:
                logger.error("reference_dict is invalid, check syntax and documentation")
                raise Exception("reference_dict is invalid, check syntax and documentation")
                
    def loadFromCache(self,cached_taxonomy):
        """
        
        This method restores the cached values stored in the Redis backend.
        
        Parameters
        ----------
            
            cached_taxonomy : Taxonomy
                The taxonomy obtained from the cache backend.
                
        .. note:: The cached object can be created using the create_tree_now set to False
        Which is going to create the taxonomy with out making the calculations for obtaining the tree
        giving an empty object with defined GeoQueryValuesSets.
        
        """
        #First check if the geometry is the same:
        cache = cached_taxonomy
        try:
            self.rich_occurrences =  cache.richness['occurrences']
            self.rich_species = cache.richness['species']
            self.rich_genera = cache.richness['genera']
            self.rich_families = cache.richness['families']
            self.rich_classes = cache.richness['classes']
            self.rich_orders = cache.richness['orders'] 
            self.rich_phyla = cache.richness['phyla']
            self.rich_kingdoms = cache.richness['kingdoms']
            self.richness ={ 'occurrences' : self.rich_occurrences,
            'species' : self.rich_species,
            'genera' : self.rich_genera,
            'families': self.rich_families,
            'classes' : self.rich_classes,
            'orders' : self.rich_orders,
            'phyla' : self.rich_phyla,
            'kingdoms' : self.rich_kingdoms
            }
            self.biomeGeometry = cache.biomeGeometry
            self.gid = cache.gid
            self.forest = cache.forest
            self.JacobiM = cache.JacobiM #This is the attribute of the Jacobian matrix calculated with respect to the distance of another taxonomy.
            self.vectorJacobi = cache.vectorJacobi # This is the vector form of the determinants at each submatrix.
            self.intrinsicM = cache.intrinsicM
            self.vectorIntrinsic = cache.vectorIntrinsic
            return True
        except:
            logger.error("cache_taxonomy is not a Taxonomy object")
            return None

    def __repr__(self):
        geom = self.biomeGeometry.wkt
        cad = "< Taxonomy in %s > %geom"
        return cad
       
    def showId(self):
        """
        This method returns a unique Id string that is going to be used as unique identifier
        use as a key in the implementation of a cache service.
        
        .. note:: Check this when global analyses are defined
        
        """
        #Here I'm supposing that the name of the table, and the extent polygon gives a unique mapping.
        try:
            extent = self.biomeGeometry.extent
            name = "tax"
            res = self.biomeGeometry.area
            string = "%s-%s:%s:%s" %(name,self.gid,extent,res)
            return string
        except:
            logger.error("[biospatial.gbif.taxonomy.GriddedTaxonomy] \n The total geometry area has not been defined. Try running mergeGeometries first")
            raise Exception("Geometry Extent has not been instantiated")
            return None 
        
    def cache(self,redis_wrapper,key='default',refresh=False):
        """
        .. cache
        
        This method stores in cache the Taxonomy
        using the key parameter as Key.
        
        Parameters
        ==========
            redis_wrapper : StrictRedis object
                This is the redis connection to be used.
                Needs to have specified host, database and port
            key : string
                The key used for storing in the Redis backend.
                If none then it will use the output of the ShowId method.
            refresh : Boolean
                If true it will update the value.
                If false and if the key / object exists then it will not store in cache.
                
        
        """
        
        
        if key == 'default':
            key = self.showId()
        
        if not redis_wrapper.exists(key) or refresh:             
            logger.info('Serializing Object. \n Depending on the amount of data it can take some time')
        
            #Cleaning GeoQueryValuesSets fields
            #map(lambda grid : grid.removeQuerySets(),self)
            logger.info('Removing GeoQueryValuesSets')
            self.removeQuerySets()
            import pickle
            logger.info('Serializing with pickle')    
            self_pickle = pickle.dumps(self)
            logger.info("Storing in Taxonomy in Cache")
            try:
            
                redis_wrapper.set(key,self_pickle)
                return True
            except:
                logger.error("Problem in serializing. The intented caching object could be very big!")
                return self_pickle    
        else:
            logger.info('Object exists on Cache System. For update activate flag: refresh to True')
            return True

    def mergeWithThisRasterData(self,raster_api_model,option=1,lazy_eval=True):
        """
        This method associate a new data to the current taxonomy. 
        It is intented to be used for fussing information from other source, specifically a raster stored
        in postgis as a raster table. 
        See: raster_api module for more information.
        
        Parameters : 
            raster_api_model : A raster_api class. (the abstract model).
            option : The aggregation method to be used. That is, how information is going to be taken from the raw raster.
                more information see: raster_api.tools.aggregates_dict
                option : integer
                    1 : Raw DEM (Elevation)
                    2 : Slope (angle 0 - 90) 
                    3 : Aspect Orientation of facet (0, 360) 
                    4 : Hillshade (for visualising)
                
            lazy_eval : if false it will retrieve the data when called.
        """
        
        raster_data = RasterData(raster_api_model,self.biomeGeometry)
        self.associated_data[raster_data.neo_label_name] = raster_data
        
        if lazy_eval:
            rasterfield = raster_data.processDEM(option=option)
            return raster_data
        else: 
            return raster_data 

    def bindRasterNodeOccurrence(self,RasterData,writeDB=False):
        """
        Binds the Occurrence (leaves in the tree) with a geospatial match of a RasterData model.
        
        Parameters :
            RasterData : The Raster_api model
        """
        for o in self.occurrences:
            o.bind_withNodeDEM(RasterData,writeDB=writeDB)
        return None
    

    def bootstrapTreeToLeaves(self,graph_driver):
        """
        Binds every internode to each Occurrences.
        This is done to make a direct connection to the matching data based on the occurrence (point/time).
        Rememmber this is done in each single tree bounded by a cell or polygon.
        """
        for occurrence in self.occurrences:
            node = occurrence.getNode()
            if self.TREE :
                self.TREE.bindExternalNode(node, relationship_type="HAS_OCURRENCE")
            

class GriddedTaxonomy:
    """
    ..
    GriddedTaxonomy
    ===============
    
        This class instantiates a model based on a given grid and defines in each cell a Taxonomy object.
        There are certain attributes that gives spatial information.

    
    Attributes
    ==========
    taxonomies : list Taxonomies
        A list of taxonomies in defined under the action of the geometric constraints of each cell in the grid.
    extent : numpy.array
        The geographical extention of the Grid
    area : Float
        The geographical (degrees) area covered by the grid
    geometry : geometry
        The geometry of the grid
    grid_name : string
        The name of the corresponding table of this grid in the database
    parent_id : int
        An id value to define the Grid   
    dArea : float
        The unit area represented by a single cell
    biosphere: GeoqueryValuesSet
        The subset of the GBIF Occurrences that is defined globally in the entire grid.

  
    Parameters
    ==========    
    biosphere : Geoqueryset (GBIF)
        The GBIF Geoqueryset attribute from gbif.models.Occurrence
    mesh : mesh.mesh
        A mesh instance (grid layer). Alternatively called grid
    upper_level_grid_id : int (default 0)
        An id value to define the Grid
    generate_tree_now : Boolean (default False)
        Flag that when True calculates the taxonomy.forest attribute.
        i.e. The taxonomic tree.
    grid_name : string
        The grid_name defined in the spatially enabled database.

    use_id_as_name: boolean (default True)
        This is a flag and when True means that the nodes in the trees are going to be named
        according to the identifier (Integer) instead of the full string name.
        Saves memory.        
    
    """
    def __init__(self,biosphere,mesh,upper_level_grid_id=0,generate_tree_now=False,grid_name='N.A.',use_id_as_name=True):
        """
        Constructor.
        This function performs a spatial intersection and initialize Taxonomy objects with the geometry given by [mesh].
        [biosphere] is a Geoqueryset of gbif occurrences. [mesh] is a mesh type.
        Upper_level_grid is a parameter reserved for the id of the parent mesh cell.
        """
        self.taxonomies = embedTaxonomyInGrid(biosphere,mesh,upper_level_grid_id=upper_level_grid_id,generate_tree_now=generate_tree_now,use_id_as_name=use_id_as_name)
        self.extent = 'N.A.'
        self.area = 'N.A'
        self.biomeGeometry = 'N.A'
        self.grid_name = grid_name
        self.parent_id = upper_level_grid_id
        self.dArea = self.taxonomies[0].biomeGeometry.area
        self.biosphere = biosphere


    def __str__(self):
        return u"GriddedTaxonomy layer: \n Extent: %s" %str(self.biomeGeometry.extent)     
        
    def __repr__(self):
        cad = "<GriddedTaxonomy instance: %s@%s >" %(self.parent_id,self.grid_name)
        return cad

            
    def __iter__(self):
        """
        .. iterator
        
        This method defines the iterator for the GriddedTaxonomy.
        It is a shortcut for using taxonomies.  
        The items are the taxonomy objects in the taxonomies list.
        
        .. note:: My second iterator :')
        """
        return iter(self.taxonomies)




    
    def showId(self):
        """
        This method returns a unique Id string that is going to be used as unique identifier
        use as a key in the implementation of a cache service.
        
        .. note:: Check this when global analyses are defined
        
        """
        #Here I'm supposing that the name of the table, and the extent polygon gives a unique mapping.
        try:
            extent = self.biomeGeometry.extent
            name = self.grid_name
            res = self.dArea
            string = "%s:%s:%s:%s" %(self.parent_id,name,extent,res)
            return string
        except:
            logger.error("[biospatial.gbif.taxonomy.GriddedTaxonomy] \n The total geometry area has not been defined. Try running mergeGeometries first")
            raise Exception("Geometry Extent has not been instantiated")
            return None   

    def restoreQuerySets(self,biosphere):
        """
        This method restores the GeoqueryValuesSet for each taxonomy in the grid: occurrences, species
        genera, families, classes, orders, phyla and kingdoms which are aggregates of 
        the Occurrence object.
        
        .. note:: This method is usefull when the Gridded Taxonomy comes from a Cache Backend
        """
        # Redefine the biosphere
        self.biosphere = biosphere
        # Extract geometries from taxonomies
        geometries = map(lambda t : t.biomeGeometry, self.taxonomies)
        # Build biomes based on the intersections between each geometry and the global biosphere
        biomes = map(lambda polygon : self.biosphere.filter(geom__intersects=polygon),geometries)
        # Now restore older querysets. Usefull if the Gridded Taxonomy comes from a Cache Backend
        biom_tax = zip(biomes,self.taxonomies)
        logger.info("Restoring the Queryset lost in the Caching process")
        map(lambda duple : duple[1].restoreQuerySets(duple[0]), biom_tax )
               
    def removeQuerySets(self):        
        """
        
        This method removes the GeoQueryValueSet specified in the attributes:
        
        * occurrences,
        * species,
        * genera,
        * families,
        * classes,
        * orders,
        * phyla
        * kingdoms
        
        Inside each element (cell) of the Gridded Taxonomy
        
        .. note:: Why ? Because it's necessary to pickle this and other derived 
        classes and the use of LazyQueries doesn't allow pickling.
        The pickling is used for creating the Cache via Redis.
        
        """
        logger.info("Disabling GeoQueryValuesSets for the taxonomic attributes")
        self.biosphere = []
        map(lambda tax : tax.removeQuerySets(), self.taxonomies)
        
    def refreshTaxonomiesGeoQuerySets(self,cached_gridded_taxonomy):
        """
        ..
        This method refresh the GeoQuerySets in the taxonomy list that
        cannot be cached because of the Lazy Queries implementation.
        
        Parameters
        ----------
            
            new_gridded_taxonomy : GriddedTaxonomy
                The grid obtained from a newly created Taxonomy object.
                
        .. note:: The new object can be created using the create_tree_now set to False
        Which is going to create the taxonomy with out making the calculations for obtaining the tree
        giving an empty object with defined GeoQueryValuesSets.
        
        """
        cache = cached_gridded_taxonomy
        self.mergeGeometries()
        cache.mergeGeometries()
        if (self.showId() == cache.showId()) and (len(self.taxonomies) == len(cache.taxonomies)):
            # Group taxonomies from itself to cached
            self_cache = zip(self.taxonomies,cache.taxonomies)
            # Load the features from cache
            map(lambda s_c: s_c[0].loadFromCache(s_c[1]),self_cache)
            return True
            
            
        else:
            raise Exception("Error the cached_griddedTaxonomy is not the same")
            return None

    def restoreTaxonomiesFromCache(self,redis_wrapper):
        """
        ..
        This method restores the taxonomies from cache.
        
        """
        #=======================================================================
        # if path_to_file:
        #     f = open(path_to_file)
        #     tax = pickle.load(f)
        #     #hacer para cuando hay file
        #=======================================================================
            
        keys = map(lambda t : t.showId(), self.taxonomies)
        
        if len(keys) == len(self.taxonomies):
            for i,key in enumerate(keys):
                logger.info('Restored Taxonomy: %i/%i '%(i+1,len(keys)))
                taxo_raw = redis_wrapper.get(key)
                tax = pickle.loads(taxo_raw)
                
                self.taxonomies[i].loadFromCache(tax)
                #logger.info('Restored Taxonomy: %i/%i '%(i+1,len(keys)))
            logger.info('All taxonomies restored')
        return None
            
    def createShapefile(self,option='richness',store='out_maps'):
        """
        .. createShapefile:
        
        This function creates a shapefile using a selected attribute from the GriddedTaxonomy class.
        
        .. note::
    
            Currently implemented:
        
            * richness (default) : 
            gives the counts of occurrences at each taxonomic level.
            
            * jacobi :
            gives the determinant of the distance (Escamilla) matrix 
            and sub-matrices from the 7x7 size to the 2x2.
            A layer for each determinant of each submatrix.
            
            * shannon :
                gives the shanon diversity index (entropy with natural logarithm)
                returns a dictionary with the values for each taxonomic level.
        
        Parameters
        ==========
        option : string
            'richness' (default), 'jacobi'
        store : string
            The path in which the shapefiles are going to be stored
                    
        """
        
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
                    #import ipdb;ipdb.set_trace()
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
        
        def selectShannon(layer):
            # This is for option richness
            for key in settings.TAXONOMIC_LEVELS:
                layer.CreateField(ogr.FieldDefn(key,ogr.OFTInteger))        
            defn = layer.GetLayerDefn()
                   
            ## If there are multiple geometries, put the "for" loop here
            for tax in self.taxonomies:
                #logger.debug("there are %s taxonomies" %(len(self.taxonomies)))
                tax.calculateShannonEntropy()
                try:
                    #import ipdb;ipdb.set_trace()
                    d = tax.shannon_entropy
                    feat = ogr.Feature(defn)
                    feat.SetField('gid', tax.gid)
                    
                    #logger.debug('gid')
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
            
        elif option == 'shannon':
            selectShannon(layer)
        # Save and close everything
        ds = layer = feat = geom = None
        logger.info('[biospatial.gbif.taxonomy.GriddedTaxonomy]\n Shapefile Created in %s/%s' %(store,option))
        return True
    
    def mergeGeometries(self):
        """
        .. mergeGeometries
        Creates a polygon made by the union of all the cells in the gridded taxonomy.
        
        Returns
        =======
        Boundary : polygon
            The polygon derived from the merging of all cells.
        """
        self.biomeGeometry = reduce(lambda p1,p2 : p1.union(p2) ,map(lambda tax : tax.biomeGeometry,self.taxonomies))
        return self.biomeGeometry
        
    def getArea(self):
        try:
            self.area = self.biomeGeometry.area
            return self.area
        except:
            logger.error('Geometry hasn\'t been defined (instantiate mergeGeometries first!)')
            return None
        
    def distanceToTree(self,taxonomic_forest):
        """
        .. distanceToTree:
        
        Calculates the distance from each taxonomy in the grid compared with an arbitrary taxonomic tree.
        
        .. seealso::
            gbif.taxonomy.distanceToTree()
        
        .. note:: 
            taxonomic_forest is a dictionary which uses keys: ['sp','gns','fam','ord','cls','phy','kng'] 
            This can be seen in the biospatial.settings file.
         
        Parameters
        ==========
        taxonomic_forest : dictionary of taxonomic trees
            With the same key value pairs as in :class: Taxonomy
        """
        
        matrices = map(lambda tax : tax.distanceToTree(taxonomic_forest),self.taxonomies)
        return matrices

    def setPresenceAbundanceData(self,reference_dict):
        """
        ..
        This method sets the presence attributes in every taxonomy in the Grid.
        It uses a dictionary passed as a parameter which has the reference presence/absence data.
        
        Parameters
        ----------
            
            reference_dict :  dictionary of Presences 
                The dictionary that has keys in {'sp','gns','fam','ord','cls','phy',kng'}
                and the associated values are the Presence data type that has all the taxonomic levels and has extends attributes in BitArray.
         
        Returns
        -------
            None : Null
                But set the attribute presences in each taxonomy.
        """
        
        ref  = reference_dict
        
        for taxonomy in self.taxonomies:
            taxonomy.setPresenceAbsenceFeature(reference_dict=ref)

        return None
            
    def summary(self,attr='raw'):
        """
        ..
        This method gives a dictionary of all the presence representation of each taxonomy in the grid.
        Depending on th parameter attr. 
        
        Parameters
        ----------
            
            attr : string
                
                The feature to extract. Options are:
                    
                    * int : the integer representation
                    * str : the Bitstring (String)
                    * list : The list of bits
                    * mapping : the mappping that relates Id with presence or absence
                
        Returns
        -------
        
            Depending on the selected paramter
        
        """
        g = {}
        g['gid'] = map(lambda x : x.gid, self.taxonomies)
        g['sp'] = map(lambda x : x.presences.species , self.taxonomies)
        
        g['gns'] = map(lambda x : x.presences.genera , self.taxonomies)   
        g['fam'] = map(lambda x : x.presences.families , self.taxonomies)
        g['ord'] = map(lambda x : x.presences.orders , self.taxonomies)
        g['cls'] = map(lambda x : x.presences.classes , self.taxonomies)
        g['phy'] = map(lambda x : x.presences.phyla , self.taxonomies)
        g['kng'] = map(lambda x : x.presences.kingdoms , self.taxonomies)
        #g['all'] = map(lambda x : (x.gid,int(x.presences.species),int(x.genera),int(x.families),int(x.orders),int(x.classes),int(x.phyla),int(x.kingdoms)),self.taxonomies)
        keys = settings.TAXONOMIC_TREE_KEYS
        if attr == 'int':
            for key in keys:
                g[key] = map(lambda p : int(p) ,g[key])
        elif attr == 'str':
            for key in keys:
                g[key] = map(lambda p : str(p) ,g[key]) 
        elif attr == 'list':
            for key in keys:
                g[key] = map(lambda p : p.list ,g[key])  
        elif attr == 'mapping':
            for key in keys:
                g[key] = map(lambda p : p.map ,g[key])       
        elif attr == 'raw':
            return g
        else:
            logger.error("Wrong attribute selection")
            return None
                              
        return g

    def cache(self,redis_wrapper,key='default'):
        """
        .. cache
        
        This method stores in cache the NestedGriddedTaxonomy
        using the key parameter as Key.
        
        Parameters
        ==========
            redis_wrapper : StrictRedis object
                This is the redis connection to be used.
                Needs to have specified host, database and port
            key : string
                The key used for storing in the Redis backend.
                If none then it will use the output of the ShowId method.
        
        """
        
        
        if key == 'default':
            key = self.showId()
        
        logger.info('Serializing GriddedTaxonomy. \n Depending on the amount of data it can take some time')
        
        #Cleaning GeoQueryValuesSets fields
        map(lambda grid : grid.removeQuerySets(),self)
        
        import pickle
        logger.info('Serializing with pickle')    
        self_pickle = pickle.dumps(self)
        logger.info("Storing in Cache")
        try:
            
            redis_wrapper.set(key,self_pickle)
            return True
        except:
            logger.error("Problem in serializing. The intented caching object could be very big!")
            return self_pickle    

    def intrinsicPanel(self,with_this_list=''):
        """
        .. intrinsicPanel
        This method extracts the intrinsicM attribute of all taxonomies with the Grid
        and returns a pandas Panel in which each entry in the matrix is a Serie composed all
        the values for a (taxonomic_level,taxonomic_level) duple.
        
        Parameters
        ==========
            
            with_this_list : list of taxonomies
                The taxonomies list from which the Panel is going to be build.
                For doing with all the taxonomies in the grid use: '' (default)
                
        
        
        Returns
        =======
            a Panel
                Similar to a matrix with the difference that each entry is a list Serie.
                Each element of this list correspond to the entry of the intrinsic matrix 
            
        """
        if with_this_list == '':
            taxonomic_list = self.taxonomies
        else:
            taxonomic_list = with_this_list
        import pandas as pn
        all_entries = {}
        for i,tax_name_i in enumerate(settings.TAXONOMIC_TREE_KEYS):
            li = {}
            for j,tax_name_j in enumerate(settings.TAXONOMIC_TREE_KEYS):   
                i_j = map(lambda t : t.intrinsicM[i,j],taxonomic_list)
                li[tax_name_j] = pn.Series(i_j)
            all_entries[tax_name_i] = li
        return pn.Panel(all_entries)          


    def bindTaxonomyToMesh(self,graph_driver):
        """
        First the mesh needs to be loaded in the GraphDB
        """
        l = []
        for t in self.taxonomies:
            nodecell = graph_driver.find_one("Cell","id",t.gid)
            coto = t.TREE.bindExternalNode(nodecell)
            l.append(coto)
        return l



        


    
class NestedTaxonomy:
    """
    .. NestedTaxomy
    
    NestedTaxonomy
    ==============
    
        This class instantiates nested taxonomies.
    
    Parameters
    ==========
    id : int
        Cell's id of the parent level (start_level)
    gbif_queryset : GeoquerySet
        An instance of the gbif database, could be a prefiltered one (e.g. a biome )
    start_level : int
        Id of the parent mesh level.
        See: gbif.mesh.NestedMesh and biospatial.settings
    end_level : int
        Id for the bottom of the stack
    generate_tree_now : Boolean (flag default: True)
        Generate the trees and subtrees of each taxonomic level in each cell.
    
    Attributes
    ==========
        levels : list of GriddedTaxonomy
        parent : The GriddedTaxonomy with the highest scale 
        parent_id : int
            Integer (gid) of the parent cell id.
        toplevel : Int
            The id level of the toppest grid.
        bottomlevel : Int
            The id level of the grid with higher resolution (bottom).
    
    
    """  
    def __init__(self,id,gbif_geoqueryset,start_level=12,end_level=14,generate_tree_now=True,use_id_as_name=True):

        self.levels = embedTaxonomyInNestedGrid(id,gbif_geoqueryset,start_level=start_level,end_level=end_level,generate_tree_now=generate_tree_now,use_id_as_name=use_id_as_name) 
        self.parent = self.levels[start_level].taxonomies[0]
        self.maxdistances = self.getMaximumDistances()
        self.parent_id = id
        self.toplevel = start_level
        self.current_level = start_level
        self.bottomlevel = end_level
               
    def __repr__(self):
        cad = '<gbif.taxonomy.NestedTaxonomy instance with levels: %s>' %str(self.levels)    
        return cad

    def next(self):
        """
        Next function for iterator
        If changed to Python 3.x the name should change to __next__
        """
        if self.current_level > self.bottomlevel:
            self.current_level = self.toplevel
            raise StopIteration

        else:
            self.current_level += 1
            return self.levels[self.current_level - 1]
            
    def __iter__(self):
        """
        .. iterator
        
        This method defines the iterator for the NestedTaxonomy. 
        The items are the ordered (from top to bottom) levels.
        Remmember that a level is a GriddedTaxonomy in the Stack.
        
        .. note:: My first iterator :')
        """
        return self
    
    def setPresenceInLevels(self,external_reference_dic='No'):
        """
        ..
        This method sets the presence/absence lists on all the taxonomies on all the 
        levels defined in the NestedTaxonomy.

           
        Parameters
        ----------
            
                external_reference_dic :  dictionary of Presences 
                The dictionary that has keys in {'sp','gns','fam','ord','cls','phy',kng'}
                and the associated values are the Presence data type that has all the taxonomic levels and has extends attributes in BitArray.
         
        Returns
        -------
            None : Null
                But set the attribute presences in each taxonomy.
        """           
           
        
        if external_reference_dic == 'No':
            # this will initialize the directory using the parent as level as reference
            logger.info('Using parent taxonomy as reference source for representing presences and absences in subsequent levels.')
            self.parent.setPresenceAbsenceFeature()
            dic = self.parent.presences.toDict()
        else:
            dic = external_reference_dic
        try:    
            for level in self:
                level.setPresenceAbundanceData(dic)
        except:
            logger.error("The reference dictionary is not compatible.")
            raise Exception("The reference dictionary is not compatible.")
    
    def getLevels(self):
        """
        Gives the available zooming levels in the current Nested Taxonomy.
        
        Returns
        =======
        levels : list
            The list of all levels
            
        """
        levels = self.levels.keys()
        levels.sort()
        a = str(levels)
        
        logger.info('[biospatial.gbif.taxonomy.NestedTaxonomy]\n Available Levels %s' %a)
        return a
        
    def getDistancesAtLevel(self,level,foreign_forest='Top'):
        """
        This method calculates all the Jacobian matrices comparing the parent tree with the specified level.
        
        .. note::
            Used extensively for first order analysis and in the QGIS implementation
        
        Parameters
        ==========
        level : int
            The key value (int) of some Gridd level nested in this object.
        foreign_forest : dictionary taxonomies
            The usual taxonomic forest
            
        Returns
        =======
        Jacobian (Distance) matrix : numpy.matrix
            The 7x7 matrix obtain by comparing all taxonomic levels with themselves.
            
        """
        if foreign_forest == 'Top':
            parent_forest = self.parent.forest
        else:
            parent_forest = foreign_forest
        try:
            mats = self.levels[level].distanceToTree(parent_forest)
            return mats
        except:
            logger.error('[biospatial.gbif.taxonomy.NestedTaxonomy] \nSomethng went wrong. Perhaps the selected level doesn\'t exist for this NestedTaxonomy')
            return None
        
    def getMaximumDistances(self):
        """
        .. GetMaximumDistances
        This method calculates the maximum distance that a tree has 
        """
        pass
       
    def getExtent(self):
        """
        .. getExtent
        
        This methods gives the geometric extent of the nested taxonomy.
        
        .. note:: Makes use of the Geometry attribute of the parent level.
        
        """
        extent = self.parent.biomeGeometry.extent
        return extent
    
    def showId(self):
        """
        .. showId
        
        This method returns a unique Id string that is going to be used as unique identifier
        use as a key in the implementation of a cache service.
        
        .. note:: Check this when global analyses are defined
        
        """
        extent = self.getExtent()
        id = self.parent_id
        levels = self.getLevels()
        prefix = settings.NESTED_TAXONOMY_PREFIX
        
        # name = prefix,id,levels,extent
        
        name = '%s:%s:%s:%s' %(prefix,id,levels,extent)
        return name
        
    def cache(self,redis_wrapper,key='default'):
        """
        .. cache
        
        This method stores in cache the NestedGriddedTaxonomy
        using the key parameter as Key.
        
        Parameters
        ==========
            redis_wrapper : StrictRedis object
                This is the redis connection to be used.
                Needs to have specified host, database and port
            key : string
                The key used for storing in the Redis backend.
                If none then it will use the output of the ShowId method.
        
        """
        
        
        if key == 'default':
            key = self.showId()
        
        logger.info('Serializing NestedGriddedTaxonomy. \n Depending on the amount of data it can take some time')
        
        #Cleaning GeoQueryValuesSets fields
        map(lambda grid : grid.removeQuerySets(),self.levels.values())
        
        import pickle
        logger.info('Serializing with pickle')    
        self_pickle = pickle.dumps(self)
        logger.info("Storing in Cache")
        try:
            
            redis_wrapper.set(key,self_pickle)
            return True
        except:
            logger.error("Problem in serializing. The intented caching object could be very big!")
            return self_pickle    
    
    def loadFromCache(self,redis_wrapper,key='default'):
        """
        .. loadFromCache
        
        This method loads the Nested Taxonomy object stored from the Redis
        Cache Backend.
        
        Parameters
        ==========
            redis_wrapper : StrictRedis object
                This is the redis connection to be used.
                Needs to have specified host, database and port
            key : string
                The key used for retrieving the object
                 in the Redis backend. The defailt value means that
                 the object is going to be called using the standard tag
                 used.
        
        """
        
        
        if key == 'default':
            key = self.showId()
        
        logger.info('Retrieving information from NestedGriddedTaxonomy. \n This can take some time')
        r = redis_wrapper
        
        nt_dump = r.get(key)
        if nt_dump:
            import pickle
            cached_nt = pickle.loads(nt_dump)
            for level in self.levels.keys():
                grid_tax = self.levels[level]
                #import ipdb
                #ipdb.set_trace()
                grid_tax.refreshTaxonomiesGeoQuerySets(cached_nt.levels[level])            
            return True
        else:
            logger.error("Object not found in the Cache database")
            raise Exception('Object not found in the Cache database')
    
    
def remap(sorted_list_duple):
    previous_value = sorted_list_duple[0][1]
    j = 0
    new = []
    for indx,current_value in sorted_list_duple:
        if current_value != previous_value:
            new.append((indx,j))
            j += 1
            previous_value = current_value
        else:
            new.append((indx,j))
    return new 
    

def summaryDataFrame(summary):
    
    fam = map(lambda id,fam : (id,fam) , summary['gid'],summary['fam'])
    sp = map(lambda id,fam : (id,fam) , summary['gid'],summary['sp'])
    cls =map(lambda id,fam : (id,fam) , summary['gid'],summary['cls'])
    ord = map(lambda id,fam : (id,fam) , summary['gid'],summary['ord'])
    kng = map(lambda id,fam : (id,fam) , summary['gid'],summary['kng'])
    gns = map(lambda id,fam : (id,fam) , summary['gid'],summary['gns'])
    phy = map(lambda id,fam : (id,fam) , summary['gid'],summary['phy'])

    #Sort by integer representation
    j= map(lambda x : x.sort(key=lambda y : y[1]),[fam,sp,cls,ord,kng,gns,phy])
    
    # Apply re-classification
    sp = remap(sp)
    gns = remap(gns)
    fam = remap(fam)
    ord = remap(ord)
    cls = remap(cls)
    phy = remap(phy)
    kng = remap(kng)
    
    #Sort by GID
    j= map(lambda x : x.sort(key=lambda y : y[0]),[fam,sp,cls,ord,kng,gns,phy])
    
    # Retrieve the gid.
    #Need to check if it's the same value for each.
    gid = map(lambda x : x[0] , fam)
    #Take away first component
    d = {'gid':gid, 'sp' : sp, 'gns' : gns, 'fam' : fam, 'ord' : ord,'cls': cls, 'phy' : phy , 'kng' : kng }    
    for key in ['fam','sp','cls','ord','kng','gns','phy']:
        tax = d[key]
        l = []
        for i,value in enumerate(tax):
            if gid[i] == value[0]:
               
                t = value[1]

                l.append(t)
            else:
                raise Exception('Error in the summary data. GID not the same for rows')
        d[key] = l
    return d     




    
    
    
    