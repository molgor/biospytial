# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0007_auto_20160112_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='_class',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='_order',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='basis_of_record',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='catalog_number',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='collection_code',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='country',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='country_code',
            field=models.TextField(db_index=True, max_length=7, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='county',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='dataset_id',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='family',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='genus',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='institution_code',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='kingdom',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='phylum',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='scientific_name',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='specific_epithet',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='state_province',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='_class',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='_order',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='basis_of_record',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='catalog_number',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='collection_code',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='country',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='country_code',
            field=models.TextField(db_index=True, max_length=7, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='county',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='dataset_id',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='family',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='genus',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='identified_by',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='institution_code',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='kingdom',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='locality',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='phylum',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='recorded_by',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='scientific_name',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='scientific_name_author',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='specific_epithet',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='state_province',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_basis_of_record',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_class',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_family',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_genus',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_infraspecific_epithet',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_kingdom',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_order',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_phylum',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_scientific_name',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_specific_epithet',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
    ]
