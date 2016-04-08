# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='taxon_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
