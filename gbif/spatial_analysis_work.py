from gbif.taxonomy import NestedTaxonomy
from gbif.models import Occurrence
from ecoregions.models import Ecoregion
from django.contrib.gis.db.models import Union, Min

biosphere = Occurrence.objects.all()
#WOuld be good to put some temporal filtering here
nt = NestedTaxonomy(36,biosphere,start_level=3,end_level=9,generate_tree_now=False)

print nt.levels

study_area = nt.parent.biomeGeometry

ecoregions = Ecoregion.objects.all()
ecoregions_in_area = ecoregions.filter(geom__within=study_area)

zonenumbers = list(set(map(lambda e : e.num_zona,ecoregions_in_area)))

z_numbers = filter(lambda x : x != None,zonenumbers)

regions_dic = {}
for i in z_numbers:
    #regions_dic[int(i)]=ecoregions_in_area.filter(num_zona=int(i)).aggregate(polygon=Union('geom'),name=Min('nomzonecol'.encode('latin-1')),zone_id=Min('num_zona'))
    regions_dic[int(i)]=ecoregions_in_area.filter(num_zona=int(i))
    #.aggregate(polygon=Union('geom'),name=Min('nomzonecol'.encode('latin-1')),zone_id=Min('num_zona'))
    
    
regions_polys = {}
for i in z_numbers:
    #regions_dic[int(i)]=ecoregions_in_area.filter(num_zona=int(i)).aggregate(polygon=Union('geom'),name=Min('nomzonecol'.encode('latin-1')),zone_id=Min('num_zona'))
    regions_polys[int(i)]=map(lambda p : p.geom , ecoregions_in_area.filter(num_zona=int(i)))
    #.aggregate(polygon=Union('geom'),name=Min('nomzonecol'.encode('latin-1')),zone_id=Min('num_zona'))
   
    
#map(lambda l_t : map(lambda t : t.calculateIntrinsicComplexity(),l_t),tropic_tax)

taxonomies_per_ecoregion = {}
for i in z_numbers:
    tax_list = []
    for poly in regions_polys[int(i)]:
        tax_list.append(map(lambda t : t.biomeGeometry.intersects(poly),l9.taxonomies))
    taxonomies_per_ecoregion[i] = tax_list
    

l9 = nt.levels[9]
l9.restoreTaxonomiesFromCache(r)

#SELECT ONE ECOREGION CLASS JUT POLYGONS
#trop_pol  = map(lambda r : r.geom , regions_dic[1])

#LET POLY BE A POLYGON OF IT TROP_POL
#poly = trop_pol[0]
#Filter taxonomies living here
#taxonomies_within_tropic = map(lambda t : t.biomeGeometry.intersects(poly),l9.taxonomies)




