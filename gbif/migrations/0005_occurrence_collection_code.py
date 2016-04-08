# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0004_auto_20160108_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence',
            name='collection_code',
            field=models.CharField(db_index=True, max_length=25, null=True, blank=True),
        ),
    ]
