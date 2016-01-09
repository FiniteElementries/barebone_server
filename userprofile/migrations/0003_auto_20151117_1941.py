# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20151116_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='career',
            field=models.CharField(default=b'Malong', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(default=b'Martian', max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='proximity',
            field=models.IntegerField(default=1, verbose_name=b'Proximity (km)'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='school',
            field=models.CharField(default=b'Community College', max_length=20),
        ),
    ]
