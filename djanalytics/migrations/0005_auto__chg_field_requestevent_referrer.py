# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
# django 1.5 compatibility
try:
    from django.db.utils import OperationalError
except:
    OperationalError = Exception


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RequestEvent.referrer'
        try:
            db.delete_index(u'djanalytics_requestevent', ['referrer'])
        except OperationalError:
            # index might not exist - not the end of the world
            pass
        db.alter_column(u'djanalytics_requestevent', 'referrer', self.gf('django.db.models.fields.URLField')(max_length=2083, null=True))

    def backwards(self, orm):

        # Changing field 'RequestEvent.referrer'
        db.alter_column(u'djanalytics_requestevent', 'referrer', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))
        db.create_index(u'djanalytics_requestevent', ['referrer'])

    models = {
        'djanalytics.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'aefccf95-69b6-4230-9e52-502d51291511'", 'max_length': '36'})
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
            'include': ('django.db.models.fields.BooleanField', [], {}),
            'netmask': ('django.db.models.fields.CharField', [], {'max_length': '19'})
        },
        u'djanalytics.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'djanalytics.pathfilter': {
            'Meta': {'object_name': 'PathFilter'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.BooleanField', [], {}),
            'path_pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'djanalytics.requestevent': {
            'Meta': {'object_name': 'RequestEvent'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djanalytics.Location']", 'null': 'True', 'blank': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'query_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.URLField', [], {'max_length': '2083', 'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'tracking_key': ('django.db.models.fields.CharField', [], {'default': "'b08a999f-d1fe-48ba-9b4a-f8c44298e8c1'", 'max_length': '36'}),
            'tracking_user_id': ('django.db.models.fields.CharField', [], {'default': "'04457bac-4357-42f2-ae8f-2762e60892e0'", 'max_length': '36'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djanalytics']
