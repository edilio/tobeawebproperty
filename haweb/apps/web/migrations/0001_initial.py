# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import haweb.apps.web.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField(default=haweb.apps.web.models.next_career_index)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['index'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CarouselInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'photos')),
                ('title', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField()),
                ('slug', models.SlugField(max_length=280, editable=False)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, blank=True)),
                ('modified_on', models.DateTimeField(null=True, editable=False, blank=True)),
                ('created_by', models.ForeignKey(related_name=b'created_content', editable=False, to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(related_name=b'modified_content', editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField(default=haweb.apps.web.models.next_faq_index)),
                ('question', models.CharField(max_length=250)),
                ('answer', models.TextField()),
            ],
            options={
                'ordering': ['index'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HelpfulLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField(default=haweb.apps.web.models.next_helpful_link_index)),
                ('title', models.CharField(max_length=250)),
                ('url', models.URLField()),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['index'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveSmallIntegerField(default=1)),
                ('name', models.CharField(max_length=50)),
                ('link', models.CharField(default=b'#', max_length=250)),
                ('parent', models.ForeignKey(related_name=b'children', blank=True, to='web.Menu', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2, choices=[(b'AK', b'Alaska'), (b'AL', b'Alabama'), (b'AR', b'Arkansas'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DC', b'District Of Columbia'), (b'DE', b'Delaware'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'IA', b'Iowa'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'MA', b'Massachusetts'), (b'MD', b'Maryland'), (b'ME', b'Maine'), (b'MH', b'Marshall Islands'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MO', b'Missouri'), (b'MP', b'Northern Mariana Islands'), (b'MS', b'Mississippi'), (b'MT', b'Montana'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'NE', b'Nebraska'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NV', b'Nevada'), (b'NY', b'New York'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'PW', b'Palau'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VA', b'Virginia'), (b'VI', b'US Virgin Islands'), (b'VT', b'Vermont'), (b'WA', b'Washington'), (b'WI', b'Wisconsin'), (b'WV', b'West Virginia'), (b'WY', b'Wyoming')])),
                ('zip', models.CharField(max_length=11)),
                ('logo', models.ImageField(upload_to=b'logos')),
                ('home_page', models.TextField()),
                ('five_year_plan', models.FileField(null=True, upload_to=b'', blank=True)),
                ('selected_theme', models.CharField(default=b'default', max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField(default=haweb.apps.web.models.next_career_index)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ['index'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceForm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField(default=haweb.apps.web.models.next_resource_index)),
                ('name', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('resource', models.FileField(upload_to=b'resources')),
                ('visible', models.BooleanField(default=True)),
                ('category', models.ForeignKey(to='web.ResourceCategory')),
            ],
            options={
                'ordering': ['index'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='carouselinfo',
            name='organization',
            field=models.ForeignKey(related_name=b'carousel', to='web.Organization'),
            preserve_default=True,
        ),
    ]
