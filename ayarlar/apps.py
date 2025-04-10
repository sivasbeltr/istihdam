from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AyarlarConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ayarlar"
    verbose_name = _("Ayarlar-Bilgiler")
