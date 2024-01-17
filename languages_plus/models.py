from __future__ import unicode_literals

import logging
from typing import List, Tuple, Optional

from countries_plus.models import Country
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


class LanguageManager(models.Manager):
    def get_by_code(self, code: str) -> "Language":
        """
        Retrieve a language by a code.

        :param code: iso code (any of the three) or its culture code
        :return: a Language object
        """
        if any(x in code for x in ("_", "-")):
            cc = CultureCode.objects.get(code=code.replace("_", "-"))
            return cc.language

        elif len(code) == 2:
            return self.get(iso_639_1=code)

        elif len(code) == 3:
            return self.get(Q(iso_639_2T=code) | Q(iso_639_2B=code) | Q(iso_639_3=code))

        raise ValueError(
            'Code must be either 2, or 3 characters: "%s" is %s' % (code, len(code))
        )

    @staticmethod
    def get_culture_pair(code: str) -> Tuple["Language", "Country"]:
        """
        #  Return a tuple of the language and country for a given culture code
        :param code:
        :return:
        """
        if not any(x in code for x in ("_", "-")):
            raise ValueError("%s is not a valid culture code" % code)

        cc = CultureCode.objects.get(code=code.replace("_", "-"))
        return cc.language, cc.country

    def filter_by_codes(self, codes, sort: str = "name_en") -> List["Language"]:
        """
        Retrieve a list (not queryset) of languages from a list of codes
        The language objects retrieved by culture code will be annotated with the country and
        culture code.
        :param codes: list of strings that can be either iso codes (any of the three) or culture
        codes.
        :param sort: str name_en|name_native|sort_code
        :return: a list of languages
        """
        lang_codes = []
        cc_codes = []
        for code in codes:
            if any(x in code for x in ("_", "-")):
                cc_codes.append(code.replace("_", "-"))
            else:
                lang_codes.append(code)

        cc_langs = CultureCode.objects.filter(code__in=cc_codes).as_languages()

        qs = self.get_queryset().filter(
            Q(iso_639_1__in=lang_codes)
            | Q(iso_639_2T__in=lang_codes)
            | Q(iso_639_2B__in=lang_codes)
            | Q(iso_639_3__in=lang_codes)
        )
        langs = list(qs)
        langs.extend(cc_langs)
        langs.sort(key=lambda x: getattr(x, sort))
        return langs


class Language(models.Model):
    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ["name_en"]

    # Added by CultureCode when returning language objects
    country = None
    culturecode = None

    iso_639_1 = models.CharField(max_length=2, primary_key=True)
    iso_639_2T = models.CharField(max_length=3, unique=True, blank=True)
    iso_639_2B = models.CharField(max_length=3, unique=True, blank=True)
    iso_639_3 = models.CharField(max_length=3, blank=True)
    name_en = models.CharField(max_length=100)
    name_sv = models.CharField(max_length=100, blank=True)
    name_native = models.CharField(max_length=100)
    family = models.CharField(max_length=50)
    notes = models.CharField(max_length=100, blank=True)
    countries_spoken = models.ManyToManyField(Country, blank=True)

    objects = LanguageManager()

    @property
    def iso(self) -> str:
        return self.iso_639_1

    @property
    def name(self) -> str:
        return self.name_native

    @property
    def sort_code(self) -> str:
        return self._get_sort_code()

    def _get_sort_code(self) -> str:
        return self.culturecode or self.iso_639_1

    def __str__(self) -> str:
        return self.name_en


class CultureCodeQuerySet(QuerySet):
    def as_languages(self):
        """
        Get the Language objects associated with this queryset of CultureCodes as a list.
        The Language objects will have country and culturecode set.
        :return:
        """
        langs = []
        for culture_code in self.select_related("language", "country").all():
            lang = culture_code.language
            lang.country = culture_code.country
            lang.culturecode = culture_code.code
            langs.append(lang)
        return langs


class CultureCodeManager(models.Manager.from_queryset(CultureCodeQuerySet)):
    pass


class CultureCode(models.Model):
    class Meta:
        verbose_name = _("CultureCode")
        verbose_name_plural = _("CultureCodes")
        ordering = ["code"]

    code = models.CharField(max_length=10, primary_key=True)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    objects = CultureCodeManager()

    def __str__(self):
        return self.code


#  fix for django-csv-importer
class LangCountry(Country):
    class Meta:
        proxy = True


#  Enhance Country class
def primary_language(self) -> Optional["Language"]:
    try:
        lang = Language.objects.get_by_code(self.languages.split(",")[0])
    except Language.DoesNotExist:
        return None
    return lang


def get_all_languages(self, sort: str = "code") -> List["Language"]:
    """Retrieve the language objects for a country.

    Language objects will be annotated with the country and culturecode attributes when applicable.

    :param sort: code|name_en|name_native
    :return: A list of Language objects.
    """
    langs = list(self.culturecode_set.all().as_languages())
    langs.extend(self.language_set.exclude(iso_639_1__in=[x.iso_639_1 for x in langs]))
    if sort in ["name_en", "name_native"]:
        return sorted(langs, key=lambda x: getattr(x, sort))
    elif sort == "code":
        codes = self.languages.split(",")

        return sorted(langs, key=lambda x: codes.index(x.sort_code))
    raise ValueError(
        "Invalid code option %s.  Valid options are: code, name_en, name_native" % sort
    )


Country.add_to_class("primary_language", primary_language)
Country.add_to_class("get_all_languages", get_all_languages)
