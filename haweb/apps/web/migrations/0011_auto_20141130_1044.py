# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20141119_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselinfo',
            name='picture',
            field=models.ImageField(help_text=b'Please, use this video https://www.youtube.com/watch?v=lMd6nQeryjs to crop the img to 1024x300 pixels', upload_to=b'photos'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.ImageField(help_text=b'Please, use this video https://www.youtube.com/watch?v=lMd6nQeryjs to crop the img to 140x140 pixels', upload_to=b'logos'),
        ),
    ]
