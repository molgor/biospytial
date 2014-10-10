# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0002_auto_20141003_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occurrence',
            name='id_gbif',
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, db_column=b'id_gbif'),
        ),
    ]
