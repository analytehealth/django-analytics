# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RequestEvent.referrer'
        db.add_column(u'djanalytics_requestevent', 'referrer',
                      self.gf('django.db.models.fields.URLField')(db_index=True, max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding index on 'RequestEvent', fields ['domain']
        db.create_index(u'djanalytics_requestevent', ['domain'])

        # Adding index on 'RequestEvent', fields ['response_code']
        db.create_index(u'djanalytics_requestevent', ['response_code'])

        # Adding index on 'RequestEvent', fields ['path']
        db.create_index(u'djanalytics_requestevent', ['path'])

        # Adding index on 'RequestEvent', fields ['method']
        db.create_index(u'djanalytics_requestevent', ['method'])


    def backwards(self, orm):
        # Removing index on 'RequestEvent', fields ['method']
        db.delete_index(u'djanalytics_requestevent', ['method'])

        # Removing index on 'RequestEvent', fields ['path']
        db.delete_index(u'djanalytics_requestevent', ['path'])

        # Removing index on 'RequestEvent', fields ['response_code']
        db.delete_index(u'djanalytics_requestevent', ['response_code'])

        # Removing index on 'RequestEvent', fields ['domain']
        db.delete_index(u'djanalytics_requestevent', ['domain'])

        # Deleting field 'RequestEvent.referrer'
        db.delete_column(u'djanalytics_requestevent', 'referrer')


    models = {
        'djanalytics.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'a7f673bd-7012-45d4-b73b-2da09a04f606'", 'max_length': '36'})
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
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 6, 0, 0)', 'db_index': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'db_index': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'query_string': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'tracking_key': ('django.db.models.fields.CharField', [], {'default': "'9ec26a33-a15b-4ea7-a3cf-8687112e0864'", 'max_length': '36'}),
            'tracking_user_id': ('django.db.models.fields.CharField', [], {'default': "'c13c1683-b8d6-42d4-b662-a6bf7209b872'", 'max_length': '36'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djanalytics']