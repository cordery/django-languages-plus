import logging

from countries_plus.models import Country
from django.core.exceptions import ObjectDoesNotExist

from .models import Language, CultureCode

logger = logging.getLogger(__name__)


def associate_countries_and_languages():
    languages = {x.iso_639_1: x for x in Language.objects.all()}
    countries = {x.iso: x for x in Country.objects.exclude(languages=None)}

    for country in countries.values():
        codes = country.languages.strip(',').split(',')
        for code in codes:
            if '-' in code:
                lang_code, country_code = code.split('-')
                language = languages.get(lang_code)
                if not language:
                    logger.info('Cannot find language identified by code %s' % lang_code)
                    continue

                country = countries.get(country_code)
                if not country:
                    logger.info('Cannot find country identified by code %s' % country_code)
                    continue

                country.language_set.add(language)
                CultureCode.objects.get_or_create(code=code, language=language,
                                                  country=country)
            else:
                try:
                    language = Language.objects.get_by_code(code)
                    country.language_set.add(language)
                except ObjectDoesNotExist:
                    logger.info('Cannot find language identified by code %s' % code)
                    continue
