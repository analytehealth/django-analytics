# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0007_alter_validators_add_error_messages'),
        ('djanalytics', '0002_prepopulate_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestevent',
            name='ip_address',
            field=models.GenericIPAddressField(db_index=True),
        ),
    ]
