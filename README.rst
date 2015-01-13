=====================
django-languages-plus
=====================

django-languages-plus provides models and fixtures for working with both common languages and 'culture codes' or locale codes, like pt-BR.

Note that this is only a small (but popular) subset of all living languages, and is not even a comprehensive set of the ISO 639 languages.  It does however include the endonym/autonym/exonym.

The Language model contains all ISO 639-1 languages and related information from http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

The model provides the following fields (original wikipedia.org column name in parentheses).

* name_en (Language name (in english))
* name_native (Native name)
* iso_639_1 (639-1)
* iso_639_2T = (639-2T)
* iso_639_2B = (639-2B)
* iso_639_3 = (639-3)
* iso_639_6 = (639-6)
* name_en = models
* name_native = mo
* name_other = mod
* family = models.
* countries_spoken


------------
Installation
------------

::

    pip install django-languages-plus


------------
Usage
------------

1. Add ``languages_plus`` to your INSTALLED_APPS

2. Sync your fixtures::

        python manage.py syncdb

3. In your code use::

        from languages_plus.models import Language
        lang = Lanuage.objects.get(iso_639_1='en')

---------------------------------------
Integrating with django-countries-plus
---------------------------------------
If you also have django-countries-plus(https://pypi.python.org/pypi/django-countries-plus) installed then you can run the following command once to associate the two datasets and generate a list of culture codes (pt_BR for example)::

        from languages_plus.utils import associate_countries_and_languages
        associate_countries_and_languages()

---------------------------------------
Requirements
---------------------------------------
Should work on most versions of Django, however if you are using Django 1.7, tests will fail unless you are using Django 1.7.2 or higher due to a bug in earlier versions.
