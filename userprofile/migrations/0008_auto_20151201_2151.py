# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_auto_20151125_2128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={},
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='blocked_friends',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='friends',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='blocked',
            field=models.ManyToManyField(related_name='_userprofile_blocked_+', null=True, to='userprofile.UserProfile', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='follower',
            field=models.ManyToManyField(related_name='_userprofile_follower_+', null=True, to='userprofile.UserProfile', blank=True),
        ),
    ]
