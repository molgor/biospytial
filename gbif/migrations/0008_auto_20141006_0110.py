# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0007_auto_20141005_1917'),
    ]

    operations = [
        migrations.CreateModel(
            name='OccurrenceGeo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'id_gbif')),
                ('dataset_id', models.CharField(db_index=True, max_length=60, null=True, blank=True)),
                ('institution_code', models.CharField(db_index=True, max_length=15, null=True, blank=True)),
                ('collection_code', models.CharField(db_index=True, max_length=15, null=True, blank=True)),
                ('catalog_number', models.CharField(db_index=True, max_length=15, null=True, blank=True)),
                ('basis_of_record', models.CharField(db_index=True, max_length=15, null=True, blank=True)),
                ('scientific_name', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('scientific_name_author', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('taxon_id', models.IntegerField(null=True, blank=True)),
                ('kingdom', models.CharField(db_index=True, max_length=15, null=True, blank=True)),
                ('phylum', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('_class', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('_order', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('family', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('genus', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('specific_epithet', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('kingdom_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('phylum_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('class_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('order_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('family_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('genus_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('species_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('country_code', models.CharField(db_index=True, max_length=7, null=True, blank=True)),
                ('latitude', models.FloatField(db_index=True, null=True, blank=True)),
                ('longitude', models.FloatField(db_index=True, null=True, blank=True)),
                ('year', models.IntegerField(db_index=True, null=True, blank=True)),
                ('month', models.IntegerField(db_index=True, null=True, blank=True)),
                ('event_date', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('elevation_in_meters', models.FloatField(db_index=True, null=True, blank=True)),
                ('depth_in_meters', models.FloatField(db_index=True, null=True, blank=True)),
                ('verbatim_scientific_name', models.CharField(db_index=True, max_length=60, null=True, blank=True)),
                ('taxon_rank', models.IntegerField(db_index=True, null=True, blank=True)),
                ('verbatim_kingdom', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_phylum', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_class', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_order', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_family', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_genus', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_specific_epithet', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_infraspecific_epithet', models.CharField(db_index=True, max_length=25, null=True, blank=True)),
                ('verbatim_latitude', models.FloatField(db_index=True, null=True, blank=True)),
                ('verbatim_longitude', models.FloatField(db_index=True, null=True, blank=True)),
                ('coordinate_precision', models.FloatField(db_index=True, null=True, blank=True)),
                ('maximum_elevation_in_meters', models.FloatField(db_index=True, null=True, blank=True)),
                ('minimum_elevation_in_meters', models.FloatField(db_index=True, null=True, blank=True)),
                ('elevation_precision', models.FloatField(db_index=True, null=True, blank=True)),
                ('minimum_depth_in_meters', models.FloatField(db_index=True, null=True, blank=True)),
                ('maximum_depth_in_meters', models.FloatField(db_index=True, null=True, blank=True)),
                ('depth_precision', models.FloatField(db_index=True, null=True, blank=True)),
                ('continent_ocean', models.FloatField(db_index=True, null=True, blank=True)),
                ('state_province', models.CharField(db_index=True, max_length=60, null=True, blank=True)),
                ('county', models.CharField(db_index=True, max_length=60, null=True, blank=True)),
                ('country', models.CharField(db_index=True, max_length=60, null=True, blank=True)),
                ('recorded_by', models.CharField(db_index=True, max_length=60, null=True, blank=True)),
                ('locality', models.CharField(db_index=True, max_length=70, null=True, blank=True)),
                ('verbatim_year', models.IntegerField(db_index=True, null=True, blank=True)),
                ('verbatim_month', models.IntegerField(db_index=True, null=True, blank=True)),
                ('day', models.IntegerField(db_index=True, null=True, blank=True)),
                ('verbatim_basis_of_record', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('identified_by', models.CharField(db_index=True, max_length=70, null=True, blank=True)),
                ('date_identified', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('created', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('modified', models.DateTimeField(db_index=True, null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Occurrence',
        ),
    ]
