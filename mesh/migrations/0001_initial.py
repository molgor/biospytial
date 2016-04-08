# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mesh',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'gid')),
                ('cell', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
            options={
                'db_table': 'mesh"."braz_grid2048a',
                'managed': False,
            },
        ),
    ]
