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
            ('uuid', self.gf('django.db.models.fields.CharField')(default='4c876504-ae19-44c3-83e1-ae7c9c60db78', max_length=36)),
        ))
        db.send_create_signal('djanalytics', ['Client'])

        # Adding model 'RequestEvent'
        db.create_table(u'djanalytics_requestevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, db_index=True)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tracking_key', self.gf('django.db.models.fields.CharField')(default='64f280b1-08ba-4342-8e5a-c867cb7b78a4', max_length=36)),
            ('tracking_user_id', self.gf('django.db.models.fields.CharField')(default='5bcd7737-4707-419c-a3cd-95cef9a8a2c7', max_length=36)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('path', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('query_string', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 4, 0, 0), db_index=True)),
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'4c876504-ae19-44c3-83e1-ae7c9c60db78'", 'max_length': '36'})
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 4, 0, 0)', 'db_index': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'query_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tracking_key': ('django.db.models.fields.CharField', [], {'default': "'08143bfc-9f50-4c48-92d9-39ae09b7d09e'", 'max_length': '36'}),
            'tracking_user_id': ('django.db.models.fields.CharField', [], {'default': "'2facd44d-8cf3-4bc1-9e32-fbe3c2796090'", 'max_length': '36'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djanalytics']