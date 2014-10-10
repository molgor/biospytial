# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0006_auto_20141005_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence',
            name='collection_code',
            field=models.CharField(db_index=True, max_length=15, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='institution_code',
            field=models.CharField(db_index=True, max_length=15, null=True, blank=True),
        ),
    ]
