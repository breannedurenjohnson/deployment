# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-15 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='author',
            field=models.CharField(default='author', max_length=255),
            preserve_default=False,
        ),
    ]
