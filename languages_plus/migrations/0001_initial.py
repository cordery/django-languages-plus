# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('countries_plus', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CultureCode',
            fields=[
                ('code', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('country', models.ForeignKey(to='countries_plus.Country')),
            ],
            options={
                'ordering': ['code'],
                'verbose_name': 'CultureCode',
                'verbose_name_plural': 'CultureCodes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('iso_639_1', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('iso_639_2T', models.CharField(unique=True, max_length=3, blank=True)),
                ('iso_639_2B', models.CharField(unique=True, max_length=3, blank=True)),
                ('iso_639_3', models.CharField(max_length=3, blank=True)),
                ('iso_639_6', models.CharField(max_length=4, blank=True)),
                ('name_en', models.CharField(max_length=100)),
                ('name_native', models.CharField(max_length=100)),
                ('name_other', models.CharField(max_length=50, blank=True)),
                ('family', models.CharField(max_length=50)),
                ('notes', models.CharField(max_length=100, blank=True)),
                ('countries_spoken', models.ManyToManyField(to='countries_plus.Country', blank=True)),
            ],
            options={
                'ordering': ['name_en'],
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='culturecode',
            name='language',
            field=models.ForeignKey(to='languages_plus.Language'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='LangCountry',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('countries_plus.country',),
        ),
    ]
