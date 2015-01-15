# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import haweb.apps.web.models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20141130_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='lat',
            field=models.FloatField(default=25.8649876, help_text=b"latitude... put 0 if you don't know", blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='lng',
            field=models.FloatField(default=-80.26423799999999, help_text=b"longitude... put 0 if you don't know", blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='selected_theme',
            field=models.CharField(default=b'default', max_length=100, choices=[(b'default', b'Default'), (b'cerulean', b'Cerulean'), (b'cosmo', b'Cosmo'), (b'united', b'United')]),
        ),
        migrations.AlterField(
            model_name='resourcecategory',
            name='index',
            field=models.PositiveIntegerField(default=haweb.apps.web.models.next_resource_category_index),
        ),
    ]
