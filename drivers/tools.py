# Some tools for handling the TreeNeo's

# Author: Juan Escamilla 
# Date: 7/4/2017
 
#!/usr/bin/env python
#-*- coding: utf-8 -*-

# visualizing and analysing
from networkx.drawing.nx_agraph import graphviz_layout
import networkx as nt
import numpy as np
from holoviews.operation.datashader import datashade, bundle_graph
import holoviews as hv
from matplotlib.pyplot import cm

def RankTaxonomicLevel(tree,list_trees,level):
    """
    Returns a list of ranks from top to bottom of the most frequent taxa using the attribute n_presence
    """
    #tree.countNodesFrequenciesOnList(list_of_trees)
    taxa = tree.levels[level]
    n = len(list_trees)
    taxa.sort(key=lambda t : t.n_presences_in_list,reverse=True)
    taxas = map(lambda node : (node,float(node.n_presences_in_list)/n),taxa)
    return taxas


def TreeToTable(tree,level):
    """
    Uses the rank list to return a pandas datatable with frequencies.
    """
    taxa = RankTaxonomicLevel(tree, level)
    pass



def plotTree(treeneo, depth=6,label_depth=5):
    """
    Plot the graph using a circo layout
    DEPRECATED. Use to_interactivePlot
    """
    ## Some functions for visualising
    extractNames = lambda graph : {k:v for (k,v) in map(lambda n : (n,n.name),graph.nodes())}
    extractColors = lambda graph :  map(lambda n : n.level,graph.nodes())
    #extractfreqs = lambda graph :  np.array(map(lambda n : n.n_presences_in_list,graph.nodes()))
    gt = treeneo.toNetworkx(depth_level=depth)
    root = treeneo.node
    pos = graphviz_layout(gt,prog='circo',root=root.node.name)
    g_labels = treeneo.toNetworkx(depth_level=4)
    #x = nt.draw(gt,pos,labels=extractNames(g_labels),node_color=extractColors(gt),node_size=extractfreqs(gt)*500)
    x = nt.draw(gt,pos,labels=extractNames(g_labels),node_color=extractColors(gt))

    return x


def to_interactivePlot(treeneo,depth=7,label_depth=7):
    """
    Creates and returns a set of Holoviews and Bokeh objets that 
    represent a given tree.
    Parameters:
        treeneo : A TreeNeo object.
        depth : (Integer) the depth of the tree to be generated (1 :root, 7 : species)
        label_depth : (Integer) the depth for labels.

    """

    def buildLabel(row,labelid=6,refresh=False):
        if row['level']==labelid:
            return(row['name'])
        elif (not refresh):
            try:
                return(row['namelabel'])
            except:
                return('')
        else:
            return('')
    
    def buildAngle(row,centerx=0,centery=0):
        # The function returns rad, let's convert to degrees.
        # seems that works like that
        ny = centery - row['y']
        nx = centerx - row['x']
        try:
            alpha = np.arctan(ny/nx)
        except ZeroDivisionError:
            alpha = 0
        d =  alpha * 180 / np.pi
        return(d)
    
    gt = treeneo.toNetworkx(depth_level=depth)
    pos = graphviz_layout(gt,prog='twopi',root='LUCA',args='')
    graphvis = hv.Graph.from_networkx(gt,pos,label='nodes').opts(
               tools=['hover'],
               width=1000,
               height= 1000,
               node_color='level',
               node_alpha=0.5,
               node_size=hv.dim('freq')* 100,
               cmap=cm.YlGn,
               padding=0.2,
               show_legend=True,
               legend_position='bottom',
               edge_color='yellow',edge_alpha=0.5,
               bgcolor='dimgrey' )
    # Fancy vis of edges
    bundles = bundle_graph(graphvis).opts(
                        edge_color='yellow',
                        edge_alpha=0.3)
    # Center
    cx = pos['LUCA'][0]
    cy = pos['LUCA'][1]
    # Make labels
    for i in range(2,label_depth):
        graphvis.nodes.data['namelabel'] = graphvis.nodes.data.apply(buildLabel,axis=1,labelid=i)

    # Create angles
    graphvis.nodes.data['angle'] = graphvis.nodes.data.apply(buildAngle,
            axis=1,centerx=cx,centery=cy)
    datalabels = graphvis.nodes.data[['x','y','namelabel','freq','angle','level']]
    const = 3
    constlab = 0.1
    #datalabels['namesize'] = datalabels['freq'] * const * ((8 - datalabels['level']) * constlab)
    datalabels['namesize'] =(8 - datalabels['level']) * const
    labels = hv.Labels(datalabels,['x','y'],
             vdims=['namelabel','freq','angle','namesize','level']).opts(
                     angle='angle',
                     text_font_size='namesize',
                     text_color='cornsilk',
                     bgcolor='dimgray')
    out = {'graph' : bundles , 'labels' :labels }
    return(out)


def redisConnection(host='redis'):
    """
    A Redis connection for Biospytial
    """
    import redis
    rc = redis.StrictRedis(host=host)
    return rc
