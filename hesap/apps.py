from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class HesapConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hesap"
    verbose_name = _("Hesap Yönetimi")
