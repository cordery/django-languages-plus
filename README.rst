===========
django-languages-plus
===========

django-languages-plus provides models and fixtures for working with both langauges and 'culture codes' or locale codes, like pt-BR.

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

        from countries_plus.models import Country
        usa = Country.objects.get(iso3='USA')


Enbling the optional middleware::

1.  Follow steps 1 & 2 above.

2.  Add 'countries_plus.middleware.AddRequestCountryMiddleware' to your middleware.

3.  add the following two settings:
    COUNTRIES_PLUS_COUNTRY_HEADER   -   A string defining the name of the meta header that provides the country code.  Ex: 'HTTP_CF_COUNTRY' (from https://support.cloudflare.com/hc/en-us/articles/200168236-What-does-CloudFlare-IP-Geolocation-do-)

    COUNTRIES_PLUS_DEFAULT_ISO  -   A string containing an iso code for the country you want to use as a fallback in the case of a missing or malformed geoip header.  Ex:  'US' or 'DE' or 'BR'

