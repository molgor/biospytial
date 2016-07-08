# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0017_remove_occurrence_csv_verbatim_geom'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrence',
            name='id_gf',
        ),
        migrations.AlterModelTable(
            name='occurrence',
            table='gbif_occurrence_spatial',
        ),
    ]
