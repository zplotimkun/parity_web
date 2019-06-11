# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='register_time',
            field=models.DateTimeField(verbose_name='註冊時間', default=datetime.datetime(2019, 6, 11, 1, 17, 5, 691897, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
