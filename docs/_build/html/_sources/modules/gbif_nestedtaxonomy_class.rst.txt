=============================
Taxonomies in the nested grid
=============================

A Nested Taxonomy is a hierarchical arrangement of Gridded Taxonomies,
each of this called ´level´. The arrangement is a list in ascending resolution
order. All levels have exactly the same geographic extent
and referencing system what makes them unique is the resolution.

The first level is composed by one grid cell. This level is often called parent.

The resolution increases to double when it changes from level to level.
Meaning that the first level

This is the definition of the class and its respective methods:

.. autoclass:: gbif.taxonomy.NestedTaxonomy
  :members:

Examples
========

This example shows how to define a NestedTaxonomy for a specific
area in South America.

Defining the area
-----------------

Using the QGIS support for visualizing the data it's possible to retrieve the Id
 value and the first zooming level (parent_level)
(See figure below:)

 .. image:: _static/nestedtaxonomy_parent_sel.png

The Id and zoom level for this region corresponds to:

* 'Id : 167   Zoom Level : 9'


To create an the Nested Taxonomy in this region for all the available zooming levels
use:

.. code-block:: python

   In [1]: from gbif.taxonomy import NestedTaxonomy

   In [2]: from gbif.models import Occurrence

   In [3]: biosphere = Occurrence.objects.all()

   In [4]: nt = NestedTaxonomy(167,biosphere,start_level=9,end_level=16,generate_tree_now=True)


The time spent in executing this analysis was:

* CPU times: user 41min 49s
* sys: 6min 15s, total: 48min 4s
* 'Wall time: 4h 38min 5s'

Therefore the need to use a caching method.

To store in cache the current Nested Taxonomy object use the cache method.

.. code-block:: python

  In[5]: import redis
  # Initialize redis connection (redis_wrapper)
  In[6]: r = redis.StrictRedis(host='localhost',db=0)
  # Store in the cache
  In[7]: nt.cache(r)
