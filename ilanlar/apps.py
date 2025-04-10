from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IlanlarConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ilanlar"
    verbose_name = _("İlanlar")
