# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_auto_20151201_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='follower',
            field=models.ManyToManyField(to='userprofile.UserProfile', null=True, blank=True),
        ),
    ]
