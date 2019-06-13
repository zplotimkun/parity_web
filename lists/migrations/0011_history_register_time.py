# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0010_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='register_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 13, 3, 52, 0, 456241, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
