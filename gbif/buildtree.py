#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Function to build phylogenetic tree
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


        


def getGenera(taxonomy_queryset):
    """
    This function returns a Tree object collapsing all the species.
    """
    tax = taxonomy_queryset
    sps = tax.species
    genera = tax.genera
    family_tree = Tree(name='genus_root')
    for genus in genera:
        family_id = genus['parent_id']
        genus_id = genus['genus_id']
        name = genus['name']
        ab = genus['ab']
        points = genus['points']
        sp_by_gns = sps.filter(genus_id__exact=genus_id)
        gn_t = Tree(name=name,support=ab)
        gn_t.add_feature('genus_id', genus_id)
        gn_t.add_feature('level','genus')
        gn_t.add_feature('points',points)
        #logger.info('Building branch for genus %s' %name)
        for specie in sp_by_gns:
            name = specie['name'].split(' ')
            name = name[0]+' '+name[1]
            points = specie['points']
            s = Tree(name = name,support=specie['ab'])
            s.add_feature('species_id', specie['species_id'])
            s.add_feature('level','species')
            s.add_feature('points',points)
            gn_t.add_child(child=s)
        family_tree.add_child(child=gn_t)
    return family_tree
            
          
def getFamilies(taxonomic_queryset,genera_tree):
    """
    Taxonomic queryset aggregated of class Taxonomy
    genera_tree is the tree obtained from building of genera.
    """
    tax = taxonomic_queryset
    families = tax.families
    genera = tax.genera
    orders_tree = Tree(name='order_root')
    for family in families:
        order_id = family['parent_id']
        name = family['name']
        ab = family['ab']
        #Add here the geometric feature (if necessary)
        points = family['points']
        family_id = family['family_id']
        famTree = Tree(name=name,support=ab)
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
 

def getOrders(taxonomic_queryset,families_tree):
    """
    Taxonomic queryset es un agregado. objeto de Taxonomy
    families_tree is the tree obtained from building of families.
    """
    tax = taxonomic_queryset
    orders = tax.orders
    families = tax.families
    classTree = Tree(name='class_root')
    logger.info("[gbif.buildtree] Collapsing Orders")
    for order in orders:
        class_id = order['parent_id']
        name = order['name']
        ab = order['ab']
        #Add here the geometric feature (if necessary)
        points = order['points']
        order_id = order['order_id']
        #logger.info("Colapsing Order id: %s" %order_id)
        orderTree = Tree(name=name,support=ab)
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


def getClasses(taxonomic_queryset,orders_tree):
    """
    Taxonomic queryset es un agregado. objeto de Taxonomy
    families_tree is the tree obtained from building of families.
    """
    tax = taxonomic_queryset
    classes = tax.classes
    orders = tax.orders
    phylumTree = Tree(name='phylum_root')
    logger.info("[gbif.buildtree] Collapsing Classes")
    for class_ in classes:
        phylum_id = class_['parent_id']
        name = class_['name']
        ab = class_['ab']
        #Add here the geometric feature (if necessary)
        points = class_['points']
        class_id = class_['class_id']
        #logger.info("Colapsing Class id: %s" %class_id)
        classTree = Tree(name=name,support=ab)
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

def getPhyla(taxonomic_queryset,classes_tree):
    """
    Taxonomic queryset es un agregado. objeto de Taxonomy
    families_tree is the tree obtained from building of families.
    """
    tax = taxonomic_queryset
    phyla = tax.phyla
    classes = tax.classes
    kingdomTree = Tree(name='kingdom_root')
    logger.info("[gbif.buildtree] Collapsing Phyla")
    for phylum in phyla:
        kingdom_id = phylum['parent_id']
        name = phylum['name']
        ab = phylum['ab']
        #Add here the geometric feature (if necessary)
        points = phylum['points']
        phylum_id = phylum['phylum_id']
        #logger.info("Colapsing Phylum: %s" %name)
        phylumTree = Tree(name=name,support=ab)
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

def getKingdoms(taxonomic_queryset,phyla_tree):
    """
    Taxonomic queryset es un agregado. objeto de Taxonomy
    families_tree is the tree obtained from building of families.
    """
    tax = taxonomic_queryset
    kingdoms = tax.kingdoms
    phyla = tax.phyla
    TreeOfLife = Tree(name='LUCA_root')
    logger.info("[gbif.buildtree] Collapsing Kingdoms")
    for kingdom in kingdoms:
        kingdom_id = 0
        name = kingdom['name']
        ab = kingdom['ab']
        #Add here the geometric feature (if necessary)
        points = kingdom['points']
        kingdom_id = kingdom['kingdom_id']
        #logger.info("Colapsing kingdom: %s" %name)
        kingdomTree = Tree(name=name,support=ab)
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


def getTOL(taxonomic_queryset):
    """
    Gives the complete tree of life
    """
    tax = taxonomic_queryset
    #tree_genera = getGenera(tax)
    TOL = getKingdoms(tax,getPhyla(tax,getClasses(tax,getOrders(tax,getFamilies(tax,getGenera(tax))))))
    
    return TOL




