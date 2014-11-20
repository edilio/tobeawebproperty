# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_insert_default_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='lat',
            field=models.FloatField(default=25.8649876),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='organization',
            name='lng',
            field=models.FloatField(default=-80.26423799999999),
            preserve_default=True,
        ),
    ]
