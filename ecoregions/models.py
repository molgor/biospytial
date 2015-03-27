# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models

class Ecoregion(models.Model):
    id = models.AutoField(primary_key=True, db_column="gid")
    area = models.FloatField()
    perimeter = models.FloatField()
    cov_ = models.FloatField()
    cov_id = models.FloatField()
    tipo_zona = models.CharField(max_length=20)
    num_zona = models.CharField(max_length=10)
    nomzonecol = models.CharField(max_length=100)
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

# Auto-generated `LayerMapping` dictionary for ecoregions model
#===============================================================================
# ecoregions_mapping = {
#     'area' : 'AREA',
#     'perimeter' : 'PERIMETER',
#     'cov_field' : 'COV_',
#     'cov_id' : 'COV_ID',
#     'tipo_zona' : 'TIPO_ZONA',
#     'num_zona' : 'NUM_ZONA',
#     'nomzonecol' : 'NOMZONECOL',
#     'geom' : 'MULTIPOLYGON',
# }
#===============================================================================

    class Meta:
        managed = False
        db_table = "mex_ecoregions"
        
        
    def __repr__(self):
        c = '<Ecoregion: instance %s :: %s >' %(self.id,self.nomzonecol.encode('latin-1'))
        return c
    
    
    def __str__(self):
        c = '<Ecoregion: instance %s :: %s >' %(self.id,self.nomzonecol.encode('latin-1'))
        return c