# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0014_auto_20160406_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_latitude',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_longitude',
            field=models.TextField(null=True, blank=True),
        ),
    ]
