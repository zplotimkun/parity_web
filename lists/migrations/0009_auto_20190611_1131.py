# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0008_auto_20190611_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='register_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
