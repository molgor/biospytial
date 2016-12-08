#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Study 1
=======
..
This is the first analysis on the series *Studies on Biodiversity*.
This study explores the intrinsic properties of the changes (ratios) from different
taxonomic levels at the highest resolution grid. 
Each cell has a defined taxonomy object and, as seen before, each taxonomy has a taxonomic tree associated
this information is converted to a 7x7 Matrix that relates the ratios between the different taxonomic levels.
For example, the entry 2,1 is the ratio between the genus and the specie level.

The study selects the polygons for a given eco-region type and filter the Taxonomies that are true under the operation of intersection.
For each of these subsets an average and std_dev matrix is calculated to characterize the mean and variation of the intrinsic properties with in an
ecoregion. This process is made for all ecoregions' type and the results are shown as graphs.


 
"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"

from gbif.taxonomy import NestedTaxonomy
from gbif.models import Occurrence
from ecoregions.models import Ecoregion
from django.contrib.gis.db.models import Union, Min
import biospytial.settings as settings
import pandas as pn
from sketches.models import Country

def PanelizeMatrices(list_of_taxonomies):
    """
    ..
    Extracts the intrinsic matrices from the taxonomies given as parameters.
    
    Returns
    =======
        a Panel
            Similar to a matrix with the difference that each entry is a list.
            Each element of this list correspond to the entry of the intrinsic matrix 
        
    """
    all_entries = []
    for i in range(7):
        li = []
        for j in range(7):   
            i_j = map(lambda t : t.intrinsicM[i,j],list_of_taxonomies)
        li.append(pn.Series(i_j))
        all_entries.append(li)
    return all_entries
    
    
def PanelizeMatrices_dic(list_of_taxonomies):
    """
    ..
    Extracts the intrinsic matrices from the taxonomies given as parameters.
    
    Returns
    =======
        a Panel
            Similar to a matrix with the difference that each entry is a list.
            Each element of this list correspond to the entry of the intrinsic matrix 
        
    """
    all_entries = {}
    for i,tax_name_i in enumerate(settings.TAXONOMIC_TREE_KEYS):
        li = {}
        for j,tax_name_j in enumerate(settings.TAXONOMIC_TREE_KEYS):   
            i_j = map(lambda t : t.intrinsicM[i,j],list_of_taxonomies)
            li[tax_name_j] = pn.Series(i_j)
        all_entries[tax_name_i] = li
    return all_entries    


# Taxonomies by Ecoregion


def getMeanStdfromPanel(panel):
    """
    ..
    Returns two dataframes Mean and Std in which  Mean is the average of the series for the i,j Serie
    Std is the standard deviation Matrix in which each entry is the std of the i,j serie.
    
    """
    mean = {}
    std = {}
    keys = ['sp','gns','fam','ord','cls','phy','kng']
    for i,key_i in enumerate(keys):
        means = {}
        stds = {}
        for j,key_j in enumerate(keys):
            means[str(j+1)+key_j] = panel[key_i][key_j].mean()
            stds[str(j+1)+key_j] = panel[key_i][key_j].std()
        mean[str(i+1)+key_i] = means
        std[str(i+1)+key_i] = stds
    return pn.DataFrame(mean),pn.DataFrame(std)
             
def getTaxonomiesPerEcoregion_dic(z_numbers,regions_polys_dic,list_taxonomies):
    """
    This method generate a dictionary for each ecoregion class (polygon) 
    with the taxonomies that:
    
    * Intersects with each polygon 
    * Are in the interior of each polygon (within)
    
    Parameters
    ==========
        
        z_numbers : list 
            The ordered list of ecoregion types
        regions_polys_dic : dictionary
            The dictionary that defines the class and the multipolygon object
        list_taxonomies : list
            The list of taxonomies that are going to be geoprocessed (filtered)
    
    
    Returns
    =======
    
        taxonomies_per_ecoregion : dictionary
            Complex structure with keys as ecoregion type and values as:
                regions : Multipolygon
                taxonomies_intersects : list of taxonomies that intersect each class
                taxonomies_within : list of taxonomies that are in the interior (within) of each polygon.
                
    """            

    taxonomies_per_ecoregion_mergpol = {}
    for i in z_numbers:
        poly = regions_polys_merged[int(i)]['polygon']
        tax_intersect = filter(lambda t : t.biomeGeometry.intersects(poly),list_taxonomies)
        tax_list_within = filter(lambda t : t.biomeGeometry.within(poly),list_taxonomies)
        monoid = {'polygons' : poly, 'taxonomies_intersect' : tax_intersect,'taxonomies_kernel':tax_list_within}
        taxonomies_per_ecoregion_mergpol[int(i)] = monoid
    return taxonomies_per_ecoregion_mergpol

