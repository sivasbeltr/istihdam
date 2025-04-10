from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class KullaniciManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError(_("Kullanıcı adı belirtilmelidir"))

        user = self.model(username=username, **extra_fields)
        if email:
            email = self.normalize_email(email)
            user.email = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username, email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Assuming KullaniciTipChoices will be imported in models.py
        # and available to the model where this manager is used
        extra_fields.setdefault("kullanici_tipi", "vatandas")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(username, email, password, **extra_fields)
