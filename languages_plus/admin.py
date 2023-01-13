from django.contrib import admin

from .models import Language, CultureCode


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        "name_en",
        "name_native",
        "iso_639_1",
        "iso_639_2T",
        "iso_639_2B",
        "iso_639_2T",
        "iso_639_3",
        "notes",
    )
    list_display_links = ("name_en",)
    search_fields = ("name_en", "name_native")


@admin.register(CultureCode)
class CultureCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "language", "country")
    list_display_links = ("code",)
    search_fields = ("code", "language", "country")
