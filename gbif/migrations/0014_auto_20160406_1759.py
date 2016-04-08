# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0013_auto_20160406_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence_csv',
            name='taxon_rank',
            field=models.TextField(null=True, blank=True),
        ),
    ]
