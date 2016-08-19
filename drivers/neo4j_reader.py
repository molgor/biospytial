#!/usr/bin/env python
#-*- coding: utf-8 -*-


import logging
from django.contrib.gis.geos import GEOSGeometry


from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
logger = logging.getLogger('biospatial.neo4j_reader')


TAXDESCEND = "IS_A_MEMBER_OF"
TAXASCEND = "IS_PARENT_OF"

ISNEIGHBOUR = "IS_NEIGHBOUR_OF"
ISIN = "IS_IN"


class Occurrence(GraphObject):
    """
    Lets see hoe this works
    """
    
    __primarykey__ = "pk"
    
    name = Property()
    longitude = Property()
    latitude = Property()
    event_date = Property()
    
    
    #species = RelatedFrom("Specie", "HAS_EVENT")
    genera  = RelatedFrom("Root", "HAS_EVENT")
    #families = RelatedFrom("Family", "HAS_EVENT")
    



class Cell(GraphObject):
    
    __primarykey__ = 'id'
#    __primarylabel__ = 'Cell'
    
    name = Property()
    longitude = Property()
    latitude = Property()
    cell = Property()
    id = Property()
       
    
    
    neighbours = RelatedTo("Cell", ISNEIGHBOUR)
    occurrence  = RelatedFrom("Occurrence", ISIN )
    #families = RelatedFrom("Family", "HAS_EVENT")    

    @property
    def polygon(self):
        polygon = GEOSGeometry(self.cell)
        return polygon




class Root(GraphObject):
    """
    Root model node
    """
    __primarykey__ = 'id'
#    __primarylabel__ = 'Cell'
    
    name = Property()
    abundance = Property()
    levelname = Property()
    keyword = Property()
    level = Property()
       
    
    parent = RelatedTo("Kingdom", TAXASCEND)
    children  = RelatedFrom("Root", TAXDESCEND)
    
    
class Kingdom(GraphObject):
    """
    Kingdom model node
    """
    __primarykey__ = 'id'
#    __primarylabel__ = 'Cell'
    
    name = Property()
    abundance = Property()
    levelname = Property()
    keyword = Property()
    level = Property()
       
    
    parent = RelatedTo("Root", TAXASCEND)
    children  = RelatedFrom("Phylum", TAXDESCEND)



class TaxonomicLevel(object):
    """
    An auxiliary class for encapsulating taxonomic level.
    """
    @property
    def abundance(self):
        return len(self.children)
    

    
    def __init__(self,plain_list_of_nodes,selected_level=7):
        """
        Given an unstructured list of nodes it will build a structure based those nodes.
        By default it selects the Specie Level.
        """
        self.children = filter(lambda n : n['level'] == selected_level,plain_list_of_nodes)
        
        try:
            template_node = self.children[0]
            rel = template_node.match_outgoing(TAXDESCEND).next()
            self.this = rel.end_node()
            self.levelname = template_node['levelname']
            self.name = self.this['name']
        except:
            logger.warning("Empty list of nodes when calling TaxonomicLevel")
            
 

        #self.abundance = len(self.nodes_in_level)
       
    def __repr__(self):
        cad = "< List of Nodes for the Level: %s> "%self.levelname
        return cad


    def isInCell(self):
        """
        Generator wrapper.
        Experimental
        """
        g_rel = self.this.match_outgoing(rel_type=ISIN )
        return g_rel
        

    def getNodeCells(self,limit=10):
        """
        Returns the nodes corresponding to the cells in which the children nodes are located.
        if limit parameter set to 'inf' it will give all the nodes.
        If it's an integer it will give only the number of cells  put as limit.
        
        IT HAS NO RELATION TO ANY SPATIAL CORRELATION.
        THE LIST GIVEN IS NOT NECESARILY CONTINUOUS
        """
        rel_g = self.isInCell()
        cells = []
        check = True
        i = 0

        
        while (check):
            if i < limit:
                i += 1 
                try:
                    node = rel_g.next().end_node()
                    cells.append(node)
                except:
                    return cells   
            elif limit == 'inf':
                check = True
            else:   
                check = False
        return cells
        
        
        

class TreeNeo(object):
    """
    A prototype for reading taxonomic trees stored in the Neo4J database.
    """

    def __init__(self,list_occurrences=[],nodes=[],spatiotemporalcontext=''):
        """
        THIS IS A PROTOTYPE.
        For now it need a list of occurrences GeoQuerySet.
        spatiotemporalcontext should be a structure that defines a compact set.
        
        """
        # First build list of nodes
        # i.e. take all the occurrences, extract the node then put everything in a list
        #self.occurrences = reduce( lambda one,two : one + two, [ map(lambda occurrence : occurrence.getNode(),occurrences )for occurrences in [ taxonomy.occurrences for taxonomy in list_taxonomies]])
        #self.occurrences =  reduce( lambda one,two : one + two ,[ list(occurrence) for occurrence in [ taxonomy.occurrences for taxonomy in list_taxonomies ]])
        self.occurrences = list_occurrences
        self.nodes = nodes
        if not self.nodes:
            try:
                self.nodes = self.setNodes()
            except:
                logger.error("Set Nodes first ")
        
    def loadNodes(self,depth=8):
        """
        Extracts the nodes from the occurrences
        """
        nodes = map(lambda n : n.getDescendingChain(depth),self.occurrences)
        nodes = reduce(lambda a,b : a + b , nodes)
        occ_nodes = map(lambda o : o.getNode(),self.occurrences)
        nodes += occ_nodes
        self.nodes = list(set(nodes))
            
        
    def setOccurrencesFromTaxonomies(self,list_of_taxonomies):
        """
        Updates the occurrences attribute to fit all the occurrences of the given list of taxonomies
        """
        self.occurrences =  reduce( lambda one,two : one + two ,[ list(occurrence) for occurrence in [ taxonomy.occurrences for taxonomy in list_of_taxonomies ]])
         
        
        
    def deriveTreeWithinCell(self):
        """
        This method builds the TREE based on the morphism IS_IN.
        Which means that if the occurrences are from another scheme or are prefiltered the representation 
        of the TREE using this method may not be accurate. 
        """
        pass
    
    
    def __add__(self, tree_neo):
        """
        Operator Overloading for adding Trees!
        In the search of the Monoid!
        New version!
        """
        occurrences = self.occurrences
        other_occurrences = tree_neo.occurrences
        new_occs = occurrences + other_occurrences
        nodes = self.nodes
        other_nodes = tree_neo.nodes
        new_nodes = nodes + other_nodes
        t = TreeNeo(list_occurrences=new_occs,nodes=new_nodes)
        logger.info("Merging Trees")
        t.nodes = list(set(t.nodes))
        return TreeNeo(list_occurrences=new_occs,nodes=new_nodes)
        
    
    def getMeshNodes(self):
        """
        This method retrieves the geometric Information of each node usign the graph structure.
        Relationship "IS_IN"
        """
        reltype = ISIN
        
        