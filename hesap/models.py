from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from hesap.choices import KullaniciTipChoices

# Vatandas modeli ve ilgili modelleri import et
from .kisi_model import (
    CalismaSaatleri,
    EgitimDurumu,
    IsTecrubesi,
    Sertifika,
    UstalikAlani,
    Vatandas,
    Yetenek,
)
from .managers import KullaniciManager


class Kullanici(AbstractUser):
    """
    Django AbstractUser modelinden türetilen özel Kullanici modeli
    """

    kullanici_tipi = models.CharField(
        max_length=20,
        choices=KullaniciTipChoices.choices,
        default=KullaniciTipChoices.vatandas,
        verbose_name=_("Kullanıcı Tipi"),
    )
    email = models.EmailField(_("email address"), blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Oluşturulma Tarihi")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Güncelleme Tarihi")
    )

    objects = KullaniciManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("Kullanıcı")
        verbose_name_plural = _("Kullanıcılar")

    def __str__(self):
        return f"{self.username} ({self.get_kullanici_tipi_display()})"


class Firma(models.Model):
    """Firma modeli, şirket ve işletme bilgilerini temsil eder."""

    # Temel Bilgiler
    kullanici = models.ForeignKey(
        "Kullanici",
        on_delete=models.SET_NULL,
        related_name="firmalar",
        verbose_name=_("Kullanıcı"),
        blank=True,
        null=True,
    )
    ad = models.CharField(_("Firma Adı"), max_length=200)
    slug = models.SlugField(
        _("Slug"), max_length=255, blank=True, null=True, unique=True
    )
    logo = models.ImageField(_("Logo"), upload_to="firma/logo/", blank=True, null=True)
    aciklama = models.TextField(_("Firma Açıklaması"), blank=True, null=True)

    # İletişim Bilgileri
    email = models.EmailField(_("E-posta"), blank=True, null=True)
    telefon = models.CharField(_("Telefon"), max_length=20, blank=True, null=True)
    fax = models.CharField(_("Fax"), max_length=20, blank=True, null=True)
    web_sitesi = models.URLField(_("Web Sitesi"), blank=True, null=True)

    # Konum Bilgileri
    il = models.ForeignKey(
        "ayarlar.Il",
        on_delete=models.SET_NULL,
        related_name="firmalar",
        verbose_name=_("İl"),
        blank=True,
        null=True,
    )
    ilce = models.ForeignKey(
        "ayarlar.Ilce",
        on_delete=models.SET_NULL,
        related_name="firmalar",
        verbose_name=_("İlçe"),
        blank=True,
        null=True,
    )
    adres = models.TextField(_("Adres"), blank=True, null=True)
    posta_kodu = models.CharField(_("Posta Kodu"), max_length=10, blank=True, null=True)

    # Sektör ve Diğer Bilgiler
    sektorler = models.ManyToManyField(
        "ayarlar.Sektor",
        related_name="firmalar",
        verbose_name=_("Sektörler"),
        blank=True,
    )
    kurulus_yili = models.PositiveIntegerField(_("Kuruluş Yılı"), blank=True, null=True)
    calisan_sayisi = models.PositiveIntegerField(
        _("Çalışan Sayısı"), blank=True, null=True
    )
    vergi_dairesi = models.CharField(
        _("Vergi Dairesi"), max_length=100, blank=True, null=True
    )
    vergi_no = models.CharField(_("Vergi No"), max_length=20, blank=True, null=True)

    # Sosyal Medya
    facebook = models.URLField(_("Facebook"), blank=True, null=True)
    twitter = models.URLField(_("Twitter"), blank=True, null=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True, null=True)
    instagram = models.URLField(_("Instagram"), blank=True, null=True)

    # Durum ve Tarihler
    aktif = models.BooleanField(_("Aktif"), default=True)
    olusturma_tarihi = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)

    class Meta:
        verbose_name = _("Firma")
        verbose_name_plural = _("Firmalar")
        ordering = ["-olusturma_tarihi"]

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        # İl-İlçe-Firma-Ad şeklinde slug oluşturma
        if self.ad and not self.slug:
            firma_slug = slugify(self.ad)

            # İl ve ilçe bilgisi varsa, bunları slug'a ekleyelim
            prefix = ""
            if self.il and self.il.slug:
                prefix = self.il.slug
                if self.ilce and self.ilce.slug and self.ilce.il == self.il:
                    ilce_slug = slugify(self.ilce.ad)  # İlçenin kendi slug'ını kullan
                    prefix = f"{prefix}-{ilce_slug}"

            # Eğer prefix varsa, firma adıyla birleştir
            if prefix:
                self.slug = f"{prefix}-{firma_slug}"
            else:
                self.slug = firma_slug

        super().save(*args, **kwargs)
