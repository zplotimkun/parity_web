# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_goods'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='keyword',
            field=models.CharField(max_length=20, default=''),
        ),
    ]
