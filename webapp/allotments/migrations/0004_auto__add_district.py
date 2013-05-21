# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'District'
        db.create_table(u'allotments_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('agency', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent_unit', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(blank=True, null=True, geography=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'allotments', ['District'])


    def backwards(self, orm):
        # Deleting model 'District'
        db.delete_table(u'allotments_district')


    models = {
        u'allotments.allotment': {
            'Meta': {'object_name': 'Allotment'},
            'acres': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'field_office': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'involved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'allotments.district': {
            'Meta': {'object_name': 'District'},
            'agency': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_unit': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['allotments']