# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0003_remove_occurrence_taxon_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='basis_of_record',
            field=models.CharField(db_index=True, max_length=35, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='catalog_number',
            field=models.CharField(db_index=True, max_length=35, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='kingdom',
            field=models.CharField(db_index=True, max_length=35, null=True, blank=True),
        ),
    ]
