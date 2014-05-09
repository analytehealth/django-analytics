# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'djanalytics_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='f98283ab-0d34-4976-a0ab-8e10b0d4d274', max_length=36)),
        ))
        db.send_create_signal('djanalytics', ['Client'])

        # Adding model 'RequestEvent'
        db.create_table(u'djanalytics_requestevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tracking_key', self.gf('django.db.models.fields.CharField')(default='ef26ad80-fadc-400b-83a3-0b78e2b154fb', max_length=36)),
            ('path', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('query_string', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('response_code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Client'])),
        ))
        db.send_create_signal('djanalytics', ['RequestEvent'])

        # Adding model 'Domain'
        db.create_table(u'djanalytics_domain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Client'])),
        ))
        db.send_create_signal('djanalytics', ['Domain'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'djanalytics_client')

        # Deleting model 'RequestEvent'
        db.delete_table(u'djanalytics_requestevent')

        # Deleting model 'Domain'
        db.delete_table(u'djanalytics_domain')


    models = {
        'djanalytics.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'f98283ab-0d34-4976-a0ab-8e10b0d4d274'", 'max_length': '36'})
        },
        'djanalytics.domain': {
            'Meta': {'object_name': 'Domain'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djanalytics.requestevent': {
            'Meta': {'object_name': 'RequestEvent'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'path': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'query_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tracking_key': ('django.db.models.fields.CharField', [], {'default': "'c64a98ce-a748-44f7-9512-96f0da4ae022'", 'max_length': '36'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djanalytics']