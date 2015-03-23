# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import re
import djanalytics.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('uuid', models.CharField(default=djanalytics.models.generate_uuid, max_length=36)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_agent', models.TextField(blank=True)),
                ('user_agent_md5', models.CharField(unique=True, max_length=32, db_index=True)),
                ('os', models.CharField(max_length=100, db_index=True)),
                ('os_version', models.CharField(db_index=True, max_length=20, null=True, blank=True)),
                ('browser', models.CharField(max_length=100, db_index=True)),
                ('browser_version', models.CharField(db_index=True, max_length=20, null=True, blank=True)),
                ('device', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
                ('screen_width', models.PositiveSmallIntegerField(db_index=True, null=True, blank=True)),
                ('screen_height', models.PositiveSmallIntegerField(db_index=True, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(db_index=True, unique=True, max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-Z0-9_]+$'), "Enter a valid 'type' consisting of letters, numbers, and/or underscores.", b'invalid')])),
                ('name', models.CharField(unique=True, max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('pattern', models.CharField(help_text=b'Deprecated, use an entry with name per domain instead', max_length=100, null=True, blank=True)),
                ('client', models.ForeignKey(to='djanalytics.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='IPFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('netmask', models.CharField(max_length=19)),
                ('include', models.BooleanField(default=False)),
                ('client', models.ForeignKey(to='djanalytics.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postal_code', models.CharField(max_length=25, null=True, blank=True)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('state', models.CharField(max_length=100, null=True, blank=True)),
                ('country', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.URLField()),
                ('client', models.ForeignKey(to='djanalytics.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PagePattern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(db_index=True, unique=True, max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-Z0-9_]+$'), "Enter a valid 'type' consisting of letters, numbers, and/or underscores.", b'invalid')])),
                ('name', models.CharField(max_length=80)),
                ('pattern', models.CharField(max_length=200)),
                ('display_path', models.CharField(help_text=b'How to display on reports', max_length=200)),
                ('client', models.ForeignKey(to='djanalytics.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(db_index=True, unique=True, max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-Z0-9_]+$'), "Enter a valid 'type' consisting of letters, numbers, and/or underscores.", b'invalid')])),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageVisit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('duration', models.DecimalField(null=True, max_digits=7, decimal_places=0)),
                ('page', models.ForeignKey(to='djanalytics.Page')),
            ],
            options={
                'get_latest_by': 'request_event__created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PathFilter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path_pattern', models.CharField(max_length=200)),
                ('include', models.BooleanField(default=False)),
                ('client', models.ForeignKey(to='djanalytics.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferrerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(db_index=True, unique=True, max_length=50, validators=[django.core.validators.RegexValidator(re.compile(b'^[a-zA-Z0-9_]+$'), "Enter a valid 'type' consisting of letters, numbers, and/or underscores.", b'invalid')])),
                ('name', models.CharField(unique=True, max_length=80)),
                ('pattern', models.CharField(unique=True, max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RequestEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.IPAddressField(db_index=True)),
                ('user_agent', models.TextField(null=True, blank=True)),
                ('tracking_key', models.CharField(default=djanalytics.models.generate_uuid, max_length=36, db_index=True)),
                ('tracking_user_id', models.CharField(default=djanalytics.models.generate_uuid, max_length=36, db_index=True)),
                ('protocol', models.CharField(max_length=10)),
                ('domain', models.CharField(max_length=100, db_index=True)),
                ('path', models.URLField(db_index=True, blank=True)),
                ('query_string', models.TextField(null=True, blank=True)),
                ('method', models.CharField(db_index=True, max_length=5, null=True, blank=True)),
                ('referrer', models.URLField(max_length=2083, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('response_code', models.IntegerField(db_index=True, null=True, blank=True)),
                ('screen_width', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('screen_height', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('client', models.ForeignKey(to='djanalytics.Client')),
                ('location', models.ForeignKey(blank=True, to='djanalytics.Location', null=True)),
            ],
            options={
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=36, db_index=True)),
                ('visit_date', models.DateField(db_index=True)),
                ('duration', models.DecimalField(null=True, max_digits=7, decimal_places=0)),
                ('conversion_count', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(to='djanalytics.Device')),
                ('first_page', models.ForeignKey(related_name='first_visit', to='djanalytics.Page')),
                ('last_page', models.ForeignKey(related_name='last_visit', to='djanalytics.Page', null=True)),
                ('pages', models.ManyToManyField(to='djanalytics.Page', through='djanalytics.PageVisit')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=36, db_index=True)),
                ('clients', models.ManyToManyField(to='djanalytics.Client')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WebProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Web properties',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='visit',
            name='visitor',
            field=models.ForeignKey(to='djanalytics.Visitor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='visit',
            name='web_property',
            field=models.ForeignKey(to='djanalytics.WebProperty'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagevisit',
            name='request_event',
            field=models.ForeignKey(to='djanalytics.RequestEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagevisit',
            name='visit',
            field=models.ForeignKey(to='djanalytics.Visit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pagepattern',
            name='page_type',
            field=models.ForeignKey(to='djanalytics.PageType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pagepattern',
            unique_together=set([('pattern', 'client')]),
        ),
        migrations.AddField(
            model_name='page',
            name='page_type',
            field=models.ForeignKey(to='djanalytics.PageType', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('path', 'client')]),
        ),
        migrations.AddField(
            model_name='domain',
            name='web_property',
            field=models.ForeignKey(to='djanalytics.WebProperty', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(blank=True, to='djanalytics.DeviceType', null=True),
            preserve_default=True,
        ),
        migrations.AlterIndexTogether(
            name='device',
            index_together=set([('screen_width', 'screen_height'), ('os', 'os_version'), ('browser', 'browser_version')]),
        ),
    ]
