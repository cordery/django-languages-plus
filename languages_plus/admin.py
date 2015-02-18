from django.contrib import admin

from .models import Language, CultureCode


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_native', 'iso_639_1', 'iso_639_2T', 'iso_639_2B', 'iso_639_2T',
                    'iso_639_3', 'iso_639_6', 'notes')
    list_display_links = ('name_en',)
    search_fields = ('name_en', 'name_native')


class CultureCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'language', 'country')
    list_display_links = ('code',)
    search_fields = ('code', 'language', 'country')

admin.site.register(Language, LanguageAdmin)
admin.site.register(CultureCode, CultureCodeAdmin)
