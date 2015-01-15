# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20141130_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='email',
            field=models.EmailField(max_length=75, null=True),
            preserve_default=True,
        ),
    ]
