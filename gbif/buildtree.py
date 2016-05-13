#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Buildtree
=========
..
This module provides the functions necessary to build a hierarchical
acyclic and connected graph (Tree) build upon the taxonomic relationships
of the biological classification.

This module makes use of the models define in gbif.models as well as the
common geospatial operations like intersects.
Based on the :ref:`gbif.models` and spatial operations.
"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"

from ete2 import Tree
import logging

logger = logging.getLogger('biospatial.gbif.buildtree')


        


def getGenera(taxonomy_queryset,only_id=False):
    """
    .. 
    This function generates a Tree object derived from the collapse 
    of all *species* under the scope of a spatial queryset.
    
    Parameters
    ----------
    taxonomy_queryset gbif.models / GeoquerySet
    
    
    only_id : Boolean (flag)
        True (default False) means that is going to append the full name of the genera.
        This is a string and can be vary in length. If it is used in big data sets it will 
        impact the amount of memory used because of the heavy load of information.   
     
    
    
    Returns
    -------
    :genera_tree: derived from ete2.TreeNode()
    """
    tax = taxonomy_queryset
    sps = tax.species
    genera = tax.genera
    family_tree = Tree(name='genus_root')
    for genus in genera:
        family_id = genus['parent_id']
        genus_id = genus['genus_id']
        if not only_id:
            name = genus['name']
        else:
            name = genus_id
        ab = genus['ab']
        points = genus['points']
        sp_by_gns = sps.filter(genus_id__exact=genus_id)
        gn_t = Tree(name=name,support=ab)
        gn_t.add_feature('abundance',ab)
        gn_t.add_feature('id',genus_id)
        gn_t.add_feature('parent_id',family_id)
        gn_t.add_feature('genus_id', genus_id)
        gn_t.add_feature('level','genus')
        gn_t.add_feature('points',points)
        #logger.info('Building branch for genus %s' %name)
        for specie in sp_by_gns:
            if not only_id:
                name = specie['name'].split(' ')
                name = name[0]+' '+name[1]
            else:
                name = specie['species_id']
#                 logger.info('The name assigned is %s' %name)
            points = specie['points']
            s = Tree(name = name,support=specie['ab'])
            s.add_feature('abundance',ab)
            s.add_feature('id',specie['species_id'])
            s.add_feature('species_id', specie['species_id'])
            s.add_feature('level','species')
            s.add_feature('points',points)
            gn_t.add_child(child=s)
        family_tree.add_child(child=gn_t)
    return family_tree
            
          
def getFamilies(taxonomic_queryset,genera_tree,only_id=False):
    """
    ..
    This function generates a Tree object derived from the collapse 
    of all *families* under the scope of a spatial queryset.

    Parameters
    ----------
    taxonomy_queryset gbif.models / GeoquerySet
        :genera_tree: Tree derived from getGenera
    
    only_id : Boolean (flag)
        True (default False) means that is going to append the full name of the families.
        This is a string and can be vary in length. If it is used in big data sets it will 
        impact the amount of memory used because of the heavy load of information.   
     
    
    
    Returns
    -------
    :families_tree: derived from ete2.TreeNode()
    """
    tax = taxonomic_queryset
    families = tax.families
    genera = tax.genera
    orders_tree = Tree(name='order_root')
    for family in families:
        order_id = family['parent_id']
        if not only_id:
            name = family['name']
        else:
            name = family['family_id']
        ab = family['ab']
        #Add here the geometric feature (if necessary)
        points = family['points']
        family_id = family['family_id']
        famTree = Tree(name=name,support=ab)
        famTree.add_feature('abundance',ab)
        famTree.add_feature('id',family_id) 
        famTree.add_feature('parent_id',order_id)       
        famTree.add_feature('family_id',family_id)
        famTree.add_feature('level','family')
        famTree.add_feature('points',points)
        gens_by_fam = genera.filter(parent_id__exact=family_id)
        for genus in gens_by_fam:
            id_g = genus['genus_id']
            #Filter the branch of the tree with the selected genus (for loop)
            branch = reduce(lambda node : node.next(),filter(lambda branch : branch.genus_id==id_g,genera_tree.get_children() ))
            # Attach the branch to the family tree
            famTree.add_child(child=branch)
        orders_tree.add_child(child=famTree)
    return orders_tree
 

