# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-26 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('battles', '0002_hashtag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hashtag_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hashtag_1', to='battles.Hashtag')),
                ('hashtag_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hashtag_2', to='battles.Hashtag')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
    ]
