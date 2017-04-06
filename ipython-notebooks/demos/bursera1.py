
# coding: utf-8

# # Burseras and Friends
# ## How´s the environment ?
# ## Which are their friends ? 

# In this example we will explore how to query and select a Node (Bursera, Node Type : Family) in the Tree Of Life.
# We will extract the associated Cells and explore which kind of other taxa share that space. 
# Let´s start!

# ![Burcera Environment](http://www.geographylists.com/mex_pv_forest.jpg "Bursera and its environment")
# 

# ### Import modules libraries and load ploting style

# In[33]:


from drivers.tree_builder import TreeNeo
from drivers.graph_models import TreeNode, Order, Family, graph


# ### Select the Node Bursera

# Bursera is a Family of Plants. We want to select a Node in the Tree Of Life that is of the type Family and the name starts 
# with "Burser". The expression "_.name=~STRING" means that we will look into the attribute "name" using a regular expression 
# "=~" followed by any number of characters ".*"

# In[34]:

bursera = list(Family.select(graph).where("_.name=~'Burser.*'")).pop()


# The result is a list. Given that there is only one Node of the type Family that has the name "Burser" we can extract
# the only element of the list using the standard method pop().


# In[39]:

cells_with_burseras = bursera.cells


# The result is a generator object. This is helpfull when the number of cells is big and surpasses the capacity of the machine
# or the analyst.

# In[40]:

cells_with_burseras


# In this example we want to get only the first 10 cells.

# In[41]:

cells_with_burseras = list(cells_with_burseras)


# In[74]:




# ## *Oke Oke*!, 
# Now we want to get the subtrees of Life constrainted by the geographical attribute of this cells.
# For doing this, simply get the occurrences within each cell with the method *occurrencesHere()* and use this output as the constructor argument.

# In[42]:


import numpy.random as rnd


# In[45]:

n = 10


# In[46]:

indices = rnd.randint(0,len(cells_with_burseras),n)


# In[47]:

selected_cells = [ cells_with_burseras[i] for i in indices ]


# ### Get the subtrees within the selected cells

# Let's create first a Constructor function

# In[48]:

ToTree = lambda cell : TreeNeo(cell.occurrencesHere())


# and map it to the selected cells

# In[49]:

trees = map(ToTree,selected_cells)


# #### Uff! it took 3 minutes, but it's a lot of data



# #### Get the UNION of the these 100 trees~

# In[51]:

big_tree = reduce(lambda a,b : a + b , trees)
t = big_tree

# In[52]:



