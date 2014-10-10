# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0009_auto_20141006_0111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='occurrence',
            old_name='location',
            new_name='geom',
        ),
    ]
