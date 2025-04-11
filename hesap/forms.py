from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from .models import Kullanici


class KullaniciOlusturmaForm(UserCreationForm):
    """
    Kullanıcı kaydı için form
    """

    email = forms.EmailField(
        required=False,
        label=_("E-posta"),
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Ad"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label=_("Soyad"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Kullanici
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "kullanici_tipi",
            "password1",
            "password2",
        )
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "kullanici_tipi": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control"})
        self.fields["password2"].widget.attrs.update({"class": "form-control"})


class KullaniciDegistirmeForm(UserChangeForm):
    """
    Kullanıcı bilgilerini güncelleme formu
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Kullanici
        fields = ("username", "email", "first_name", "last_name", "kullanici_tipi")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "kullanici_tipi": forms.Select(attrs={"class": "form-control"}),
        }


class KullaniciProfilForm(forms.ModelForm):
    """
    Kullanıcı profil güncelleme formu
    """

    class Meta:
        model = Kullanici
        fields = ("kullanici_tipi", "first_name", "last_name", "email")
        widgets = {
            "kullanici_tipi": forms.Select(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
