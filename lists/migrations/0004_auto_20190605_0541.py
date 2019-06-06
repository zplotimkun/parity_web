# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_goods_keyword'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name_plural': 'Goods'},
        ),
    ]
