# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_auto_20190605_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='store',
            field=models.CharField(max_length=20, default=''),
        ),
    ]
