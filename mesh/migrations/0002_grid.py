# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mesh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='grid',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column=b'gid')),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('cell', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
            options={
                'db_table': 'grid025mex',
                'managed': False,
            },
        ),
    ]
