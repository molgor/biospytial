"""
This is just a crapy script for calculating taxonomies if the biosphere dataquery has been changed.

It takes a lot of time
"""




l9 = nt.levels[9]   
max_i = len(l9.taxonomies)    
for i,tax in enumerate(l9):
    name = tax.showId()
    if r.exists(name):
        tax.buildInnerTree(deep=True)
        tax.calculateIntrinsicComplexity()
        tax.cache(r,refresh=True)
        print('Calculating and caching taxonomy %s/%s'%(str(i),str(max_i)))
del(l9)
del(nt.levels[9])

l8 = nt.levels[8]    
max_i = len(l8.taxonomies)    
for i,tax in enumerate(l8):
    name = tax.showId()
    if r.exists(name):
        tax.buildInnerTree(deep=True)
        tax.calculateIntrinsicComplexity()
        tax.cache(r,refresh=True)
        print('Calculating and caching taxonomy %s/%s'%(str(i),str(max_i)))
del(l8)
del(nt.levels[8])

l7 = nt.levels[7]
max_i = len(l7.taxonomies)    
for i,tax in enumerate(l7):
    name = tax.showId()
    if r.exists(name):
        tax.buildInnerTree(deep=True)
        tax.calculateIntrinsicComplexity()
        tax.cache(r,refresh=True)
        print('Calculating and caching taxonomy %s/%s'%(str(i),str(max_i)))
del(l7)
del(nt.levels[7])

l6 = nt.levels[6]
max_i = len(l6.taxonomies)    
for i,tax in enumerate(l6):
    name = tax.showId()
    if r.exists(name):
        tax.buildInnerTree(deep=True)
        tax.calculateIntrinsicComplexity()
        tax.cache(r,refresh=True)
        print('Calculating and caching taxonomy %s/%s'%(str(i),str(max_i)))
del(l6)
del(nt.levels[6])

l5 = nt.levels[5]
max_i = len(l5.taxonomies)    
for i,tax in enumerate(l5):
    name = tax.showId()
    if r.exists(name):
        tax.buildInnerTree(deep=True)
        tax.calculateIntrinsicComplexity()
        tax.cache(r,refresh=True)
        print('Calculating and caching taxonomy %s/%s'%(str(i),str(max_i)))
del(l5)
del(nt.levels[5])

    
max_i = len(l4.taxonomies)    
for i,tax in enumerate(l4):
    name = tax.showId()
    tax.buildInnerTree(deep=True)
    tax.calculateIntrinsicComplexity()
    print('Calculating and caching taxonomy %s/%s'%(str(i),str(max_i)))
#del(l4)
#del(nt.levels[4]) 

l3 = nt.levels[3]
max_i = len(l3.taxonomies)    
for i,tax in enumerate(l3):
    name = tax.showId()
    tax.buildInnerTree(deep=True)
    tax.calculateIntrinsicComplexity()
    print('Calculating and caching taxonomy %s/%s'%(str(i),str(max_i)))
#del(l3)
#del(nt.levels[3]) 