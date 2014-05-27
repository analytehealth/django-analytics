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
            ('uuid', self.gf('django.db.models.fields.CharField')(default='94b4dd7c-e98e-4e13-bf9a-35f4e8613245', max_length=36)),
        ))
        db.send_create_signal('djanalytics', ['Client'])

        # Adding model 'RequestEvent'
        db.create_table(u'djanalytics_requestevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tracking_key', self.gf('django.db.models.fields.CharField')(default='089c084b-18bc-4a16-b27f-42dcef918bb6', max_length=36)),
            ('tracking_user_id', self.gf('django.db.models.fields.CharField')(default='78612f3e-3da0-4464-9fe2-a22ccf0cb383', max_length=36)),
            ('path', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('query_string', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
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

        # Adding model 'IPFilter'
        db.create_table(u'djanalytics_ipfilter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('netmask', self.gf('django.db.models.fields.CharField')(max_length=19)),
            ('include', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Client'])),
        ))
        db.send_create_signal('djanalytics', ['IPFilter'])

        # Adding model 'PathFilter'
        db.create_table(u'djanalytics_pathfilter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path_pattern', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('include', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Client'])),
        ))
        db.send_create_signal('djanalytics', ['PathFilter'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'djanalytics_client')

        # Deleting model 'RequestEvent'
        db.delete_table(u'djanalytics_requestevent')

        # Deleting model 'Domain'
        db.delete_table(u'djanalytics_domain')

        # Deleting model 'IPFilter'
        db.delete_table(u'djanalytics_ipfilter')

        # Deleting model 'PathFilter'
        db.delete_table(u'djanalytics_pathfilter')


    models = {
        'djanalytics.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'94b4dd7c-e98e-4e13-bf9a-35f4e8613245'", 'max_length': '36'})
        },
        'djanalytics.domain': {
            'Meta': {'object_name': 'Domain'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'djanalytics.ipfilter': {
            'Meta': {'object_name': 'IPFilter'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'netmask': ('django.db.models.fields.CharField', [], {'max_length': '19'})
        },
        'djanalytics.pathfilter': {
            'Meta': {'object_name': 'PathFilter'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path_pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'djanalytics.requestevent': {
            'Meta': {'object_name': 'RequestEvent'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'path': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'query_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tracking_key': ('django.db.models.fields.CharField', [], {'default': "'c200a12e-8927-4e1d-b9a9-90b50ddf4411'", 'max_length': '36'}),
            'tracking_user_id': ('django.db.models.fields.CharField', [], {'default': "'aad52790-177f-4c6a-811f-c5fc8c8023b8'", 'max_length': '36'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djanalytics']