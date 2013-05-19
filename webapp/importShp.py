#!/usr/bin/env python
import sys
from datetime import datetime
from django.core.management import setup_environ
from grazingDB import settings
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
import os
import logging
from optparse import OptionParser
import itertools
import re

from django.contrib.gis.gdal import DataSource, CoordTransform, SpatialReference, OGRGeometry
from django.contrib.gis.geos import *


def l_d(*parms):
    #logging.debug(' '.join(itertools.imap(repr,parms)))
    print (' '.join(itertools.imap(repr,parms)))


def load_shp_file(filename, agency, state=None, name_field='ALLOT_NAME', acres_field=None, 
    source=None):
    from allotments.models import Allotment

    l_d("Opening shapefile %s" % filename)
    inputShp = DataSource(filename)
    l_d("fields: %s" % inputShp[0].fields)

    if not acres_field:
        if "ACRES" in inputShp[0].fields:
            acres_field = "ACRES"
        elif "GIS_ACRES" in inputShp[0].fields:
            acres_field = "GIS_ACRES"

    create_count = 0
    update_count = 0
    for inputLayer in inputShp:
        print('Layer "%s": %i %ss' % (inputLayer.name, len(inputLayer), inputLayer.geom_type.name))
        ct = CoordTransform(inputLayer.srs, SpatialReference('WGS84'))

        for feature in inputLayer:
#            print feature
            geom = feature.geom
            geom.transform(ct)
            name = feature.get(name_field)

            multi_poly = None
            if geom.geom_type == 'MultiPolygon':
                multi_poly = geom
            else:
                geos_geom = GEOSGeometry(geom.wkb)
                multi_poly = MultiPolygon(geos_geom,)
            #print multi_poly.wkt
            
            #(new_allotment, created) = Allotment.objects.get_or_create(name=name, agency=agency, geometry=multi_poly.wkt)
            
            new_allotment = Allotment(name=name, agency=agency,)
            new_allotment.geometry = multi_poly.wkt
            if acres_field:
                acres = float(feature.get(acres_field))
                new_allotment.acres = acres
            new_allotment.state = state
            new_allotment.source = source

            create_count += 1
            new_allotment.save()
    print "created %i features, updated %i" % (create_count, update_count)


if __name__=='__main__':
    usage = "usage: %prog "
    parser = OptionParser(usage=usage,
        description="Load a shp file of grazing allotments")
    parser.add_option("-d", "--debug", action="store_true", dest="debug")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet")
    parser.add_option("-a", "--agency", action="store", type="string", dest="agency")
    parser.add_option("-n", "--name-field", action="store", type="string", dest="nameField",
     default='ALLOT_NAME')
    parser.add_option("-A", "--acres", action="store", type="string", dest="acresField")
    parser.add_option("-s", "--state", action="store", type="string", dest="state")
    parser.add_option("-S", "--source", action="store", type="string", dest="source")

    (options, args) = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if options.debug else 
        (logging.ERROR if options.quiet else logging.INFO))
    l_d(options)

    if not options.agency:
        print "agency is required(ex: -a BLM)"
        sys.exit()

    if not options.state:
        print "state is required(ex: -s AZ)"
        sys.exit()

    setup_environ(settings)

    for filename in args:
        source = options.source
        if not source:
            (dirName, lastComponent) = os.path.split(filename)
            if dirName:
                (parentDirName, dirName) = os.path.split(dirName)
                source = "%s/%s" % (dirName, lastComponent)
            else:
                source = lastComponent

        load_shp_file(filename, options.agency, name_field=options.nameField, 
            acres_field=options.acresField, state=options.state, source=source)
