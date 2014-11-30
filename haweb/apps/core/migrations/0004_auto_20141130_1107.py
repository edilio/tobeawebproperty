# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20141130_1044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AddField(
            model_name='tenant',
            name='cell_phone',
            field=localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenant',
            name='home_phone',
            field=localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tenant',
            name='work_phone',
            field=localflavor.us.models.PhoneNumberField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='zipcode',
            name='zip_code',
            field=models.CharField(max_length=10),
        ),
    ]
