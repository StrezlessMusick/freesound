# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-02-05 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0036_sound_uploaded_with_bulk_upload_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='short_summary',
            field=models.TextField(null=True),
        ),
    ]