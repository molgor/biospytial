# Just for fun
# Produce jpg images of several months taking raster data

## Load country border
# Load data from a Country polygon 
from sketches.models import Country

mexico_border = Country.objects.filter(name__contains='exico').get()
uk_border = Country.objects.filter(name__contains='United Kingdom').get()

polygon_mex = mexico_border.geom
polygon_uk = uk_border = uk_border.geom


import matplotlib.pyplot as plt
from raster_api.tools import RasterData
from raster_api.models import raster_models

mexprec = RasterData(raster_models[1],polygon_mex)

ukprec = RasterData(raster_models[1],polygon_uk)

mexprec.getRaster()
ukprec.getRaster()


mex_stats_dict = mexprec.rasterdata.allBandStatistics()
uk_stats_dict = ukprec.rasterdata.allBandStatistics()




meses = {'01':'Enero','02':'Febrero','03':'Marzo','04':'Abril','05':'Mayo','06':'Junio','07':'Julio','08':'Agosto','09':'Septiembre','10':'Octubre','11':'Noviembre','12':'Diciembre'}
#mex.exportToJPG('0'+name,s,title=month,band=int(name),cmap=plt.cm.inferno)

cmap = plt.cm.PuBu