def getOrders(taxonomic_queryset,families_tree,only_id=False):
    """
    This function generates a Tree object derived from the collapse 
    of all *orders* under the scope of a spatial queryset.

    Parameters
    ----------
    taxonomy_queryset gbif.models / GeoquerySet
    :families_tree: Tree derived from getFamilies

    only_id : Boolean (flag)
        True (default False) means that is going to append the full name of the orders.
        This is a string and can be vary in length. If it is used in big data sets it will 
        impact the amount of memory used because of the heavy load of information.   
 

    
    Returns
    -------
    :orders_tree: derived from ete2.TreeNode()    
    """
    tax = taxonomic_queryset
    orders = tax.orders
    families = tax.families
    classTree = Tree(name='class_root')
    logger.info("[gbif.buildtree] Collapsing Orders")
    for order in orders:
        class_id = order['parent_id']
        if not only_id:      
            name = order['name']
        else:
            name = order['order_id']
        ab = order['ab']
        #Add here the geometric feature (if necessary)
        points = order['points']
        order_id = order['order_id']
        #logger.info("Colapsing Order id: %s" %order_id)
        orderTree = Tree(name=name,support=ab)
        orderTree.add_feature('abundance',ab)
        orderTree.add_feature('id',order_id)
        orderTree.add_feature('parent_id',class_id)        
        orderTree.add_feature('order_id',order_id)
        orderTree.add_feature('level','order')
        orderTree.add_feature('points',points)
        #orderTree.add_feature('points',points)
        fams_by_order = families.filter(parent_id__exact=order_id)
        for family in fams_by_order:
            id_f = family['family_id']
            #Filter the branch of the tree with the selected genus (for loop)
            branch = reduce(lambda node : node.next(),filter(lambda branch : branch.family_id==id_f,families_tree.get_children()))
            #print branch
            # Attach the branch to the family tree
            orderTree.add_child(child=branch)
        classTree.add_child(child=orderTree)
    return classTree   


def getClasses(taxonomic_queryset,orders_tree,only_id=False):
    """
    ..
    This function generates a Tree object derived from the collapse 
    of all *classes* under the scope of a spatial queryset.

    Parameters
    ----------
    taxonomy_queryset gbif.models / GeoquerySet
        :orders_tree: Tree derived from getOrders
    
    only_id : Boolean (flag)
        True (default False) means that is going to append the full name of the classes.
        This is a string and can be vary in length. If it is used in big data sets it will 
        impact the amount of memory used because of the heavy load of information.   
 
    
    Returns
    -------
    :classes_tree: derived from ete2.TreeNode() 


    """
    tax = taxonomic_queryset
    classes = tax.classes
    orders = tax.orders
    phylumTree = Tree(name='phylum_root')
    logger.info("[gbif.buildtree] Collapsing Classes")
    for class_ in classes:
        phylum_id = class_['parent_id']
        if not only_id: 
            name = class_['name']
        else:
            name = class_['class_id']
        ab = class_['ab']
        #Add here the geometric feature (if necessary)
        points = class_['points']
        class_id = class_['class_id']
        #logger.info("Colapsing Class id: %s" %class_id)
        classTree = Tree(name=name,support=ab)
        classTree.add_feature('id',class_id)
        classTree.add_feature('abundance',ab)
        classTree.add_feature('parent_id',phylum_id)
        classTree.add_feature('class_id',class_id)
        classTree.add_feature('level','class')
        classTree.add_feature('points',points)
        orders_by_class = orders.filter(parent_id__exact=class_id)
        for order in orders_by_class:
            id_o = order['order_id']
            #Filter the branch of the tree with the selected genus (for loop)
            branch = reduce(lambda node : node.next(),filter(lambda branch : branch.order_id==id_o,orders_tree.get_children()))
            #print branch
            # Attach the branch to the family tree
            classTree.add_child(child=branch)
        phylumTree.add_child(child=classTree)
    return phylumTree  

