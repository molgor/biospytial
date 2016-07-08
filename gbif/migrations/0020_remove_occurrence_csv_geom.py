# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0019_occurrence_csv_verbatim_popo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrence_csv',
            name='geom',
        ),
    ]
