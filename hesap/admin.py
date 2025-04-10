from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import KullaniciDegistirmeForm, KullaniciOlusturmaForm
from .models import (
    CalismaSaatleri,
    EgitimDurumu,
    Firma,
    IsTecrubesi,
    Kullanici,
    Sertifika,
    UstalikAlani,
    Vatandas,
    Yetenek,
)


# Inline Models
class EgitimDurumuInline(admin.TabularInline):
    model = EgitimDurumu
    extra = 1
    classes = ["collapse"]
    verbose_name = _("Eğitim Bilgisi")
    verbose_name_plural = _("Eğitim Bilgileri")
    # açıklamayı çıkart
    exclude = ("aciklama",)


class IsTecrubesiInline(admin.TabularInline):
    model = IsTecrubesi
    extra = 1
    classes = ["collapse"]
    verbose_name = _("İş Tecrübesi")
    verbose_name_plural = _("İş Tecrübeleri")


class YetenekInline(admin.TabularInline):
    model = Yetenek
    extra = 1
    classes = ["collapse"]
    verbose_name = _("Yetenek")
    verbose_name_plural = _("Yetenekler")


class SertifikaInline(admin.TabularInline):
    model = Sertifika
    extra = 1
    classes = ["collapse"]
    verbose_name = _("Sertifika")
    verbose_name_plural = _("Sertifikalar")


class UstalikAlaniInline(admin.TabularInline):
    model = UstalikAlani
    extra = 1
    classes = ["collapse"]
    verbose_name = _("Ustalık Alanı")
    verbose_name_plural = _("Ustalık Alanları")


class CalismaSaatleriInline(admin.TabularInline):
    model = CalismaSaatleri
    extra = 7  # Haftanın her günü için bir satır
    classes = ["collapse"]
    verbose_name = _("Çalışma Saati")
    verbose_name_plural = _("Çalışma Saatleri")


# Main models
@admin.register(Vatandas)
class VatandasAdmin(admin.ModelAdmin):
    """Vatandaş modelinin admin panelinde gösterimi."""

    list_display = (
        "get_full_name",
        "kullanici",
        "telefon",
        "il",
        "ilce",
        "is_usta",
        "is_is_arayan",
    )
    list_filter = ("is_usta", "is_is_arayan", "il")
    search_fields = (
        "kullanici__username",
        "kullanici__first_name",
        "kullanici__last_name",
        "telefon",
    )
    readonly_fields = ("olusturma_tarihi", "guncelleme_tarihi", "uuid")

    # Otomatik tamamlama için alanlar
    autocomplete_fields = ["kullanici", "il", "ilce"]

    # Alanların estetik gruplandırılması
    fieldsets = (
        (
            _("Temel Bilgiler"),
            {
                "fields": (
                    "kullanici",
                    "uuid",
                    "dogum_tarihi",
                    "cinsiyet",
                    "profil_fotografi",
                ),
            },
        ),
        (
            _("İletişim Bilgileri"),
            {
                "fields": ("telefon",),
                "classes": ("collapse",),
            },
        ),
        (
            _("Konum Bilgileri"),
            {
                "fields": (
                    "il",
                    "ilce",
                    "adres",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Profil ve Özgeçmiş"),
            {
                "fields": (
                    "hakkinda",
                    "ozgecmis_dosya",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Rol ve Özellikler"),
            {
                "fields": (
                    "is_usta",
                    "usta_unvani",
                    "usta_aciklama",
                    "is_is_arayan",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Sosyal Medya"),
            {
                "fields": (
                    "facebook",
                    "twitter",
                    "linkedin",
                    "instagram",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Tarihler"),
            {
                "fields": (
                    "olusturma_tarihi",
                    "guncelleme_tarihi",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [
        EgitimDurumuInline,
        IsTecrubesiInline,
        YetenekInline,
        SertifikaInline,
        UstalikAlaniInline,
        CalismaSaatleriInline,
    ]

    def get_full_name(self, obj):
        return obj.kullanici.get_full_name() or obj.kullanici.username

    get_full_name.short_description = _("Ad Soyad")
    get_full_name.admin_order_field = "kullanici__first_name"


class KullaniciAdmin(UserAdmin):
    add_form = KullaniciOlusturmaForm
    form = KullaniciDegistirmeForm
    model = Kullanici

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "kullanici_tipi",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "kullanici_tipi",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("User type"), {"fields": ("kullanici_tipi",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined", "created_at", "updated_at")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "kullanici_tipi",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Firma)
class FirmaAdmin(admin.ModelAdmin):
    """Firma modelinin admin panelinde gösterimi."""

    list_display = (
        "ad",
        "kullanici",
        "telefon",
        "il",
        "ilce",
        "aktif",
        "olusturma_tarihi",
    )
    list_filter = ("aktif", "il", "sektorler")
    search_fields = ("ad", "kullanici__username", "email", "telefon", "vergi_no")
    prepopulated_fields = {"slug": ("ad",)}
    date_hierarchy = "olusturma_tarihi"
    readonly_fields = ("olusturma_tarihi", "guncelleme_tarihi")

    # Otomatik tamamlama için alanlar
    autocomplete_fields = ["kullanici", "il", "ilce", "sektorler"]

    # Alanların estetik gruplandırılması
    fieldsets = (
        (
            _("Temel Bilgiler"),
            {
                "fields": (
                    "ad",
                    "slug",
                    "logo",
                    "kullanici",
                    "aciklama",
                ),
            },
        ),
        (
            _("İletişim Bilgileri"),
            {
                "fields": (
                    "email",
                    "telefon",
                    "fax",
                    "web_sitesi",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Konum Bilgileri"),
            {
                "fields": (
                    "il",
                    "ilce",
                    "adres",
                    "posta_kodu",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Sektör ve Diğer Bilgiler"),
            {
                "fields": (
                    "sektorler",
                    "kurulus_yili",
                    "calisan_sayisi",
                    "vergi_dairesi",
                    "vergi_no",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Sosyal Medya"),
            {
                "fields": (
                    "facebook",
                    "twitter",
                    "linkedin",
                    "instagram",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Durum ve Tarihler"),
            {
                "fields": (
                    "aktif",
                    "olusturma_tarihi",
                    "guncelleme_tarihi",
                ),
                "classes": ("collapse",),
            },
        ),
    )


# Remove inline models from admin index
admin.site.register(Kullanici, KullaniciAdmin)

# Don't register these models separately since they're used as inlines
admin.site.empty_value_display = _("Boş")
