# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def insert_default_user_groups(apps, schema_editor):
    """
    Auth app is loaded at this point, guessing n error in django
    for now moving the code to admin to continue dev
    """
    pass
    # print apps.app_configs.keys()
    # Group = apps.get_model('auth', 'Group')
    # Group.objects.create(name='Displayable Users')
    # Group.objects.create(name='Commissioners')


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_insert_default_category_forms_'),
    ]

    operations = [
        migrations.RunPython(insert_default_user_groups)
    ]
