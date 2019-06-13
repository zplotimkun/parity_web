# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0009_auto_20190611_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('keyword', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to='lists.User')),
            ],
            options={
                'verbose_name_plural': 'History',
            },
        ),
    ]
