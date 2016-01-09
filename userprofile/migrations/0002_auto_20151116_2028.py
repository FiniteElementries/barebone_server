# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='about_me',
            field=models.TextField(default=b'Something about myself...'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(default=b'Single City', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='proximity',
            field=models.IntegerField(verbose_name=b'Proximity (km)'),
        ),
    ]
