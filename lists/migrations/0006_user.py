# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_goods_store'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=20)),
                ('mail', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'User',
            },
        ),
    ]