def getRichnessFromTaxonomies(tax_list):
    dunno = {'id': [] ,'occurrences': [] ,'species' : [] ,'genera' : [] ,'families' : [], 'orders' : [],'classes': [], 'phyla' :[], 'kingdoms':[],'r_sp_gn':[],'r_gn_fam':[],'r_fam_ord':[],'r_ord_cls':[], 'r_cls_phy':[],'r_phy_kng':[]}
    def puke_data(taxonomy):
        M = taxonomy.intrinsicM
        chain_change = []
        for i in range(1,7):
            chain_change.append(M[i-1,i])
        return chain_change
        #return taxonomy.gid, t['species'],t['genera'],t['families'],t['orders'],t['classes'],t['phyla'],t['kingdoms']  
    #Get by tax level
    dunno['id'] = map(lambda t : t.gid , tax_list)
    dunno['occurrences'] = map(lambda t : t.richness['occurrences'] , tax_list)
    dunno['species'] = map(lambda t : t.richness['species'] , tax_list)
    dunno['genera'] = map(lambda t : t.richness['genera'] , tax_list)
    dunno['families'] = map(lambda t : t.richness['families'] , tax_list)
    dunno['orders'] = map(lambda t : t.richness['orders'] , tax_list)
    dunno['classes'] = map(lambda t : t.richness['classes'] , tax_list)
    dunno['phyla'] = map(lambda t : t.richness['phyla'] , tax_list)
    dunno['kingdoms'] = map(lambda t : t.richness['kingdoms'] , tax_list)
    competition = map(lambda t: puke_data(t),tax_list)
    dunno['r_sp_gn'] = map(lambda c : c[0],competition)
    dunno['r_gn_fam'] = map(lambda c : c[1],competition)
    dunno['r_fam_ord'] = map(lambda c : c[2],competition)
    dunno['r_ord_cls'] = map(lambda c : c[3],competition)
    dunno['r_cls_phy'] = map(lambda c : c[4],competition)
    dunno['r_phy_kng'] = map(lambda c : c[5],competition)                    
        
    import pandas as pn
    all_tax=pn.DataFrame(dunno, index=dunno['id'],columns=['occurrences','species','genera','families','orders','classes','phyla','kingdoms','r_sp_gn','r_gn_fam','r_fam_ord','r_ord_cls', 'r_cls_phy','r_phy_kng'])    
    return all_tax


#def initializeGrid(tax_list,):



biosphere = Occurrence.objects.all()
#Would be good to put some temporal filtering here
#DOne
biosphere = biosphere.filter(year__gt=2000)

#Filter terrestrial taxonomies
mex = Country.objects.filter(name__contains='exico').get()

biosphere = biosphere.filter(geom__intersects=mex.geom)

nt = NestedTaxonomy(36,biosphere,start_level=3,end_level=10,generate_tree_now=False)


#Select the study area
study_area = nt.parent.biomeGeometry

ecoregions = Ecoregion.objects.all()
ecoregions_in_area = ecoregions.filter(geom__within=study_area)

zonenumbers = list(set(map(lambda e : e.num_zona,ecoregions_in_area)))

z_numbers = filter(lambda x : x != None,zonenumbers)


from django.contrib.gis.db.models import Union, Min
regions_polys_merged = {}
for i in z_numbers:
    regions_polys_merged[int(i)]=ecoregions_in_area.filter(num_zona=int(i)).aggregate(polygon=Union('geom'),name=Min('nomzonecol'.encode('latin-1')),zone_id=Min('num_zona'))

   
regions_polys = {}
for i in z_numbers:
    regions_polys[int(i)]=map(lambda p : p.geom , ecoregions_in_area.filter(num_zona=int(i)))


    
#===============================================================================
# 
# taxonomies_per_ecoregion = {}
# for i in z_numbers:
#     tax_list = []
#     for poly in regions_polys[int(i)]:
#         tax_list.append(map(lambda t : t.biomeGeometry.intersects(poly),l9.taxonomies))
#     taxonomies_per_ecoregion[i] = tax_list
#     
#===============================================================================
import redis
r = redis.StrictRedis()
l7 = nt.levels[7]

#l9.restoreTaxonomiesFromCache(r)
l9  = nt.levels[9]
l10 = nt.levels[10]
l10.restoreTaxonomiesFromCache(r)
max = len(l7.taxonomies)
#filtered_taxs = getTaxonomiesPerEcoregion_dic(z_numbers,regions_polys,l10.taxonomies)
"""
for i,t in enumerate(l7):
    if not r.exists(t.showId()):
        t.calculateIntrinsicComplexity()
        t.buildInnerTree(deep=True)
        t.cache(r)
        c="Cached %s percent" %(str((float(i)/max)*100))
        print c
    else:
        c="Stored already  %s " %(str((float(i)/max)*100))
        print c
"""