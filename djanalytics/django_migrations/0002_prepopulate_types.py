# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def prepopulate_types(apps, schema_editor):
    PageType = apps.get_model('djanalytics', 'PageType')
    for code in ('conversion', 'funnel'):
        PageType.objects.get_or_create(code=code, name=code.capitalize())

def delete_types(apps, schema_editor):
    PageType = apps.get_model('djanalytics', 'PageType')
    PageType.objects.filter(code__in=('conversion', 'funnel')).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('djanalytics', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(prepopulate_types, delete_types),
    ]
