# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Allotment.source'
        db.add_column(u'allotments_allotment', 'source',
                      self.gf('django.db.models.fields.CharField')(default='old', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Allotment.source'
        db.delete_column(u'allotments_allotment', 'source')


    models = {
        u'allotments.allotment': {
            'Meta': {'object_name': 'Allotment'},
            'acres': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['allotments']