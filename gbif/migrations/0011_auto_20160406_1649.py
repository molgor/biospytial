# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0010_auto_20160406_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence_csv',
            name='basis_of_record',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='catalog_number',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='collection_code',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='continent_ocean',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='coordinate_precision',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='country',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='country_code',
            field=models.TextField(max_length=7, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='county',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='dataset_id',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='date_identified',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='day',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='depth_in_meters',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='depth_precision',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='elevation_in_meters',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='elevation_precision',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='identified_by',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='institution_code',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='locality',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='maximum_depth_in_meters',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='maximum_elevation_in_meters',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='minimum_depth_in_meters',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='minimum_elevation_in_meters',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='modified',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='recorded_by',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='scientific_name_author',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='state_province',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='taxon_rank',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_basis_of_record',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_class',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_family',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_genus',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_infraspecific_epithet',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_kingdom',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_latitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_longitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_month',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_order',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_phylum',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_scientific_name',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_specific_epithet',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_year',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
