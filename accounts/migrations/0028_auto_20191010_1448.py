# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-10-10 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_deleteduser_last_login'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deleteduser',
            name='type',
        ),
        migrations.AddField(
            model_name='deleteduser',
            name='reason',
            field=models.CharField(choices=[(b'ss', b'Sound spammer'), (b'fs', b'Forum/comments/messages spammer'), (b'ad', b'Deleted by an admin'), (b'sd', b'Self deleted')], default='ss', max_length=2),
            preserve_default=False,
        ),
    ]
