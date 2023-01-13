=============================
Django Languages Plus
=============================

.. image:: https://badge.fury.io/py/django-languages-plus.svg
    :target: https://badge.fury.io/py/django-languages-plus

.. image:: https://travis-ci.org/cordery/django-languages-plus.svg?branch=master
    :target: https://travis-ci.org/cordery/django-languages-plus

.. image:: https://codecov.io/gh/cordery/django-languages-plus/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/cordery/django-languages-plus



django-languages-plus provides models and fixtures for working with both common languages and 'culture codes' or locale codes, like pt-BR.

Note that this is only a small (but popular) subset of all living languages, and is not even a comprehensive set of the ISO 639 languages.  It does however include the endonym/autonym/exonym.

The Language model contains all ISO 639-1 languages and related information from http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes

The model provides the following fields (original wikipedia.org column name in parentheses).

* name_en (ISO Language Name)
* name_native (Native Name)
* iso_639_1 (639-1)
* iso_639_2T = (639-2/T)
* iso_639_2B = (639-2/B)
* iso_639_3 = (639-3)
* family = (Language Family)
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

2. Migrate your database and load the language data fixture::

        python manage.py migrate
        python manage.py loaddata languages_data.json.gz

3. In your code use::

        from languages_plus.models import Language
        lang = Language.objects.get(iso_639_1='en')

---------------------------------------
Generating Culture Codes (ex: pt_BR)
---------------------------------------
django-countries-plus(https://pypi.python.org/pypi/django-countries-plus) is now an explicit requirement.  After installing both packages you can run the following command once to associate the two datasets and generate a list of culture codes (pt_BR for example)::

        from languages_plus.utils import associate_countries_and_languages
        associate_countries_and_languages()

---------------------------------------
Requirements
---------------------------------------
django-countries-plus >= 1.

Django:  Tested against the latest versions of 3, and 4.
Python 3


Running Tests
-------------

Does the code actually work?

::

    $ poetry install
    $ poetry run pytest

Or for the full tox suite:

::

    $ poetry install
    $ pip install tox
    $ tox
