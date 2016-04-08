# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0016_occurrence_csv_verbatim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrence_csv_verbatim',
            name='geom',
        ),
    ]
