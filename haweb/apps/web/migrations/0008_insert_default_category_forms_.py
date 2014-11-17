# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def insert_category_form(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    ResourceCategory = apps.get_model("web", "ResourceCategory")
    if not ResourceCategory.objects.exists():
        ResourceCategory.objects.create(index=1, name='Forms')


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_insert_default_helpful_links'),
    ]

    operations = [
        migrations.RunPython(insert_category_form),
    ]
