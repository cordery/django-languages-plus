import logging

from django.test import TestCase

from languages_plus.models import CultureCode
from languages_plus.utils import associate_countries_and_languages

logger = logging.getLogger(__name__)


class TestAssociation(TestCase):
    fixtures = ['countries_data.json.gz', 'languages_data.json.gz']

    @classmethod
    def setUpTestData(cls):
        associate_countries_and_languages()

    def test_count(self):
        culture_code_count = CultureCode.objects.count()
        self.assertEqual(culture_code_count, 235)

    def test_get_culture_code(self):
        culture_code = CultureCode.objects.get(pk='en-CA')
        self.assertEqual(culture_code.country.name, 'Canada')
        self.assertEqual(culture_code.language.name, 'English')

    def test_get_languages_for_country(self):
        culture_codes = CultureCode.objects.filter(country__name='Canada')
        results = {'en-CA': 'English',
                   'fr-CA': 'French'}
        self.assertEqual(len(results), len(culture_codes))
        for culture_code in culture_codes:
            self.assertEqual(results[culture_code.code], str(culture_code.language))
