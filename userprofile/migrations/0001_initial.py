# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'male'), (b'F', b'female')])),
                ('date_of_birth', models.DateField()),
                ('age', models.IntegerField()),
                ('language', models.CharField(max_length=10)),
                ('school', models.CharField(max_length=20)),
                ('career', models.CharField(max_length=20)),
                ('proximity', models.IntegerField()),
                ('blocked_friends', models.ManyToManyField(related_name='_userprofile_blocked_friends_+', null=True, to='userprofile.UserProfile', blank=True)),
                ('friends', models.ManyToManyField(related_name='_userprofile_friends_+', null=True, to='userprofile.UserProfile', blank=True)),
                ('recommendations', models.ManyToManyField(related_name='_userprofile_recommendations_+', null=True, to='userprofile.UserProfile', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
