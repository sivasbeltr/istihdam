from django.db import models
from django.utils.translation import gettext_lazy as _


class KullaniciTipChoices(models.TextChoices):
    firma = "firma", _("Firma")
    vatandas = "vatandas", _("Vatandaş")
    belediye = "belediye", _("Belediye")


class CinsiyetChoices(models.TextChoices):
    ERKEK = "E", _("Erkek")
    KADIN = "K", _("Kadın")


class EgitimDereceChoices(models.TextChoices):
    ILKOKUL = "ilkokul", _("İlkokul")
    ORTAOKUL = "ortaokul", _("Ortaokul")
    LISE = "lise", _("Lise")
    ONLISANS = "onlisans", _("Önlisans")
    LISANS = "lisans", _("Lisans")
    YUKSEK_LISANS = "yukseklisans", _("Yüksek Lisans")
    DOKTORA = "doktora", _("Doktora")


class YetenekSeviyeChoices(models.TextChoices):
    BASLANGIC = "baslangic", _("Başlangıç")
    ORTA = "orta", _("Orta")
    IYI = "iyi", _("İyi")
    COK_IYI = "cokiyi", _("Çok İyi")
    UZMAN = "uzman", _("Uzman")


class CalismaGunleriChoices(models.TextChoices):
    PAZARTESI = "pazartesi", _("Pazartesi")
    SALI = "sali", _("Salı")
    CARSAMBA = "carsamba", _("Çarşamba")
    PERSEMBE = "persembe", _("Perşembe")
    CUMA = "cuma", _("Cuma")
    CUMARTESI = "cumartesi", _("Cumartesi")
    PAZAR = "pazar", _("Pazar")
