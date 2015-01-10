from django.core.exceptions import ObjectDoesNotExist
from countries_plus.models import Country

from .models import Language, CultureCode


def associate_countries_and_languages():
    for country in Country.objects.all():
        langs = country.languages.strip(',')
        if langs:
            codes = langs.split(",")
            for code in codes:
                if '-' in code:
                    lang_code, country_code = code.split('-')
                    try:
                        language = Language.objects.get(iso_639_1=lang_code)
                    except ObjectDoesNotExist:
                        print("Cannot find language identified by code %s" % lang_code)
                        continue

                    try:
                        country = Country.objects.get(iso=country_code)
                    except ObjectDoesNotExist:
                        print("Cannot find country identified by code %s" % country_code)
                        continue

                    CultureCode.objects.get_or_create(code=code, language=language, country=country)
                else:
                    try:
                        language = Language.objects.get_by_code(code)
                        country.language_set.add(language)
                    except ObjectDoesNotExist:
                        print("Cannot find language identified by code %s" % code)
                        continue
        else:
            print ("No langauges found for country %s" % country)
