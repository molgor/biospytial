
from gbif.taxonomy import NestedTaxonomy,remap,summaryDataFrame

from gbif.models import Occurrence

import pandas as pn
biosphere = Occurrence.objects.all()

import redis


#===============================================================================
# def remap(sorted_list_duple):
#     previous_value = sorted_list_duple[0][1]
#     j = 0
#     new = []
#     for indx,current_value in sorted_list_duple:
#         if current_value != previous_value:
#             new.append((indx,j))
#             j += 1
#             previous_value = current_value
#         else:
#             new.append((indx,j))
#     return new 
#     
# def summaryDataFrame(summary):
#     
#     fam = map(lambda id,fam : (id,fam) , summary['gid'],summary['fam'])
#     sp = map(lambda id,fam : (id,fam) , summary['gid'],summary['sp'])
#     cls =map(lambda id,fam : (id,fam) , summary['gid'],summary['cls'])
#     ord = map(lambda id,fam : (id,fam) , summary['gid'],summary['ord'])
#     kng = map(lambda id,fam : (id,fam) , summary['gid'],summary['kng'])
#     gns = map(lambda id,fam : (id,fam) , summary['gid'],summary['gns'])
#     phy = map(lambda id,fam : (id,fam) , summary['gid'],summary['phy'])
# 
#     #Sort by integer representation
#     j= map(lambda x : x.sort(key=lambda y : y[1]),[fam,sp,cls,ord,kng,gns,phy])
#     
#     # Apply re-classification
#     sp = remap(sp)
#     gns = remap(gns)
#     fam = remap(fam)
#     ord = remap(ord)
#     cls = remap(cls)
#     phy = remap(phy)
#     kng = remap(kng)
#     
#     #Sort by GID
#     j= map(lambda x : x.sort(key=lambda y : y[0]),[fam,sp,cls,ord,kng,gns,phy])
#     
#     # Retrieve the gid.
#     #Need to check if it's the same value for each.
#     gid = map(lambda x : x[0] , fam)
#     #Take away first component
#     d = {'gid':gid, 'sp' : sp, 'gns' : gns, 'fam' : fam, 'ord' : ord,'cls': cls, 'phy' : phy , 'kng' : kng }    
#     for key in ['fam','sp','cls','ord','kng','gns','phy']:
#         tax = d[key]
#         l = []
#         for i,value in enumerate(tax):
#             if gid[i] == value[0]:
#                
#                 t = value[1]
# 
#                 l.append(t)
#             else:
#                 raise Exception('Error in the summary data. GID not the same for rows')
#         d[key] = l
#     return d
#===============================================================================
       

nt = NestedTaxonomy(10417,biosphere,start_level=12,end_level=16,generate_tree_now=False)

r = redis.StrictRedis()

nt.loadFromCache(r)


nt.setPresenceInLevels()
summary_16 = nt.levels[16].summary(attr='int')


s = pn.DataFrame(summary_16,dtype=object)

s16 = summaryDataFrame(summary_16)
s = pn.DataFrame(s16)

