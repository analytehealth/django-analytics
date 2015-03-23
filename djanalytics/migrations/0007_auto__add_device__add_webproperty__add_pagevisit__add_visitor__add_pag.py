# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Device'
        db.create_table(u'djanalytics_device', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('os_version', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('browser', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('browser_version', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('device', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('device_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.DeviceType'], null=True, blank=True)),
            ('screen_width', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('screen_height', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('djanalytics', ['Device'])

        # Adding model 'WebProperty'
        db.create_table(u'djanalytics_webproperty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
        ))
        db.send_create_signal('djanalytics', ['WebProperty'])

        # Adding model 'PageVisit'
        db.create_table(u'djanalytics_pagevisit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Page'])),
            ('visit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Visit'])),
            ('request_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.RequestEvent'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=0)),
        ))
        db.send_create_signal('djanalytics', ['PageVisit'])

        # Adding model 'Visitor'
        db.create_table(u'djanalytics_visitor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36)),
        ))
        db.send_create_signal('djanalytics', ['Visitor'])

        # Adding M2M table for field clients on 'Visitor'
        m2m_table_name = db.shorten_name(u'djanalytics_visitor_clients')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visitor', models.ForeignKey(orm['djanalytics.visitor'], null=False)),
            ('client', models.ForeignKey(orm['djanalytics.client'], null=False))
        ))
        db.create_unique(m2m_table_name, ['visitor_id', 'client_id'])

        # Adding model 'PagePattern'
        db.create_table(u'djanalytics_pagepattern', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('pattern', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Client'])),
            ('page_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.PageType'])),
        ))
        db.send_create_signal('djanalytics', ['PagePattern'])

        # Adding unique constraint on 'PagePattern', fields ['pattern', 'client']
        db.create_unique(u'djanalytics_pagepattern', ['pattern', 'client_id'])

        # Adding model 'Page'
        db.create_table(u'djanalytics_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Client'])),
            ('page_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.PageType'], null=True)),
        ))
        db.send_create_signal('djanalytics', ['Page'])

        # Adding unique constraint on 'Page', fields ['path', 'client']
        db.create_unique(u'djanalytics_page', ['path', 'client_id'])

        # Adding model 'Visit'
        db.create_table(u'djanalytics_visit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('visitor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Visitor'])),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.Device'])),
            ('visit_date', self.gf('django.db.models.fields.DateField')()),
            ('duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=0)),
            ('first_page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='first_visit', to=orm['djanalytics.Page'])),
            ('last_page', self.gf('django.db.models.fields.related.ForeignKey')(related_name='last_visit', null=True, to=orm['djanalytics.Page'])),
            ('conversion_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('web_property', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.WebProperty'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('djanalytics', ['Visit'])

        # Adding model 'ReferrerType'
        db.create_table(u'djanalytics_referrertype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
            ('pattern', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('djanalytics', ['ReferrerType'])

        # Adding model 'DeviceType'
        db.create_table(u'djanalytics_devicetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal('djanalytics', ['DeviceType'])

        # Adding model 'PageType'
        db.create_table(u'djanalytics_pagetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('djanalytics', ['PageType'])

        # Adding field 'Domain.name'
        db.add_column(u'djanalytics_domain', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Domain.web_property'
        db.add_column(u'djanalytics_domain', 'web_property',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djanalytics.WebProperty'], null=True),
                      keep_default=False)


        # Changing field 'Domain.pattern'
        db.alter_column(u'djanalytics_domain', 'pattern', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Page', fields ['path', 'client']
        db.delete_unique(u'djanalytics_page', ['path', 'client_id'])

        # Removing unique constraint on 'PagePattern', fields ['pattern', 'client']
        db.delete_unique(u'djanalytics_pagepattern', ['pattern', 'client_id'])

        # Deleting model 'Device'
        db.delete_table(u'djanalytics_device')

        # Deleting model 'WebProperty'
        db.delete_table(u'djanalytics_webproperty')

        # Deleting model 'PageVisit'
        db.delete_table(u'djanalytics_pagevisit')

        # Deleting model 'Visitor'
        db.delete_table(u'djanalytics_visitor')

        # Removing M2M table for field clients on 'Visitor'
        db.delete_table(db.shorten_name(u'djanalytics_visitor_clients'))

        # Deleting model 'PagePattern'
        db.delete_table(u'djanalytics_pagepattern')

        # Deleting model 'Page'
        db.delete_table(u'djanalytics_page')

        # Deleting model 'Visit'
        db.delete_table(u'djanalytics_visit')

        # Deleting model 'ReferrerType'
        db.delete_table(u'djanalytics_referrertype')

        # Deleting model 'DeviceType'
        db.delete_table(u'djanalytics_devicetype')

        # Deleting model 'PageType'
        db.delete_table(u'djanalytics_pagetype')

        # Deleting field 'Domain.name'
        db.delete_column(u'djanalytics_domain', 'name')

        # Deleting field 'Domain.web_property'
        db.delete_column(u'djanalytics_domain', 'web_property_id')


        # User chose to not deal with backwards NULL issues for 'Domain.pattern'
        raise RuntimeError("Cannot reverse this migration. 'Domain.pattern' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Domain.pattern'
        db.alter_column(u'djanalytics_domain', 'pattern', self.gf('django.db.models.fields.CharField')(max_length=100))

    models = {
        'djanalytics.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'aed4ab96-ab2e-49be-8248-792b60627bd7'", 'max_length': '36'})
        },
        'djanalytics.device': {
            'Meta': {'object_name': 'Device'},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'browser_version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.DeviceType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'os_version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'screen_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'screen_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'djanalytics.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
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
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'page_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.PageType']"}),
            'pattern': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'djanalytics.pagetype': {
            'Meta': {'object_name': 'PageType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
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
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
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
            'tracking_key': ('django.db.models.fields.CharField', [], {'default': "'8fbe15a1-2d5a-4e82-8dd3-c27dffd99b4e'", 'max_length': '36'}),
            'tracking_user_id': ('django.db.models.fields.CharField', [], {'default': "'3b74c3b4-934a-497d-b90b-2872c9cf118c'", 'max_length': '36'}),
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
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'visit_date': ('django.db.models.fields.DateField', [], {}),
            'visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.Visitor']"}),
            'web_property': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['djanalytics.WebProperty']"})
        },
        'djanalytics.visitor': {
            'Meta': {'object_name': 'Visitor'},
            'clients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['djanalytics.Client']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36'})
        },
        'djanalytics.webproperty': {
            'Meta': {'object_name': 'WebProperty'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['djanalytics']