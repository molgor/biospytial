
# coding: utf-8

# This Demo shows how to work with different Trees loaded from the Graph Database. 

# In[93]:

get_ipython().magic(u'matplotlib inline')
import sys
sys.path.append('/apps')
import django
django.setup()


# ## Import biospytial modules

# In[94]:

from drivers.tree_builder import TreeNeo
from drivers.graph_models import graph, Mex4km_
from mesh.models import MexMesh
from gbif.taxonomy import Occurrence, Taxonomy, GriddedTaxonomy
from drivers.graph_models import Cell
from drivers.tree_builder import extractOccurrencesFromTaxonomies


# ### How to work with custom polygons ?

# In[95]:

from django.contrib.gis.geos import GEOSGeometry
polystr = "POLYGON((-109 27,-106 27,-106 30,-109 30,-109 27))"
polygon = GEOSGeometry(polystr)


# ### Load mesh class

# In[96]:

mexgrid = MexMesh.objects.filter(cell__intersects=polygon)


# ### Instantiate the biosphere

# In[97]:

biosphere = Occurrence.objects.all()


# ### Filter by geometry

# In[98]:

subbiosphere = biosphere.filter(geom__intersects=polygon)


# ### Instantiate Gridded Taxonomy

# In[99]:

ggg = GriddedTaxonomy(subbiosphere,mexgrid.filter(cell__intersects=polystr),'mex4km',generate_tree_now=False,use_id_as_name=False)


# ### Load some trees
# If we load all of them it will take a lot of time (31 mins (in local machine)).

# In[100]:

taxonomies = ggg.taxonomies[0:200]


# ### Let's load the data from the graphdb

# In[101]:

trees = map(lambda t : t.loadFromGraphDB(),taxonomies)


# ### Sort it, ... ;)

# In[102]:

trees.sort(key=lambda l : l.richness, reverse=True)


# In[103]:

trees[0].richness


# ### Ok, let's explore this *super* node

# In[104]:

st = trees[0]


# ### mmhh... vertebrates ? 

# In[105]:

st.to_Animalia.to_Chordata


# ### Let birds be :

# In[106]:

birds = st.to_Animalia.to_Chordata.to_Aves


# In[107]:

birds.richness


# ### Give me environmental conditions

# In[108]:

environment = birds.associatedData.getEnvironmentalVariablesPoints()


# In[109]:

environment


# ## Explore the neighbours

# In[110]:

ns = birds.getNeighboringTrees()


# In[111]:

ns


# In[112]:

ns.getCooccurrenceMatrix(taxonomic_level=3)


# ### Expand the neighbourhood to size 3

# In[113]:

ns.expandNeighbourhood(4)


# In[114]:

big_tree = ns.extendedTree


# In[115]:

big_tree


# In[116]:

ns.getCooccurrenceMatrix(taxonomic_level=3)


# In[117]:

big_tree.getExactCells()

raster = big_tree.associatedData.getAssociatedRasterAreaData?
# In[118]:

raster = big_tree.associatedData.getAssociatedRasterAreaData('SolarRadiation')


# In[119]:

raster.display_field(band=6)


# In[120]:

neighbours = ns.neighbours


# ### Which neighbours have birds ?

# In[138]:

map(lambda neighbour : neighbour.hasNode(birds) , neighbours)


# ### Filter the neighbours that have birds! 

# In[139]:

birds


# In[136]:

filter(lambda neighbour : neighbour.hasNode(birds), neighbours)

