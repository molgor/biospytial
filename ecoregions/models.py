# This is an auto-generated Django model module created by ogrinspect.
from django.contrib.gis.db import models
from biospytial import settings

class Ecoregion(models.Model):
    id = models.AutoField(primary_key=True, db_column="gid")
    area = models.FloatField()
    perimeter = models.FloatField()
    cov = models.FloatField()
    covid = models.FloatField()
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
    
    
    
class InegiIV(models.Model):
    id = models.AutoField(primary_key=True, db_column="gid")
    covid = models.IntegerField(db_column="cov_id")
    cov = models.IntegerField(db_column="cov_")
    code = models.IntegerField(db_column="codigo")
    name = models.CharField(max_length=50,db_column="descripcio")
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = "landuse-inegi5"
        
        
    def __repr__(self):
        c = '<LandUse: instance %s :: %s >' %(self.id,self.name.encode('utf8'))
        return c
    
    
    def __str__(self):
        c = '<LandUse: instance %s :: %s >' %(self.id,self.name.encode('utf8'))
        return c
    

# This is an auto-generated Django model module created by ogrinspect.

class TerrEcoregions(models.Model):
    id = models.AutoField(primary_key=True, db_column="gid")
    eco_id_u = models.IntegerField()
    eco_code = models.CharField(max_length=16)
    eco_name = models.CharField(max_length=100)
    eco_num = models.IntegerField()
    ecode_name = models.CharField(max_length=120)
    cls_code = models.IntegerField()
    eco_notes = models.CharField(max_length=250)
    wwf_realm = models.CharField(max_length=2)
    wwf_realm2 = models.CharField(max_length=15)
    wwf_mhtnum = models.IntegerField()
    wwf_mhtnam = models.CharField(max_length=70)
    realmmht = models.CharField(max_length=4)
    er_update = models.CharField(max_length=15)
    er_date_u = models.CharField(max_length=12)
    er_ration = models.CharField(max_length=100)
    sourcedata = models.CharField(max_length=50)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        #managed = False
        db_table = settings.ECOREGIONS_DATATABLE

    def __repr__(self):
        c = '<Terr.Ecoregion: instance %s :: %s >' %(self.id,self.eco_name.encode('utf8'))
        return c
    
    
    def __str__(self):
        c = '<Terr.Ecoregion %s :: %s >' %(self.id,self.name.encode('utf8'))
        return c







