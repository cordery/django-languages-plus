from django.test import TestCase
from ..models import Language, CultureCode
from ..utils import associate_countries_and_languages
__author__ = 'luiscberrocal'


class TestLanguages(TestCase):

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




