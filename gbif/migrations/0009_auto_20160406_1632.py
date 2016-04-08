# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0008_auto_20160406_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence_csv',
            name='continent_ocean',
            field=models.TextField(db_index=True, null=True, blank=True),
        ),
    ]
