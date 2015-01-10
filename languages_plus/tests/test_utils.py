from django.test import TestCase
from countries_plus import Country
from ..models import CultureCode
from ..utils import associate_countries_and_languages

__author__ = 'luiscberrocal'

def setUpModule():
    associate_countries_and_languages()

class TestAssociation(TestCase):

    # def setUp(self):
    #     associate_countries_and_languages()

    def test_count(self):
        culture_code_count = CultureCode.objects.all().count()
        self.assertEqual(culture_code_count, 235)

    def test_get_culture_code(self):
        culture_code = CultureCode.objects.get(pk='en-CA')
        self.assertEqual(culture_code.country.name, 'Canada')
        self.assertEqual(culture_code.language.name, 'English')

    def test_get_languages_for_country(self):
        culture_codes = CultureCode.objects.filter(country__name='Canada')
        results = {'en-CA': 'English',
                   'fr-CA':  'French'}
        self.assertEqual(len(results), len(culture_codes))
        for culture_code in culture_codes:
            self.assertEqual(results[culture_code.code], str(culture_code.language))


    def test_get_all_languages(self):
        canada = Country.objects.get(pk='CA')
        languages = canada.get_all_languages()
        results = {'en': 'English',
                   'fr':  'French',
                   'iu': 'Inuktitut'}
        self.assertEqual(len(results), len(languages))
        for language in languages:
            #print('%-4s %-20s' % (language.iso, language.name_en))
            self.assertEqual(results[language.iso], str(language.name_en))