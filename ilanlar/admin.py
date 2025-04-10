from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import (
    BasvuruCevap,
    IlanAnahtar,
    IlanBasvuru,
    IlanDil,
    IlanSonuc,
    IlanSoru,
    IsBilgileri,
)


# Inline Models
class IlanAnahtarInline(admin.TabularInline):
    """İlan anahtar kelimeleri için inline form"""

    model = IlanAnahtar
    extra = 3
    verbose_name = _("Anahtar Kelime")
    verbose_name_plural = _("Anahtar Kelimeler")


class IlanDilInline(admin.TabularInline):
    """İlan dil gereksinimleri için inline form"""

    model = IlanDil
    extra = 1
    verbose_name = _("Dil Şartı")
    verbose_name_plural = _("Dil Şartları")


class IlanSoruInline(admin.StackedInline):
    """İlan soruları için inline form"""

    model = IlanSoru
    extra = 1
    classes = ["collapse"]
    verbose_name = _("Başvuru Sorusu")
    verbose_name_plural = _("Başvuru Soruları")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "soru",
                    "soru_tipi",
                    "zorunlu",
                    "sira",
                )
            },
        ),
        (
            _("Çoktan Seçmeli Ayarları"),
            {
                "fields": ("secenekler",),
                "classes": ("collapse",),
                "description": _(
                    "Çoktan seçmeli sorular için seçenekleri her satıra bir tane olacak şekilde girin."
                ),
            },
        ),
    )


# Başvuru için inline model
class BasvuruCevapInline(admin.TabularInline):
    """Başvuru cevapları için inline form"""

    model = BasvuruCevap
    extra = 0
    readonly_fields = ("soru", "cevap")
    can_delete = False
    verbose_name = _("Cevap")
    verbose_name_plural = _("Cevaplar")


