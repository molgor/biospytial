# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0005_auto_20141005_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='scientific_name_author',
            field=models.CharField(db_index=True, max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='specific_epithet',
            field=models.CharField(db_index=True, max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='verbatim_basis_of_record',
            field=models.CharField(db_index=True, max_length=100, null=True, blank=True),
        ),
    ]
