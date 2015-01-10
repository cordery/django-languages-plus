from django.test import TestCase
from ..models import Language
__author__ = 'luiscberrocal'


class TestLanguages(TestCase):

    def test_language_count(self):
        language_count = Language.objects.all().count()
        self.assertEqual(language_count, 184)

    def test_get_languages(self):
        english = Language.objects.get(pk='en')
        self.assertEqual(english.name, 'English')


