# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20141115_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='slug',
            field=models.SlugField(default=b'', max_length=280, editable=False),
            preserve_default=True,
        ),
    ]
