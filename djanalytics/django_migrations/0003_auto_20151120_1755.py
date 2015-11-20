# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djanalytics', '0002_prepopulate_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestevent',
            name='ip_address',
            field=models.GenericIPAddressField(db_index=True),
        ),
    ]
