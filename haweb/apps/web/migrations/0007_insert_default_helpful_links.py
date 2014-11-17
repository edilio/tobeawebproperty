# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def insert_links(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Link = apps.get_model("web", "HelpfulLink")
    text = """\
Alachua County Coalition for the Homeless and Hungry:
http://www.acchh.org/

Alachua County Housing Programs Division:
http://growth-management.alachua.fl.us/housing/housing_index.php

Alachua County School Board:
http://sbac.edu/

Alachua County State Housing Initiative Partnership (S.H.I.P.):
http://growth-management.alachua.fl.us/housing/ship.php

FL Housing Authorities:
http://www.hud.gov/offices/pih/pha/contacts/states/fl.cfm

Gainesville Housing Authority:
http://www.gainesvillehousingauthority.org/

Gainesville Regional Utilities:
http://www.gru.com/

Housing Discrimination Complaints:
http://www.hud.gov/complaints/housediscrim.cfm

Meridian Behavioral Healthcare, Inc.
http://www.mbhci.org/

National Association of Housing and Redevelopment Officials (NAHRO):
http://nahro.org/index.cfm

Privately Owned Subsidized Housing assistance in your area rental search:
http://www.hud.gov/apps/section8/index.cfm

To find out information about renting and HUD assistance rental programs:
http://www.hud.gov/renting/index.cfm

To find out information about GRACE Project:
http://www.alachuahomeless.com"""
    lst = text.splitlines()
    index = 0
    for i in range(len(lst)/3):
        index += 1
        title = lst[i*3]
        url = lst[i*3+1]
        description = title
        Link.objects.create(index=index,
                            title=title,
                            url=url,
                            description=description)

class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_insert_default_careers'),
    ]

    operations = [
        migrations.RunPython(insert_links),
    ]
