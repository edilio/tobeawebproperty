# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_tenant_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='move_out_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
