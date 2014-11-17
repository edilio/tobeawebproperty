# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.template.defaultfilters import slugify


def insert_faqs(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    FAQ = apps.get_model("web", "FAQ")
    faqs = [
        {
            "index": 1,
            "question": "I've just submitted my application, how long will I have to wait for housing?",
            "answer": "There is not a simple answer to this question because an applicant's wait will depend upon the date and time you submitted the application and how many others are ahead of you. In most cases, it takes several weeks.\r\n",
        },
        {
            "index": 2,
            "question": "Where am I on the waiting list?",
            "answer": "You may call 256-329-2201 and our secretary will be happy to refer you to the proper person. They should be able to assist you with this information. The Authority may not be able to give you an exact time frame on when you will receive housing based on where you are on the waiting list.\r\n",
        },
        {
            "index": 3,
            "question": "Do I have to be a resident of Alexander City to be assisted?",
            "answer": "No",
        },
        {
            "index": 4,
            "question": "I am a person with disabilities, will I get housing more quickly?",
            "answer": "Yes. Persons with disabilities rank higher on the admission list. But you have to meet Social Security's definition of a disability. Please contact the Authority office at 256-329-2201 for more information.",
        },
        {
            "index": 5,
            "question": "Do you have emergency housing or emergency assistance?",
            "answer": "No. There are no provisions in our policies that allow someone with an emergency to move in before someone else. You must be determined eligible first and then you will be housed in accordance with the date and time of your application. Please contact the Authority office at 256-329-2201 for more information.",
        },
        {
            "index": 6,
            "question": "How old must I be to be eligible to live in senior housing?",
            "answer": "You must be 62 years of age or older, disabled or handicapped according to Social Security standards.",
        },
        {
            "index": 7,
            "question": "I have a landlord who is willing to rent to me under the Housing Choice Voucher Program (formally known as Section 8), can I get a Voucher immediately?",
            "answer": "No. You must apply for housing assistance first and be determined eligible. Then you will be placed on the list according to the date and time of application.",
        },
        {
            "index": 8,
            "question": "I am homeless, can you help me immediately?",
            "answer": "Unfortunately, no. Please refer to Question 5.",
        },
        {
            "index": 9,
            "question": "My family is soon to be evicted, how can you help?",
            "answer": "Please refer to Question 5.",
        },
        {
            "index": 10,
            "question": "What is the difference between Public Housing and the Housing Choice Voucher Program?",
            "answer": "Public Housing is owned by the Housing Authority and the Authority manages the property it leases. The ACHA owns and manages apartments in Alexander City, Alabama which are leased to low-income people on an income-based rental rate or at a flat rental rate depending on what the resident chooses.",
        },
        {
            "index": 11,
            "question": "I have applied for the Housing Choice Voucher Program, can I apply for Public Housing too?",
            "answer": "Yes you may. You will need to fill out an application for Public Housing and will be placed on the waiting list at the Authority.",
        }
    ]
    for q in faqs:
        FAQ.objects.create(index=q['index'],
                           question=q['question'],
                           answer=q['answer'],
                           slug=slugify(q['question']))



class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20141116_1149'),
    ]

    operations = [
        migrations.RunPython(insert_faqs),
    ]
