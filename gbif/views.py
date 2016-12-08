#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""

Http interfaces using Views
===========================
..
This module implements command-line tools for use in external applications through HTTP request/responses.
For example: Using QGIS actions and the PyQT webkit it is possible to develop interactive analysis in the OpenSource
Desktop GIS.

.. note::
    This is where all the interfaces between biospytial and QGIS or Browsers should be living.

"""

__author__ = "Juan Escamilla Mólgora"
__copyright__ = "Copyright 2015, JEM"
__license__ = "GPL"
__version__ = "2.2.1"
__mantainer__ = "Juan"
__email__ ="molgor@gmail.com"
__status__ = "Prototype"



from django.shortcuts import render
import biospytial.settings as settings

from django.template.loader import get_template
from django.template import Context


# Create your views here.
from django.http import HttpResponse

from gbif.models import Occurrence
from mesh.models import initMesh
from gbif.taxonomy import GriddedTaxonomy
from ete2 import TreeStyle
import logging
logger = logging.getLogger('biospytial.gbif.views')


def HelloWorld(request):
    t = get_template('base.html')
    mensj = 'Cara de cola'
    html = t.render(Context({'mensaje':mensj }))
    return HttpResponse(html)


def showTreeInGrid(request):
    """
    .. showTreeInGrid:
    
    Performs a selection, spatial filter and returns an image.
    
    Parameters in GET variable
    ===========================
    grid_level : int
        The grid layer.
    taxonomic_level : string
        The taxonomic level to be shown. 
        Options are: sp, gns, fam, ord, cls, phy, king
        
    Returns
    =======
    HTTP RESPONSE
    with an image showing the tree.
    
    See figure: 
    .. image:: 
    """
    from ete2.treeview import drawer
    from PyQt4 import QtCore
    import ipdb
    
    response = HttpResponse()
    get = request.GET
    try:
        
        gid = int(get['gid'])
        grid_level = int(get['g_l'])
        taxonomic_level = get['tax_lvl']
    except:
        response.content='Bad request. Check GET variable definitions'
        response.status_code = 500
        return response
    
    biome = Occurrence.objects.all() 
    mesh = initMesh(grid_level)
    try:
        cell = mesh.objects.get(id=gid)
    except:
        logger.error("Selected id does not exist in selected grid")
        return None
    
    import os.path
    
    head_path = settings.PATH_IMAGES
    filename = "%s-%s-%s.png" %(grid_level,gid,taxonomic_level)
    file_ = head_path+filename
    logger.info('Writing in: %s'%file_)    
    if not os.path.isfile(file_):
        logger.info("The image doens't exist") 
        gb=GriddedTaxonomy(biome,cell,generate_tree_now=True)
        forest = gb.taxonomies[0].forest

        ts = TreeStyle()
        ts.show_leaf_name = True
        ts.mode = "c"
        ts.arc_start = -180 # 0 degrees = 3 o'clock
        ts.arc_span = 360
        try:
            #ipdb.set_trace()
            forest[taxonomic_level].render(file_, w=100, units="mm",tree_style=ts)
            #drawer.exit_gui(1, 1)
            
            #logger.info(QtCore.QThreadPool)
            del(forest[taxonomic_level])
        except:
            logger.error('Something went wrong with the image rendering')
        #del(forest)
    #ipdb.set_trace()
    template = get_template('base.html')
    html = template.render(Context({'gid':gid,'taxonomic_level':taxonomic_level,'grid_level':grid_level,'image_path':filename}))
    response.content=(html)
    #response.content=str(forest[taxonomic_level])
    response.status_code = 200
    
    return response



def showAllLevelsInTreeInGrid(request):
    """
    Performs a selection, spatial filter and returns an image.
    grid_level is the grid layer.
    taxonomic_level is the taxonomic level to be shown. Options are:
    sp, gns, fam, ord, cls, phy, king
    """

    import ipdb
    
    response = HttpResponse()
    get = request.GET
    try:
        
        gid = int(get['gid'])
        grid_level = int(get['g_l'])
        names = int(get['names'])
        if names > 0:
            only_id = False
        else:
            only_id = True
        #taxonomic_level = get['tax_lvl']
    except:
        response.content='Bad request. Check GET variable definitions'
        response.status_code = 500
        return response
    
    biome = Occurrence.objects.all() 
    mesh = initMesh(grid_level)
    try:
        cell = mesh.objects.get(id=gid)
    except:
        logger.error("Selected id does not exist in selected grid")
        return None
    
    import os.path
    tax_levels = ['sp','gns','fam','cls','ord','phy','kng']
    tax_keys = {'sp':'1.Species','gns':'2. Genera','fam':'3. Families','ord':'4. Orders','cls':'5. Classes','phy':'6. Phyla','kng':'7. Kingdoms'}
    rich_keys = { 'oc':'occurrences','sp' :'species','gns':'genera','fam':'families','cls':'classes','ord':'orders','phy':'phyla','kng':'kingdoms'}
    img_paths = {}
    #THIS IS VERY VERY WRONG AND I WOULD SUGGEST A REFACTORING like the use of a binary written copy in disk about the object in question (cached)
    gb=GriddedTaxonomy(biome,cell,generate_tree_now=True,use_id_as_name=only_id)
    taxonomy = gb.taxonomies[0]
    #ipdb.set_trace()
    mat_complex = taxonomy.calculateIntrinsicComplexity()
    for taxonomic_level in tax_levels:
        head_path = settings.PATH_IMAGES
        filename = "%s-%s-%s.png" %(grid_level,gid,taxonomic_level)
        file_ = head_path+filename
        logger.info('Writing in: %s'%file_)    
        if not os.path.isfile(file_):
            logger.info("The image doens't exist") 
            try:
                if gb not in locals():
                    #gb=GriddedTaxonomy(biome,cell,generate_tree_now=True)
                    logger.info("Gridded taxonomy doesn't found")
            except:
                gb=GriddedTaxonomy(biome,cell,generate_tree_now=True,use_id_as_name=only_id)
            forest = taxonomy.forest

            ts = TreeStyle()
            ts.show_leaf_name = True
            ts.mode = "c"
            ts.arc_start = -180 # 0 degrees = 3 o'clock
            ts.arc_span = 360
            ts.show_scale = False
            try:
                #ipdb.set_trace()
                forest[taxonomic_level].render(file_,h=500, w=500, units="px",tree_style=ts)
                #drawer.exit_gui(1, 1)
                
                #logger.info(QtCore.QThreadPool)
                #del(forest[taxonomic_level])
            except:
                logger.error('Something went wrong with the image rendering')
                
                
            img_paths[taxonomic_level] = {'name': tax_keys[taxonomic_level],'path':filename,'richness':taxonomy.richness[rich_keys[taxonomic_level]]}
        else:
            img_paths[taxonomic_level] = {'name': tax_keys[taxonomic_level],'path':filename,'richness':taxonomy.richness[rich_keys[taxonomic_level]]}
        #del(forest)
    #
    
    
    #dic_richness = gb.taxonomies[0].richness
    det_complex = gb.taxonomies[0].vectorIntrinsic 
    template = get_template('base.html')

    submatrices = map(lambda i : mat_complex[0:i,0:i],range(1,len(mat_complex)))
    #ipdb.set_trace()
    import numpy as np
    tras = map(lambda mat : np.linalg.eigvals(mat),submatrices)
    #ipdb.set_trace()
    try:
        eigenv = np.linalg.eigvals(mat_complex).tolist()
        svd = np.linalg.svd(mat_complex)
        
    except:
        eigenv =[]
        svd = [[],[],[]]
    
    #ipdb.set_trace()  
    html = template.render(Context({'gid':gid,'taxonomic_level':taxonomic_level,'grid_level':grid_level,'image_path':sorted(img_paths.itervalues()),'complexity':mat_complex.tolist(),'vect_comp':det_complex,'eigenv':eigenv,'left_eig_vect':svd[0].tolist(),'svd':svd[1].tolist(),'right_eig_vect':svd[2].tolist()}))
    response.content=(html)
    #response.content=str(forest[taxonomic_level])
    response.status_code = 200
    
    return response







