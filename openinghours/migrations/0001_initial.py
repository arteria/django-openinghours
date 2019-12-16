# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from openinghours.app_settings import PREMISES_MODEL


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(verbose_name='Name', max_length=100)),
                ('slug', models.SlugField(verbose_name='Slug', unique=True)),
                ('logo', models.FileField(verbose_name='Logo', null=True, blank=True, upload_to=b'logo')),
            ],
            options={
                'swappable': 'OPENINGHOURS_PREMISES_MODEL',
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='ClosingRules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(verbose_name='Start')),
                ('end', models.DateTimeField(verbose_name='End')),
                ('reason', models.TextField(verbose_name='Reason', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Closing Rule',
                'verbose_name_plural': 'Closing Rules',
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.IntegerField(verbose_name='Weekday', choices=[
                    (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'),
                    (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')
                ])),
                ('from_hour', models.TimeField(verbose_name='Opening')),
                ('to_hour', models.TimeField(verbose_name='Closing')),
                ('company', models.ForeignKey(verbose_name='Company', to=PREMISES_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Opening Hours',
                'verbose_name_plural': 'Opening Hours',
                'ordering': ['company', 'weekday', 'from_hour'],
            },
        ),
        migrations.AddField(
            model_name='closingrules',
            name='company',
            field=models.ForeignKey(verbose_name='Company', to=PREMISES_MODEL, on_delete=models.CASCADE),
        ),
    ]
