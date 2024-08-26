# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-08-14 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docsitalia', '0011_auto_20180726_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisherproject',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='publisherproject',
            name='slug',
            field=models.SlugField(max_length=255, verbose_name='slug'),
        ),
        migrations.AlterUniqueTogether(
            name='publisherproject',
            unique_together=set([('publisher', 'slug')]),
        ),
    ]
