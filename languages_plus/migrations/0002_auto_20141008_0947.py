# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import gzip

from django.core import serializers
from django.db import migrations


fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../fixtures'))
fixture_filename = 'initial_data_orig.json.gz'

# Taken from https://stackoverflow.com/questions/25960850/loading-initial-data-with-django-1-7-and-data-migrations


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)

    with gzip.open(fixture_file, 'rb') as fixture:
        objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
        for obj in objects:
            obj.save()


def unload_fixture(apps, schema_editor):
    """Brutally deleting all entries for this model..."""

    MyModel = apps.get_model("languages_plus", "Language")
    MyModel.objects.all().delete()

    MyModel = apps.get_model("languages_plus", "CultureCode")
    MyModel.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('languages_plus', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]