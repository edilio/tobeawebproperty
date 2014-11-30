# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20141130_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='cell_phone',
            field=localflavor.us.models.PhoneNumberField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='first_name',
            field=models.CharField(max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='home_phone',
            field=localflavor.us.models.PhoneNumberField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='last_name',
            field=models.CharField(max_length=50, db_index=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='tenant_id',
            field=models.CharField(db_index=True, max_length=7, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='tenant',
            name='work_phone',
            field=localflavor.us.models.PhoneNumberField(db_index=True, max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='address',
            field=models.CharField(max_length=100, db_index=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_id',
            field=models.CharField(db_index=True, max_length=7, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='zipcode',
            name='zip_code',
            field=models.CharField(max_length=10, db_index=True),
        ),
    ]
