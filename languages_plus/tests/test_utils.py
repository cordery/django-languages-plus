from django.test import TestCase
from ..models import CultureCode
from ..utils import associate_countries_and_languages

__author__ = 'luiscberrocal'


class TestAssociation(TestCase):

    def setUp(self):
        associate_countries_and_languages()

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
            #print('%-4s %-20s %s' % (culture_code.code, culture_code.language, culture_code.country))