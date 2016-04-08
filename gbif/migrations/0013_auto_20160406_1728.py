# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gbif', '0012_auto_20160406_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='occurrence_csv',
            name='created',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='modified',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_month',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='occurrence_csv',
            name='verbatim_year',
            field=models.TextField(null=True, blank=True),
        ),
    ]