@admin.register(IsBilgileri)
class IsBilgileriAdmin(admin.ModelAdmin):
    """İş ilanı modelinin admin panelinde gösterimi."""

    list_display = (
        "baslik",
        "firma",
        "pozisyon",
        "il",
        "get_durum_badge",
        "basvuru_sayisi",
        "olusturma_tarihi",
    )
    list_filter = (
        "durum",
        "calisma_modeli",
        "calisma_yeri",
        "sektor",
        "il",
        "egitim_duzey",
        "deneyim_duzey",
        "one_cikartilmis",
    )
    search_fields = (
        "baslik",
        "pozisyon",
        "firma__ad",
        "aciklama",
        "gerekli_nitelikler",
    )
    readonly_fields = (
        "basvuru_sayisi",
        "goruntuleme_sayisi",
        "olusturma_tarihi",
        "guncelleme_tarihi",
        "uuid",
    )
    prepopulated_fields = {"slug": ("baslik",)}
    date_hierarchy = "olusturma_tarihi"

    # Otomatik tamamlama için alanlar
    autocomplete_fields = ["firma", "sektor", "il", "ilce"]

    # İnline formlar
    inlines = [IlanAnahtarInline, IlanDilInline, IlanSoruInline]

    # Özelleştirilmiş metotlar
    def get_durum_badge(self, obj):
        """İlan durumunu renkli badge olarak gösterme"""
        colors = {
            "taslak": "secondary",
            "yayinda": "success",
            "durduruldu": "warning",
            "sonlandi": "info",
            "iptal": "danger",
        }
        color = colors.get(obj.durum, "secondary")
        return format_html(
            '<span class="badge badge-{}">{}</span>', color, obj.get_durum_display()
        )

    get_durum_badge.short_description = _("Durum")
    get_durum_badge.admin_order_field = "durum"

    # Fieldset gruplandırması
    fieldsets = (
        (
            _("Temel Bilgiler"),
            {
                "fields": (
                    "baslik",
                    "slug",
                    "firma",
                    "uuid",
                ),
            },
        ),
        (
            _("İş Detayları"),
            {
                "fields": (
                    "pozisyon",
                    "aciklama",
                    "sektor",
                    "departman",
                    "calisma_modeli",
                    "calisma_yeri",
                ),
            },
        ),
        (
            _("Adres Bilgileri"),
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
            _("Aranan Nitelikler"),
            {
                "fields": (
                    "gerekli_nitelikler",
                    "tercih_nitelikleri",
                    "egitim_duzey",
                    "deneyim_duzey",
                ),
            },
        ),
        (
            _("Ücret ve Yan Haklar"),
            {
                "fields": (
                    "maas_bilgisi",
                    "maas_gizli",
                    "yan_haklar",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Başvuru Bilgileri"),
            {
                "fields": (
                    "basvuru_baslangic",
                    "basvuru_bitis",
                    "beklenen_basvuru",
                    "alinacak_kisi",
                ),
            },
        ),
        (
            _("Durum ve İstatistikler"),
            {
                "fields": (
                    "durum",
                    "one_cikartilmis",
                    "basvuru_sayisi",
                    "goruntuleme_sayisi",
                    "yayinlanma_tarihi",
                    "olusturma_tarihi",
                    "guncelleme_tarihi",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # Admin düzenleme formu için talimatlar
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # İl-İlçe ilişkisi için yardım metni
        form.base_fields["ilce"].help_text += " " + _("Lütfen önce il seçiniz.")

        # Diğer yardımcı metinler
        if obj and obj.durum == "taslak":
            form.base_fields["durum"].help_text += " " + _(
                "Yayınlamak için 'Yayında' seçeneğini seçiniz."
            )

        return form

    # İlan durumu değiştiğinde yayınlanma tarihini ayarla
    def save_model(self, request, obj, form, change):
        # Eğer ilan ilk kez yayında durumuna geçiyorsa, yayınlanma tarihini şimdi olarak ayarla
        if (
            change
            and form.cleaned_data.get("durum") == "yayinda"
            and (not obj.yayinlanma_tarihi)
        ):
            from django.utils import timezone

            obj.yayinlanma_tarihi = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(IlanSoru)
class IlanSoruAdmin(admin.ModelAdmin):
    """İlan soruları için ayrı admin görünümü (gerektiğinde)"""

    list_display = ("soru", "ilan", "soru_tipi", "zorunlu", "sira")
    list_filter = ("zorunlu", "soru_tipi", "ilan")
    search_fields = ("soru", "ilan__baslik")
    autocomplete_fields = ["ilan"]

    # Çoktan seçmeli sorular için seçenekler alanının düzenlenmesi
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "ilan",
                    "soru",
                    "soru_tipi",
                    "zorunlu",
                    "sira",
                )
            },
        ),
        (
            _("Çoktan Seçmeli Ayarları"),
            {
                "fields": ("secenekler",),
                "classes": ("collapse",),
                "description": _(
                    "Çoktan seçmeli sorular için seçenekleri her satıra bir tane olacak şekilde girin."
                ),
            },
        ),
    )


@admin.register(IlanBasvuru)
class IlanBasvuruAdmin(admin.ModelAdmin):
    """İş ilanı başvuruları için admin arayüzü."""

    list_display = (
        "vatandas",
        "ilan",
        "get_durum_badge",
        "basvuru_tarihi",
        "okundu",
        "favorilendi",
        "puan",
    )
    list_filter = ("durum", "okundu", "favorilendi", "basvuru_tarihi", "ilan__firma")
    search_fields = (
        "vatandas__kullanici__first_name",
        "vatandas__kullanici__last_name",
        "ilan__baslik",
        "degerlendirme_notu",
    )
    readonly_fields = (
        "basvuru_tarihi",
        "guncelleme_tarihi",
        "son_islem_tarihi",
        "uuid",
    )
    date_hierarchy = "basvuru_tarihi"

    # İnline cevaplar
    inlines = [BasvuruCevapInline]

    # Otomatik tamamlama için alanlar
    autocomplete_fields = ["vatandas", "ilan"]

    # Durumu renkli göster
    def get_durum_badge(self, obj):
        """Başvuru durumunu renkli badge olarak gösterme"""
        colors = {
            "beklemede": "secondary",
            "incelendi": "info",
            "musakat": "primary",
            "red": "danger",
            "kabul": "success",
            "iptal": "warning",
        }
        color = colors.get(obj.durum, "secondary")
        return format_html(
            '<span class="badge badge-{}">{}</span>', color, obj.get_durum_display()
        )

    get_durum_badge.short_description = _("Durum")
    get_durum_badge.admin_order_field = "durum"

    # Alanların gruplandırılması
    fieldsets = (
        (
            _("Temel Bilgiler"),
            {
                "fields": (
                    "ilan",
                    "vatandas",
                    "uuid",
                    "durum",
                ),
            },
        ),
        (
            _("Başvuru İçeriği"),
            {
                "fields": (
                    "on_yazi",
                    "ozgecmis",
                ),
            },
        ),
        (
            _("İşveren Değerlendirmesi"),
            {
                "fields": (
                    "degerlendirme_notu",
                    "puan",
                    "okundu",
                    "favorilendi",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Tarihler ve Takip"),
            {
                "fields": (
                    "basvuru_tarihi",
                    "son_islem_tarihi",
                    "guncelleme_tarihi",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # Durum değişikliğinde son işlem tarihini otomatik güncelle
    def save_model(self, request, obj, form, change):
        if change and "durum" in form.changed_data:
            from django.utils import timezone

            obj.son_islem_tarihi = timezone.now()

        super().save_model(request, obj, form, change)


@admin.register(IlanSonuc)
class IlanSonucAdmin(admin.ModelAdmin):
    """İş ilanı sonuçları için admin arayüzü."""

    list_display = (
        "ilan",
        "tamamlandi",
        "tamamlanma_tarihi",
        "toplam_basvuru",
        "ise_alinan",
    )
    list_filter = ("tamamlandi",)
    search_fields = ("ilan__baslik", "aciklama", "ic_degerlendirme")
    readonly_fields = ("tamamlanma_tarihi", "toplam_basvuru")
    filter_horizontal = ("ise_alinanlar",)

    # Otomatik tamamlama için alanlar
    autocomplete_fields = ["ilan"]

    # Alanların gruplandırılması
    fieldsets = (
        (
            _("İlan Bilgisi"),
            {
                "fields": (
                    "ilan",
                    "tamamlandi",
                    "tamamlanma_tarihi",
                ),
            },
        ),
        (
            _("Sonuç İstatistikleri"),
            {
                "fields": (
                    "toplam_basvuru",
                    "mulakat_yapilan",
                    "ise_alinan",
                ),
            },
        ),
        (
            _("İşe Alınanlar"),
            {
                "fields": ("ise_alinanlar",),
                "description": _(
                    "Bu ilanda işe alınan adayları seçin. Seçilen aday sayısı, işe alınan sayısıyla eşleşmelidir."
                ),
            },
        ),
        (
            _("Değerlendirme"),
            {
                "fields": (
                    "aciklama",
                    "basari_puani",
                    "ic_degerlendirme",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # İlan sonuçları kaydedildiğinde toplam başvuru sayısını güncelle
    def save_model(self, request, obj, form, change):
        # İşe alınanlar ile işe alınan sayısı tutarlılığını kontrol et
        if obj.ise_alinanlar.count() != obj.ise_alinan:
            from django.contrib import messages

            messages.warning(
                request, _("İşe alınan adaylar ile işe alınan sayısı eşleşmiyor!")
            )

        # Toplam başvuru sayısını güncelle
        obj.toplam_basvuru = obj.ilan.basvurular.count()

        super().save_model(request, obj, form, change)


# İlan cevapları için ayrı admin kaydı yapmıyoruz, sadece inline olarak gösteriliyor
admin.site.register(BasvuruCevap)
