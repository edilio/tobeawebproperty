#!/usr/bin/env python
import os
import sys

#
APP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))

APP_DIR = APP_DIR.replace('bin', 'concernsprj')
print APP_DIR
sys.path.append(APP_DIR)
sys.path.append(os.path.dirname(APP_DIR))
#

import dotenv

dotenv.read_dotenv(os.path.join(APP_DIR, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'concernsprj.settings')

import pymysql
pymysql.install_as_MySQLdb()

import django
django.setup()

import problemusprj
print dir(problemusprj)

from problemus.models import ProblemVote
from problemus.serializers import ProblemVoteSerializer


def recover_votes(votes):
    for vote in votes:
        serializer = ProblemVoteSerializer(data=vote['fields'])
        print serializer.is_valid()
        print serializer.save(force_insert=False)
    print "worked!!!"

f = open('votes.txt')
txt = f.read()
f.close()
import json
txt = json.loads(txt)
ProblemVote.objects.all().delete()
recover_votes(txt)
