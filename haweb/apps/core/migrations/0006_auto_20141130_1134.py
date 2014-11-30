# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20141130_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=localflavor.us.models.PhoneNumberField(default=b'', max_length=20),
        ),
    ]
