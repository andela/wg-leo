# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-07-20 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealitem',
            name='meal_choice',
            field=models.CharField(default='Planned', max_length=10, verbose_name='Meal choice'),
        ),
    ]
