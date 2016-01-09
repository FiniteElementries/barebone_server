# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_remove_userprofile_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('full_access', 'full access'), ('friend', 'friend'), ('blocked', 'blocked'), ('stranger', 'stranger'))},
        ),
    ]
