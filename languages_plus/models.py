from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models import Q
from rentalsite.countries_plus.models import Country
from django.db.models.query import QuerySet


class LanguageManager(models.Manager):

    #  Retrieve a language by either an iso code (any of the three) or its culture code.
    def get_by_code(self, code):
        if any(x in code for x in ('_', '-')):
            cc = CultureCode.objects.get(code=code.replace('_', '-'))
            return cc.language
        elif len(code) > 2:
            try:
                return Language.objects.get(iso_639_2=code)
            except ObjectDoesNotExist:
                pass

            try:
                return Language.objects.get(iso_639_3=code)
            except ObjectDoesNotExist:
                pass

            try:
                return Language.objects.get(iso_639_3=code)
            except ObjectDoesNotExist:
                pass

            raise Language.DoesNotExist

        else:
            return Language.objects.get(iso_639_1=code)

    #  Return a tuple of the language and country for a given culture code
    def get_culture_pair(self, code):
        if not any(x in code for x in ('_', '-')):
            raise ValueError("%s is not a valid culture code" % code)

        cc = CultureCode.objects.get(code=code.replace('_', '-'))
        return cc.language, cc.country

    #  Retrieve a list (not queryset) of languages from a list of codes that can be either iso codes (any of the three) or culture codes.
    #  The language objects retreived by culture code will be annotated with the country and culture code
    def filter_by_codes(self, codes, sort='name_en'):
        lang_codes = []
        cc_codes = []
        for code in codes:
            if any(x in code for x in ('_', '-')):
                cc_codes.append(code.replace('_', '-'))
            else:
                lang_codes.append(code)

        cc_langs = CultureCode.objects.filter(code__in=cc_codes).get_culture_code_languages()

        qs = self.get_queryset().filter(Q(iso_639_1__in=lang_codes) | Q(iso_639_2T__in=lang_codes) | Q(iso_639_2B__in=lang_codes) | Q(iso_639_3__in=lang_codes))
        langs = [lang for lang in qs]
        langs.extend(cc_langs)
        langs.sort(key=lambda x: getattr(x, sort))
        return langs


class Language(models.Model):

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['name_en']

    # Added by CultureCode when returning language objects
    country = None
    culturecode = None

    iso_639_1 = models.CharField(max_length=2, primary_key=True)
    iso_639_2T = models.CharField(max_length=3, unique=True, blank=True)
    iso_639_2B = models.CharField(max_length=3, unique=True, blank=True)
    iso_639_3 = models.CharField(max_length=3, blank=True)
    iso_639_6 = models.CharField(max_length=4, blank=True)
    name_en = models.CharField(max_length=100)
    name_native = models.CharField(max_length=100)
    name_other = models.CharField(max_length=50, blank=True)
    family = models.CharField(max_length=50)
    notes = models.CharField(max_length=100, blank=True)
    countries_spoken = models.ManyToManyField(Country, blank=True, null=True)

    objects = LanguageManager()

    @property
    def iso(self):
        return self.iso_639_1

    @property
    def name(self):
        return self.name_native

    def _get_sort_code(self):
        if self.culturecode:
            return self.culturecode
        return self.iso_639_1

    def __unicode__(self):
        return u'%s' % (self.name_en,)


class CultureCodeMixin(object):

    def as_languages(self):
        langs = []
        for culturecode in self.all():
            lang = culturecode.language
            lang.country = culturecode.country
            lang.culturecode = culturecode.code
            langs.append(lang)
        return langs


class CultureCodeQuerySet(QuerySet, CultureCodeMixin):
    pass


class CultureCodeManager(models.Manager, CultureCodeMixin):

    def get_query_set(self):
        return CultureCodeQuerySet(self.model, using=self._db)


class CultureCode(models.Model):

    class Meta:
        verbose_name = _('CultureCode')
        verbose_name_plural = _('CultureCodes')
        ordering = ['code']

    code = models.CharField(max_length=10, primary_key=True)
    language = models.ForeignKey('Language')
    country = models.ForeignKey(Country)

    objects = CultureCodeManager()

    def __unicode__(self):
        return self.code


#  fix for django-csv-importer
class LangCountry(Country):

    class Meta:
        proxy = True


#  Enhance Country class
def primary_language(self):
    try:
        lang = Language.objects.get_by_code(self.languages.split(',')[0])
    except:
        return None
    return lang


def get_all_languages(self, sort='code'):
    langs = list(self.language_set.all())
    langs.extend(self.culturecode_set.all().as_languages())
    if sort in ['name_en', 'name_native']:
        langs.sort(key=lambda x: getattr(x, sort))
    else:
        langs.sort(key=lambda x: self.languages.split(',').index(x._get_sort_code()))
    return langs

Country.add_to_class('primary_language', primary_language)
Country.add_to_class('get_all_languages', get_all_languages)
