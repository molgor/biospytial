# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0006_auto_20160108_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='_class',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='_order',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='basis_of_record',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='catalog_number',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='collection_code',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='family',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='genus',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='institution_code',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='kingdom',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='phylum',
            field=models.CharField(db_index=True, max_length=55, null=True, blank=True),
        ),
    ]
