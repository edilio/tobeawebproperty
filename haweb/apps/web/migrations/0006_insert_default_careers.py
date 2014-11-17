# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.template.defaultfilters import slugify


def insert_career(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Career = apps.get_model("web", "Career")
    careers = [
        {
            "index": 1,
            "title": "Plumbing Specialist",
            "description": "<p>Performs a variety of skilled plumbing maintenance work at DHA sites. Work involves repair and replacement of items such as toilets, faucets, water heaters, water lines, sewer lines, and preventive maintenance on plumbing components. Provides consultation throughout DHA to maintenance personnel involved in plumbing maintenance. Working conditions include inadequate lighting, restricted movement, dirty environment, air contamination, extreme temperatures, intense noise, hazardous materials, or lifting or carrying heavy objects. Graduation from high school or GED equivalent, North Carolina Licensed Plumber, and at least 5 years of plumbing experience or an equivalent combination of training and experience.</p>\r\n<p><br /> DHA offers a competitive benefits package to include retirement, 457(b), life, annual/sick leave, medical and dental care (nominal monthly employee payment) with subsidized dependent coverage.<br /> All applicants must be able to pass pre-employment drug screening and criminal background checks and possess a driver&rsquo;s license valid in the state of North Carolina.</p>"
        },
        {
            "index": 2,
            "title": "Property Manager",
            "description": "<p>The Property Manager has broad responsibility for managing all aspects of one or more housing site. Responsibilities include managing the daily operations, property management, vacancy reduction, leasing, lease enforcement, resident problem resolution, property appearance, maintenance, modernization, purchasing, budget responsibility, and supervising other staff members.</p>\r\n<p>Job Responsibilities:</p>\r\n<p>&bull; Leases and shows units to ensure properties are fully occupied<br />&bull; Monitors lease compliance by way of inspection, follow-up on receivables, holding/participating in hearings, resolving resident complaints, etc.<br />&bull; Conducts thorough inspections including, move-in, 90-day, move-out, housekeeping, HUD required, etc.<br />&bull; Issues eviction notices and testifies in housing court<br />&bull; Manages all maintenance functions ensuring work orders are completed timely and satisfactorily<br />&bull; Supervises maintenance and clerical staff<br />&bull; Walks and inspects grounds<br />&bull; Prepares annual budget, continually analyzing financials to monitor costs and meet budget objectives<br />&bull; Purchases goods and services for properties following establish procurement policy<br />&bull; Shows professionalism and courtesy to internal and external customers and manages communication within the agency<br />&bull; Ensures staff are trained and follow safe work practices<br />&bull; Coordinates with other departments and community resources for services to residents<br />&bull; Completes HUD and LMHA reports<br />&bull; Ensures LMHA Action Plan goals and objectives are met or exceeded<br />&bull; Other duties as assigned</p>\r\n<p>Requirements:</p>\r\n<p>&bull; Bachelor&rsquo;s degree in business administration, public administration, the behavioral sciences, or other related field<br />&bull; Minimum of 3 years of work experience in private or public housing or equivalent <br />&bull; Minimum of 1 year of supervisory experience<br />&bull; Computer literacy including word processing and spreadsheets<br />&bull; Valid Ohio or Michigan driver&rsquo;s license and insurable status <br />&bull; Effective verbal and written communication skills<br />&bull; Experience working with diverse populations<br />&bull; Excellent customer service skills<br />This is a Section 3 covered position and HUD recipients are encouraged to apply.<br />Please note on your submittal if you are a LMHA Public Housing or Section 8 resident.</p>\r\n<p>Persons with disabilities are encouraged to apply.</p>\r\n<p>EMPLOYMENT APPLICATION MUST BE COMPLETED ONLINE AT</p>\r\n<p>http://lucasmha.org/Employment/tabid/690/Default.aspx</p>\r\n<p>SUBMITALS ARE NOT RECEIVED AT ANY OF OUR OFFICES, VIA FAX, OR EMAIL.</p>\r\n<p>Phone calls regarding this or any other position are not accepted.</p>\r\n<p>This job posting will be removed from the website at 11:59 p.m. on <br />Friday, November 28, 2014.</p>\r\n<p>TO COMPLETE OUR ONLINE APPLICATION:<br />&bull; Click on the &ldquo;APPLY NOW&rdquo; button at the bottom of this page.<br />&bull; If currently employed, use the current date for &ldquo;DATE JOB ENDED&rdquo; for &ldquo;EMPLOYER #1.&rdquo;<br />&bull; Ensure all &ldquo;REQUIRED FIELDS&rdquo; are completed.<br />&bull; Attachments are NOT accepted; any applicable experience MUST BE detailed in the online application.</p>"
        }
    ]
    for obj in careers:
        Career.objects.create(index=obj['index'],
                              title=obj['title'],
                              description=obj['description'])


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_insert_default_faqs'),
    ]

    operations = [
        migrations.RunPython(insert_career),
    ]
