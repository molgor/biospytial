# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0005_occurrence_collection_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='id_gf',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
