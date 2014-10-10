# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0004_auto_20141005_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='country',
            field=models.CharField(db_index=True, max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='county',
            field=models.CharField(db_index=True, max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='dataset_id',
            field=models.CharField(db_index=True, max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='identified_by',
            field=models.CharField(db_index=True, max_length=70, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='locality',
            field=models.CharField(db_index=True, max_length=70, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='recorded_by',
            field=models.CharField(db_index=True, max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='scientific_name',
            field=models.CharField(db_index=True, max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='scientific_name_author',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='specific_epithet',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='state_province',
            field=models.CharField(db_index=True, max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_basis_of_record',
            field=models.CharField(db_index=True, max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_scientific_name',
            field=models.CharField(db_index=True, max_length=60, null=True, blank=True),
        ),
    ]
