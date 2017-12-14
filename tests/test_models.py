from countries_plus.models import Country
from django.test import TestCase

from languages_plus.models import Language, CultureCode
from languages_plus.utils import associate_countries_and_languages


class TestLanguages(TestCase):
    fixtures = ['countries_data.json.gz', 'languages_data.json.gz']

    @classmethod
    def setUpTestData(cls):
        associate_countries_and_languages()

    def test_language_count(self):
        language_count = Language.objects.all().count()
        self.assertEqual(language_count, 184)

    def test_get_language_by_pk(self):
        language = Language.objects.get(pk='en')
        self.assertEqual(language.name_en, 'English')

    def test_get_by_code(self):
        language = Language.objects.get_by_code('iu')
        self.assertEqual(language.name_en, 'Inuktitut')

    def test_language__str__(self):
        language = Language.objects.get(pk='es')
        self.assertEqual(str(language), 'Spanish; Castilian')

    def test_get_culture_pair(self):
        language, country = Language.objects.get_culture_pair('en-CA')
        self.assertEqual(str(language), 'English')
        self.assertEqual(str(country), 'Canada')

    def test_filter_by_codes(self):
        canada = Country.objects.get(name='Canada')
        codes = canada.languages.split(',')
        langs = Language.objects.filter_by_codes(codes)
        self.assertEqual(langs, [Language.objects.get(pk=x.split('-')[0]) for x in codes])
        langs = {x.pk: x for x in langs}
        self.assertEqual(langs['en'].country, canada)
        self.assertEqual(langs['en'].culturecode, 'en-CA')


class TestCultureCode(TestCase):
    fixtures = ['countries_data.json.gz', 'languages_data.json.gz']

    @classmethod
    def setUpTestData(cls):
        associate_countries_and_languages()

    def test_get_as_languages(self):
        languages = CultureCode.objects.filter(pk='en-CA').as_languages()
        self.assertIsInstance(languages[0], Language)
        self.assertEqual(languages[0].country, Country.objects.get(name='Canada'))
        self.assertEqual(languages[0].culturecode, 'en-CA')


class TestCountry(TestCase):
    fixtures = ['countries_data.json.gz', 'languages_data.json.gz']

    @classmethod
    def setUpTestData(cls):
        associate_countries_and_languages()

    def test_primary_language(self):
        uk = Country.objects.get(name='United Kingdom')
        self.assertEqual(uk.primary_language(), Language.objects.get(pk='en'))

    def test_get_all_languages(self):
        canada = Country.objects.get(pk='CA')
        languages = canada.get_all_languages()
        results = {'en': 'English',
                   'fr': 'French',
                   'iu': 'Inuktitut'}
        self.assertEqual(len(results), len(languages))
        for language in languages:
            self.assertEqual(results[language.iso], str(language.name_en))
