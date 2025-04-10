from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Il(models.Model):
    """İl modeli, Türkiye'deki illeri temsil eder."""

    ad = models.CharField(_("İl Adı"), max_length=100)
    slug = models.SlugField(
        _("Slug"), max_length=100, unique=True, blank=True, null=True
    )

    class Meta:
        verbose_name = _("İl")
        verbose_name_plural = _("İller")
        ordering = ["ad"]

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        if self.ad and not self.slug:
            self.slug = slugify(self.ad)
        super().save(*args, **kwargs)


class Ilce(models.Model):
    """İlçe modeli, illere bağlı ilçeleri temsil eder."""

    il = models.ForeignKey(
        Il, on_delete=models.CASCADE, related_name="ilceler", verbose_name=_("İl")
    )
    ad = models.CharField(_("İlçe Adı"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = _("İlçe")
        verbose_name_plural = _("İlçeler")
        ordering = ["ad"]
        unique_together = [["il", "slug"]]

    def __str__(self):
        return f"{self.ad}, {self.il}"

    def save(self, *args, **kwargs):
        # İl-İlçe şeklinde hiyerarşik slug oluştur
        if self.ad and not self.slug and self.il and self.il.slug:
            self.slug = f"{self.il.slug}-{slugify(self.ad)}"
        super().save(*args, **kwargs)


class Mahalle(models.Model):
    """Mahalle modeli, ilçelere bağlı mahalleleri temsil eder."""

    ilce = models.ForeignKey(
        Ilce,
        on_delete=models.CASCADE,
        related_name="mahalleler",
        verbose_name=_("İlçe"),
    )
    ad = models.CharField(_("Mahalle Adı"), max_length=100)
    slug = models.SlugField(_("Slug"), max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _("Mahalle")
        verbose_name_plural = _("Mahalleler")
        ordering = ["ad"]
        unique_together = [["ilce", "slug"]]

    def __str__(self):
        return f"{self.ad}, {self.ilce.ad}, {self.ilce.il}"

    def save(self, *args, **kwargs):
        # İl-İlçe-Mahalle şeklinde hiyerarşik slug oluştur
        if (
            self.ad
            and not self.slug
            and self.ilce
            and self.ilce.il
            and self.ilce.il.slug
        ):
            # Önce ilçe'nin il bilgisini al
            il_slug = self.ilce.il.slug
            ilce_ad_slug = slugify(self.ilce.ad)
            mahalle_ad_slug = slugify(self.ad)
            self.slug = f"{il_slug}-{ilce_ad_slug}-{mahalle_ad_slug}"
        super().save(*args, **kwargs)


class Sektor(models.Model):
    """Sektör modeli, iş sektörlerini temsil eder."""

    ad = models.CharField(_("Sektör Adı"), max_length=100)
    slug = models.SlugField(
        _("Slug"), max_length=200, blank=True, null=True, unique=True
    )
    aciklama = models.TextField(_("Açıklama"), blank=True, null=True)

    class Meta:
        verbose_name = _("Sektör")
        verbose_name_plural = _("Sektörler")
        ordering = ["ad"]

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        if self.ad and not self.slug:
            self.slug = slugify(self.ad)
        super().save(*args, **kwargs)


class Meslek(models.Model):
    """Meslek modeli, iş mesleklerini temsil eder."""

    ad = models.CharField(_("Meslek Adı"), max_length=100)
    slug = models.SlugField(
        _("Slug"), max_length=200, blank=True, null=True, unique=True
    )
    aciklama = models.TextField(_("Açıklama"), blank=True, null=True)

    class Meta:
        verbose_name = _("Meslek")
        verbose_name_plural = _("Meslekler")
        ordering = ["ad"]

    def __str__(self):
        return self.ad

    def save(self, *args, **kwargs):
        if self.ad and not self.slug:
            self.slug = slugify(self.ad)
        super().save(*args, **kwargs)
