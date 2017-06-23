#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Encoders module
================

.. Export TreeNodes to a json format

"""

from json import JSONEncoder
class TreeNodeEncoder(JSONEncoder):
    def default(self, o):
        #d = [o.id,o.name,o.n_presences_in_list,o.levelname]
        d = "%s, 'name' : %s, 'freq': %s, 'levelname' : %s"%(o.id,o.name,o.n_presences_in_list,o.levelname)
        #d = { 'name' : o.name, 'id' : o.id, 'n_presences_in_list': o.n_presences_in_list,'level':o.level,'levelname':o.levelname} 
        return d   


def nodesToList(networkxGraph):
    """
    Converts the nodes from a NetworkxGraph Graph object into a string to be exported to json.
    Following the especification for force graph in d3.js from: https://bl.ocks.org/mbostock/4062045
    """
    nodes = map(lambda node : node.character,networkxGraph)
    return nodes



def edgesToList(networkxGraph):
    """
    Converts the edges from a NetworkxGraph object into a list to be exported to json.
    It uses the standard keys (source, target, id, key) gused by force-graph in d3.js
    ONLY WORKS FOR NON Hypergraphs i.e. every edge connects two nodes.
    """
    items = networkxGraph.edge.iteritems()
    
    ## template
    # (<LocalTree | Genus: Monstera - n.count : 7- | AF: 4 >,
    # {<LocalTree | Family: Araceae - n.count : 53- | AF: 9 >: {'weight': 53}})
    g_t = lambda (source,dictionary) : {"source" : source.id, "target" : reduce(lambda a,b : a+b  , map( lambda (key,value) : ( key.id,  value) ,dictionary.items()))}
    ff = lambda d : {"source" : d['source'] , "target" : d['target'][0] , 'weight' : d['target'][1]['weight']}
    extractEdge = lambda x : ff(g_t(x))
    return map(extractEdge,items)


def exportJSOND3(networkxGraph):
    """
    Exports networkx graph object into a json format for use in D3.js
    """
    d = {}
    d['nodes'] = nodesToList(networkxGraph)
    d['links'] = edgesToList(networkxGraph)
    return d
    
    