from django.apps import AppConfig

from . import APP_NAME


class LanguagesPlusConfig(AppConfig):
    name = APP_NAME

    def ready(self):
        pass
