# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0018_auto_20160623_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='occurrence_csv_verbatim',
            name='popo',
            field=models.TextField(null=True, blank=True),
        ),
    ]