def getPhyla(taxonomic_queryset,classes_tree,only_id=False):
    """
    ...
    This function generates a Tree object derived from the collapse 
    of all *phyla* under the scope of a spatial queryset.

    Parameters
    ----------
    taxonomy_queryset gbif.models / GeoquerySet
        :classes_tree: Tree derived from getclasses

        only_id : Boolean (flag)
            True (default False) means that is going to append the full name of the Phyla.
            This is a string and can be vary in length. If it is used in big data sets it will 
            impact the amount of memory used because of the heavy load of information.   
  
    
    Returns
    -------
    :phyla_tree: derived from ete2.TreeNode()   
    """
    tax = taxonomic_queryset
    phyla = tax.phyla
    classes = tax.classes
    kingdomTree = Tree(name='kingdom_root')
    logger.info("[gbif.buildtree] Collapsing Phyla")
    for phylum in phyla:
        kingdom_id = phylum['parent_id']
        if not only_id:         
            name = phylum['name']
        else:
            name = phylum['phylum_id']
        ab = phylum['ab']
        #Add here the geometric feature (if necessary)
        points = phylum['points']
        phylum_id = phylum['phylum_id']
        #logger.info("Colapsing Phylum: %s" %name)
        phylumTree = Tree(name=name,support=ab)
        phylumTree.add_feature('id',phylum_id)
        phylumTree.add_feature('abundance',ab)
        phylumTree.add_feature('parent_id',kingdom_id)        
        phylumTree.add_feature('phylum_id',phylum_id)
        phylumTree.add_feature('level','phylum')
        phylumTree.add_feature('points',points)
        classes_by_phylum = classes.filter(parent_id__exact=phylum_id)
        for class_ in classes_by_phylum:
            id_c = class_['class_id']
            #Filter the branch of the tree with the selected genus (for loop)
            branch = reduce(lambda node : node.next(),filter(lambda branch : branch.class_id==id_c,classes_tree.get_children()))
            #print branch
            # Attach the branch to the family tree
            phylumTree.add_child(child=branch)
        kingdomTree.add_child(child=phylumTree)
    return kingdomTree  

def getKingdoms(taxonomic_queryset,phyla_tree,only_id=False):
    """
    ...
    This function generates a Tree object derived from the collapse 
    of all *kingdoms* under the scope of a spatial queryset.

    Parameters
    ----------
        taxonomy_queryset gbif.models / GeoquerySet
            :phyla_tree: Tree derived from getKingdoms

        only_id : Boolean (flag)
            True (default False) means that is going to append the full name of the kingdoms.
            This is a string and can be vary in length. If it is used in big data sets it will 
            impact the amount of memory used because of the heavy load of information.   
 
    
    Returns
    -------
    :kingdoms_tree: derived from ete2.TreeNode()   
    
    
    """
    tax = taxonomic_queryset
    kingdoms = tax.kingdoms
    total_abundance = sum(map(lambda a : a['ab'],kingdoms))
    phyla = tax.phyla
    TreeOfLife = Tree(name='Life')
    TreeOfLife.add_feature("abundance", total_abundance)
    TreeOfLife.add_feature("id", 'LOCAL_LUCA')
    TreeOfLife.add_feature("parent_id", False)
    TreeOfLife.add_feature("level", "root")
    logger.info("[gbif.buildtree] Collapsing Kingdoms")
    for kingdom in kingdoms:
        kingdom_id = 0
        if not only_id:         
            name = kingdom['name']
        else:
            name = kingdom['kingdom_id']    
        ab = kingdom['ab']
        #Add here the geometric feature (if necessary)
        points = kingdom['points']
        kingdom_id = kingdom['kingdom_id']
        #logger.info("Colapsing kingdom: %s" %name)
        kingdomTree = Tree(name=name,support=ab)
        kingdomTree.add_feature('id',kingdom_id)
        kingdomTree.add_feature('abundance',ab)
        kingdomTree.add_feature('parent_id','LOCAL_LUCA')
        kingdomTree.add_feature('kingdom_id',kingdom_id)
        kingdomTree.add_feature('level','kingdom')
        kingdomTree.add_feature('points',points)
        phyla_by_kingdom = phyla.filter(parent_id__exact=kingdom_id)
        for phylum in phyla_by_kingdom:
            id_p = phylum['phylum_id']
            #Filter the branch of the tree with the selected genus (for loop)
            branch = reduce(lambda node : node.next(),filter(lambda branch : branch.phylum_id==id_p,phyla_tree.get_children()))
            #print branch
            # Attach the branch to the family tree
            kingdomTree.add_child(child=branch)
        TreeOfLife.add_child(child=kingdomTree)
    return TreeOfLife  


def getTOL(taxonomic_queryset,only_id=False):
    """
    ...
    Calculates the entire Local Tree of Life derived from the collapsing functions.
    Gives the complete tree of life
    
    Parameters
    ----------
        only_id : Boolean (flag)
            True (default False) means that is going to append the full name of the taxons.
            This is a string and can be vary in length. If it is used in big data sets it will 
            impact the amount of memory used because of the heavy load of information.   
    
    Returns
    -------
    :local_tree_of_life: derived from ete2.TreeNode() 
    
    See also
    --------
    gbif.taxonomy : Where this module is highly used.
 
    """
    tax = taxonomic_queryset
    #tree_genera = getGenera(tax)
    
    TOL = getKingdoms(tax,getPhyla(tax,getClasses(tax,getOrders(tax,getFamilies(tax,getGenera(tax,only_id=only_id),only_id=only_id),only_id=only_id),only_id=only_id),only_id=only_id),only_id=only_id)
    
    return TOL



