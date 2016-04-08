# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0002_occurrence_taxon_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrence',
            name='taxon_id',
        ),
    ]
