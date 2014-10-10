# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='_class',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='_order',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='basis_of_record',
            field=models.CharField(max_length=15, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='catalog_number',
            field=models.CharField(max_length=15, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='class_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='collection_code',
            field=models.CharField(max_length=10, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='continent_ocean',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='coordinate_precision',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='country',
            field=models.CharField(max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='country_code',
            field=models.CharField(max_length=7, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='county',
            field=models.CharField(max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='created',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='dataset_id',
            field=models.CharField(max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='date_identified',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='day',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='depth_in_meters',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='depth_precision',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='elevation_in_meters',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='elevation_precision',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='event_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='family',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='family_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='genus',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='genus_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='identified_by',
            field=models.CharField(max_length=45, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='institution_code',
            field=models.CharField(max_length=10, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='kingdom',
            field=models.CharField(max_length=15, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='kingdom_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='latitude',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='locality',
            field=models.CharField(max_length=45, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='longitude',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='maximum_depth_in_meters',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='maximum_elevation_in_meters',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='minimum_depth_in_meters',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='minimum_elevation_in_meters',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='modified',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='month',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='order_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='phylum',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='phylum_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='recorded_by',
            field=models.CharField(max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='scientific_name',
            field=models.CharField(max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='scientific_name_author',
            field=models.CharField(max_length=35, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='species_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='specific_epithet',
            field=models.CharField(max_length=35, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='state_province',
            field=models.CharField(max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='taxon_rank',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_basis_of_record',
            field=models.CharField(max_length=35, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_class',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_family',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_genus',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_infraspecific_epithet',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_kingdom',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_latitude',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_longitude',
            field=models.FloatField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_month',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_order',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_phylum',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_scientific_name',
            field=models.CharField(max_length=40, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_specific_epithet',
            field=models.CharField(max_length=25, db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_year',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='year',
            field=models.IntegerField(db_index=True),
        ),
    ]
