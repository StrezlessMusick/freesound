# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-02-07 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sounds', '0039_auto_20210607_1404'),
    ]

    operations = [
        migrations.RenameField(
            model_name='soundanalysis',
            old_name='extractor',
            new_name='analyzer',
        ),
        migrations.AddField(
            model_name='soundanalysis',
            name='analysis_status',
            field=models.CharField(choices=[(b'OK', b'Ok'), (b'SK', b'Skipped'), (b'FA', b'Failed')], db_index=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='soundanalysis',
            name='is_queued',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='soundanalysis',
            name='num_analysis_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='soundanalysis',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='soundanalysis',
            name='analysis_filename',
        ),
        migrations.AlterUniqueTogether(
            name='soundanalysis',
            unique_together=set([('sound', 'analyzer')]),
        ),
    ]