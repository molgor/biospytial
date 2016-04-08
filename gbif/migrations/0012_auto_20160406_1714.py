# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0011_auto_20160406_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence_csv',
            name='date_identified',
            field=models.TextField(null=True, blank=True),
        ),
    ]
