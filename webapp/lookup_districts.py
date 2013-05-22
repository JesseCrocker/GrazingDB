#!/usr/bin/env python
import sys
from django.core.management import setup_environ
from grazingDB import settings
import os
import logging

setup_environ(settings)

from allotments.models import Allotment

for allotment in Allotment.objects.all():
    if allotment.field_office and len(allotment.field_office):
        continue

    district = allotment.lookup_district()
    print("%s in %s" % (allotment.name, district))
    if district:
        allotment.field_office=district
        allotment.save()
