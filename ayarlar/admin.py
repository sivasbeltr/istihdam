from django.contrib import admin

from .models import Il, Ilce, Mahalle, Meslek, Sektor


@admin.register(Il)
class IlAdmin(admin.ModelAdmin):
    """İl modelinin admin panelinde gösterimi."""

    list_display = ("ad", "slug")
    search_fields = ("ad",)
    prepopulated_fields = {"slug": ("ad",)}


@admin.register(Ilce)
class IlceAdmin(admin.ModelAdmin):
    """İlçe modelinin admin panelinde gösterimi."""

    list_display = ("ad", "il", "slug")
    list_filter = ("il",)
    search_fields = ("ad", "il__ad")
    prepopulated_fields = {"slug": ("ad",)}
    autocomplete_fields = ["il"]


@admin.register(Mahalle)
class MahalleAdmin(admin.ModelAdmin):
    """Mahalle modelinin admin panelinde gösterimi."""

    list_display = ("ad", "ilce", "slug")
    list_filter = ("ilce__il", "ilce")
    search_fields = ("ad", "ilce__ad", "ilce__il__ad")
    prepopulated_fields = {"slug": ("ad",)}
    autocomplete_fields = ["ilce"]


@admin.register(Sektor)
class SektorAdmin(admin.ModelAdmin):
    """Sektör modelinin admin panelinde gösterimi."""

    list_display = ("ad", "slug", "aciklama")
    search_fields = ("ad",)
    prepopulated_fields = {"slug": ("ad",)}


@admin.register(Meslek)
class MeslekAdmin(admin.ModelAdmin):
    """Meslek modelinin admin panelinde gösterimi."""

    list_display = ("ad", "slug", "aciklama")
    search_fields = ("ad",)
    prepopulated_fields = {"slug": ("ad",)}
