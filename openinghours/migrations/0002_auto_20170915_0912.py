# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openinghours', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='closingrules',
            options={'ordering': ['start'], 'verbose_name_plural': 'Closing Rules', 'verbose_name': 'Closing Rule'},
        ),
        migrations.AlterModelOptions(
            name='openinghours',
            options={'ordering': ['company', 'weekday', 'from_hour'], 'verbose_name_plural': 'Opening Hours', 'verbose_name': 'Opening Hours'},
        ),
        migrations.AlterField(
            model_name='closingrules',
            name='company',
            field=models.ForeignKey(to='openinghours.Company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='closingrules',
            name='end',
            field=models.DateTimeField(verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='closingrules',
            name='reason',
            field=models.TextField(null=True, verbose_name='Reason', blank=True),
        ),
        migrations.AlterField(
            model_name='closingrules',
            name='start',
            field=models.DateTimeField(verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.FileField(null=True, upload_to=b'logo', verbose_name='Logo', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='slug',
            field=models.SlugField(verbose_name='Slug', unique=True),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='company',
            field=models.ForeignKey(to='openinghours.Company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='from_hour',
            field=models.TimeField(verbose_name='Opening'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='to_hour',
            field=models.TimeField(verbose_name='Closing'),
        ),
        migrations.AlterField(
            model_name='openinghours',
            name='weekday',
            field=models.IntegerField(verbose_name='Weekday', choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')]),
        ),
    ]
