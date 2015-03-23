# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Device.user_agent_md5'
        db.add_column(u'djanalytics_device', 'user_agent_md5',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=32, db_index=True),
                      keep_default=False)

        # Adding index on 'Device', fields ['screen_width']
        db.create_index(u'djanalytics_device', ['screen_width'])

        # Adding index on 'Device', fields ['os_version']
        db.create_index(u'djanalytics_device', ['os_version'])

        # Adding index on 'Device', fields ['browser_version']
        db.create_index(u'djanalytics_device', ['browser_version'])

        # Adding index on 'Device', fields ['device']
        db.create_index(u'djanalytics_device', ['device'])

        # Adding index on 'Device', fields ['browser']
        db.create_index(u'djanalytics_device', ['browser'])

        # Adding index on 'Device', fields ['os']
        db.create_index(u'djanalytics_device', ['os'])

        # Adding index on 'Device', fields ['screen_height']
        db.create_index(u'djanalytics_device', ['screen_height'])

        # Adding index on 'Device', fields ['screen_width', 'screen_height']
        db.create_index(u'djanalytics_device', ['screen_width', 'screen_height'])

        # Adding index on 'Device', fields ['os', 'os_version']
        db.create_index(u'djanalytics_device', ['os', 'os_version'])

        # Adding index on 'Device', fields ['browser', 'browser_version']
        db.create_index(u'djanalytics_device', ['browser', 'browser_version'])

        # Adding index on 'PageType', fields ['code']
        db.create_index(u'djanalytics_pagetype', ['code'])

        # Adding index on 'RequestEvent', fields ['tracking_key']
        db.create_index(u'djanalytics_requestevent', ['tracking_key'])

        # Adding index on 'RequestEvent', fields ['tracking_user_id']
        db.create_index(u'djanalytics_requestevent', ['tracking_user_id'])

        # Adding index on 'Visitor', fields ['uuid']
        db.create_index(u'djanalytics_visitor', ['uuid'])

        # Adding index on 'Visit', fields ['visit_date']
        db.create_index(u'djanalytics_visit', ['visit_date'])

        # Adding index on 'Visit', fields ['uuid']
        db.create_index(u'djanalytics_visit', ['uuid'])

        # Adding index on 'ReferrerType', fields ['code']
        db.create_index(u'djanalytics_referrertype', ['code'])

        # Adding index on 'DeviceType', fields ['code']
        db.create_index(u'djanalytics_devicetype', ['code'])

        # Adding field 'PagePattern.display_path'
        db.add_column(u'djanalytics_pagepattern', 'display_path',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200),
                      keep_default=False)

        # Adding index on 'PagePattern', fields ['code']
        db.create_index(u'djanalytics_pagepattern', ['code'])


    def backwards(self, orm):
        # Removing index on 'PagePattern', fields ['code']
        db.delete_index(u'djanalytics_pagepattern', ['code'])

        # Removing index on 'DeviceType', fields ['code']
        db.delete_index(u'djanalytics_devicetype', ['code'])

        # Removing index on 'ReferrerType', fields ['code']
        db.delete_index(u'djanalytics_referrertype', ['code'])

        # Removing index on 'Visit', fields ['uuid']
        db.delete_index(u'djanalytics_visit', ['uuid'])

        # Removing index on 'Visit', fields ['visit_date']
        db.delete_index(u'djanalytics_visit', ['visit_date'])

        # Removing index on 'Visitor', fields ['uuid']
        db.delete_index(u'djanalytics_visitor', ['uuid'])

        # Removing index on 'RequestEvent', fields ['tracking_user_id']
        db.delete_index(u'djanalytics_requestevent', ['tracking_user_id'])

        # Removing index on 'RequestEvent', fields ['tracking_key']
        db.delete_index(u'djanalytics_requestevent', ['tracking_key'])

        # Removing index on 'PageType', fields ['code']
        db.delete_index(u'djanalytics_pagetype', ['code'])

        # Removing index on 'Device', fields ['browser', 'browser_version']
        db.delete_index(u'djanalytics_device', ['browser', 'browser_version'])

        # Removing index on 'Device', fields ['os', 'os_version']
        db.delete_index(u'djanalytics_device', ['os', 'os_version'])

        # Removing index on 'Device', fields ['screen_width', 'screen_height']
        db.delete_index(u'djanalytics_device', ['screen_width', 'screen_height'])

        # Removing index on 'Device', fields ['screen_height']
        db.delete_index(u'djanalytics_device', ['screen_height'])

        # Removing index on 'Device', fields ['os']
        db.delete_index(u'djanalytics_device', ['os'])

        # Removing index on 'Device', fields ['browser']
        db.delete_index(u'djanalytics_device', ['browser'])

        # Removing index on 'Device', fields ['device']
        db.delete_index(u'djanalytics_device', ['device'])

        # Removing index on 'Device', fields ['browser_version']
        db.delete_index(u'djanalytics_device', ['browser_version'])

        # Removing index on 'Device', fields ['os_version']
        db.delete_index(u'djanalytics_device', ['os_version'])

        # Removing index on 'Device', fields ['screen_width']
        db.delete_index(u'djanalytics_device', ['screen_width'])

        # Deleting field 'Device.user_agent_md5'
        db.delete_column(u'djanalytics_device', 'user_agent_md5')

        # Deleting field 'PagePattern.display_path'
        db.delete_column(u'djanalytics_pagepattern', 'display_path')


    models = {
        'djanalytics.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'a613d16b-2fca-43c4-8f10-d3d967289c7b'", 'max_length': '36'})
        },
        'djanalytics.device': {
            'Meta': {'object_name': 'Device', 'index_together': "[('browser', 'browser_version'), ('os', 'os_version'), ('screen_width', 'screen_height')]"},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'browser_version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.DeviceType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'os_version': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'screen_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'screen_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_agent_md5': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32', 'db_index': 'True'})
        },
        'djanalytics.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'})
        },
        'djanalytics.domain': {
            'Meta': {'object_name': 'Domain'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'web_property': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.WebProperty']", 'null': 'True'})
        },
        'djanalytics.ipfilter': {
            'Meta': {'object_name': 'IPFilter'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'djanalytics.page': {
            'Meta': {'unique_together': "(('path', 'client'),)", 'object_name': 'Page'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.PageType']", 'null': 'True'}),
            'path': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'djanalytics.pagepattern': {
            'Meta': {'unique_together': "(('pattern', 'client'),)", 'object_name': 'PagePattern'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'display_path': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.PageType']"}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'djanalytics.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'djanalytics.pagevisit': {
            'Meta': {'object_name': 'PageVisit'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Page']"}),
            'request_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.RequestEvent']"}),
            'visit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Visit']"})
        },
        'djanalytics.pathfilter': {
            'Meta': {'object_name': 'PathFilter'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Client']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'path_pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'djanalytics.referrertype': {
            'Meta': {'object_name': 'ReferrerType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'pattern': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
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
            'screen_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'screen_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tracking_key': ('django.db.models.fields.CharField', [], {'default': "'e9721934-59a1-4bdb-a5e8-377c6aafc1b6'", 'max_length': '36', 'db_index': 'True'}),
            'tracking_user_id': ('django.db.models.fields.CharField', [], {'default': "'5d725c5a-e9fd-477e-8a99-dc2512d19dbe'", 'max_length': '36', 'db_index': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'djanalytics.visit': {
            'Meta': {'object_name': 'Visit'},
            'conversion_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Device']"}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '0'}),
            'first_page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_visit'", 'to': "orm['djanalytics.Page']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_page': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_visit'", 'null': 'True', 'to': "orm['djanalytics.Page']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['djanalytics.Page']", 'through': "orm['djanalytics.PageVisit']", 'symmetrical': 'False'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'visit_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Visitor']"}),
            'web_property': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.WebProperty']"})
        },
        'djanalytics.visitor': {
            'Meta': {'object_name': 'Visitor'},
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['djanalytics.Client']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'})
        },
        'djanalytics.webproperty': {
            'Meta': {'object_name': 'WebProperty'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['djanalytics']