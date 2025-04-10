import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .choices import (
    CalismaGunleriChoices,
    CinsiyetChoices,
    EgitimDereceChoices,
    YetenekSeviyeChoices,
)


class Vatandas(models.Model):
    """
    Gerçek kişi/vatandaş bilgileri modeli.
    Kullanıcıya bağlıdır ve kişisel detaylar içerir.
    """

    kullanici = models.OneToOneField(
        "Kullanici",
        on_delete=models.CASCADE,
        related_name="vatandas_bilgisi",
        verbose_name=_("Kullanıcı"),
        help_text=_("Bu vatandaş profilinin bağlı olduğu kullanıcı hesabı"),
    )

    # Benzersiz tanımlayıcı
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("Vatandaşı benzersiz şekilde tanımlayan UUID"),
    )

    # Kişisel bilgiler
    dogum_tarihi = models.DateField(
        _("Doğum Tarihi"), blank=True, null=True, help_text=_("Vatandaşın doğum tarihi")
    )
    cinsiyet = models.CharField(
        _("Cinsiyet"),
        max_length=1,
        choices=CinsiyetChoices.choices,
        blank=True,
        null=True,
        help_text=_("Vatandaşın cinsiyeti"),
    )
    profil_fotografi = models.ImageField(
        _("Profil Fotoğrafı"),
        upload_to="profil/fotograf/",
        blank=True,
        null=True,
        help_text=_("Vatandaşın profil fotoğrafı"),
    )

    # İletişim bilgileri
    telefon = models.CharField(
        _("Telefon"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("İletişim için telefon numarası"),
    )

    # Konum bilgileri
    il = models.ForeignKey(
        "ayarlar.Il",
        on_delete=models.SET_NULL,
        related_name="vatandaslar",
        verbose_name=_("İl"),
        blank=True,
        null=True,
        help_text=_("Vatandaşın ikamet ettiği il"),
    )
    ilce = models.ForeignKey(
        "ayarlar.Ilce",
        on_delete=models.SET_NULL,
        related_name="vatandaslar",
        verbose_name=_("İlçe"),
        blank=True,
        null=True,
        help_text=_("Vatandaşın ikamet ettiği ilçe"),
    )
    adres = models.TextField(
        _("Adres"), blank=True, null=True, help_text=_("Vatandaşın açık adresi")
    )

    # Özgeçmiş ve tanıtım
    hakkinda = models.TextField(
        _("Hakkında"),
        blank=True,
        null=True,
        help_text=_("Vatandaş hakkında kısa bilgi"),
    )
    ozgecmis_dosya = models.FileField(
        _("Özgeçmiş Dosyası"),
        upload_to="ozgecmis/",
        blank=True,
        null=True,
        help_text=_("Vatandaşın özgeçmiş dosyası (PDF, Word vb.)"),
    )

    # Özel durumlar - ana Kullanici modeline dokunmadan bu bilgileri saklıyoruz
    is_usta = models.BooleanField(
        _("Usta mı?"),
        default=False,
        help_text=_("Vatandaşın usta olarak iş yapıp yapamayacağını belirler"),
    )
    is_is_arayan = models.BooleanField(
        _("İş arıyor mu?"),
        default=False,
        help_text=_("Vatandaşın iş arayıp aramadığını belirler"),
    )

    # Usta bilgileri
    usta_unvani = models.CharField(
        _("Usta Ünvanı"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Usta olarak çalışıyorsa kullandığı ünvan"),
    )
    usta_aciklama = models.TextField(
        _("Usta Açıklaması"),
        blank=True,
        null=True,
        help_text=_("Ustalık hizmetleri hakkında açıklama"),
    )

    # Sosyal medya
    facebook = models.URLField(
        _("Facebook"), blank=True, null=True, help_text=_("Facebook profil adresi")
    )
    twitter = models.URLField(
        _("Twitter"), blank=True, null=True, help_text=_("Twitter profil adresi")
    )
    linkedin = models.URLField(
        _("LinkedIn"), blank=True, null=True, help_text=_("LinkedIn profil adresi")
    )
    instagram = models.URLField(
        _("Instagram"), blank=True, null=True, help_text=_("Instagram profil adresi")
    )

    # Tarihler
    olusturma_tarihi = models.DateTimeField(_("Oluşturulma Tarihi"), auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(_("Güncellenme Tarihi"), auto_now=True)

    class Meta:
        verbose_name = _("Vatandaş")
        verbose_name_plural = _("Vatandaşlar")

    def __str__(self):
        return f"{self.kullanici.get_full_name() or self.kullanici.username}"


class EgitimDurumu(models.Model):
    """
    Vatandaşın eğitim durumu bilgilerini içerir.
    """

    vatandas = models.ForeignKey(
        Vatandas,
        on_delete=models.CASCADE,
        related_name="egitimler",
        verbose_name=_("Vatandaş"),
        help_text=_("Bu eğitim bilgisinin ait olduğu vatandaş"),
    )
    okul_adi = models.CharField(
        _("Okul Adı"), max_length=200, help_text=_("Eğitim alınan kurumun adı")
    )
    bolum = models.CharField(
        _("Bölüm"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("Eğitim alınan bölüm veya alan"),
    )
    derece = models.CharField(
        _("Derece"),
        max_length=20,
        choices=EgitimDereceChoices.choices,
        help_text=_("Eğitimin derecesi veya seviyesi"),
    )
    baslangic_tarihi = models.DateField(
        _("Başlangıç Tarihi"), help_text=_("Eğitime başlama tarihi")
    )
    bitis_tarihi = models.DateField(
        _("Bitiş Tarihi"),
        blank=True,
        null=True,
        help_text=_("Eğitimi bitirme tarihi (halen devam ediyorsa boş bırakın)"),
    )
    devam_ediyor = models.BooleanField(
        _("Devam Ediyor"),
        default=False,
        help_text=_("Eğitim halen devam ediyorsa işaretleyin"),
    )
    aciklama = models.TextField(
        _("Açıklama"), blank=True, null=True, help_text=_("Eğitim hakkında ek bilgiler")
    )

    class Meta:
        verbose_name = _("Eğitim Durumu")
        verbose_name_plural = _("Eğitim Durumları")
        ordering = ["-baslangic_tarihi"]

    def __str__(self):
        return f"{self.okul_adi} - {self.bolum or self.get_derece_display()}"


class IsTecrubesi(models.Model):
    """
    Vatandaşın iş tecrübesi bilgilerini içerir.
    """

    vatandas = models.ForeignKey(
        Vatandas,
        on_delete=models.CASCADE,
        related_name="is_tecrubesi",
        verbose_name=_("Vatandaş"),
        help_text=_("Bu iş tecrübesinin ait olduğu vatandaş"),
    )
    firma_adi = models.CharField(
        _("Firma Adı"), max_length=200, help_text=_("Çalışılan firmanın adı")
    )
    pozisyon = models.CharField(
        _("Pozisyon"), max_length=200, help_text=_("Çalışılan pozisyon veya ünvan")
    )
    baslangic_tarihi = models.DateField(
        _("Başlangıç Tarihi"), help_text=_("İşe başlama tarihi")
    )
    bitis_tarihi = models.DateField(
        _("Bitiş Tarihi"),
        blank=True,
        null=True,
        help_text=_("İşten ayrılma tarihi (halen çalışıyorsa boş bırakın)"),
    )
    calisiyor = models.BooleanField(
        _("Halen Çalışıyor"),
        default=False,
        help_text=_("Bu firmada halen çalışıyorsa işaretleyin"),
    )
    aciklama = models.TextField(
        _("Açıklama"),
        blank=True,
        null=True,
        help_text=_("Yaptığınız işler ve sorumluluklar hakkında bilgi"),
    )
    referans_adi = models.CharField(
        _("Referans Adı"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Referans olarak gösterilebilecek kişinin adı"),
    )
    referans_telefon = models.CharField(
        _("Referans Telefonu"),
        max_length=20,
        blank=True,
        null=True,
        help_text=_("Referans kişinin telefon numarası"),
    )

    class Meta:
        verbose_name = _("İş Tecrübesi")
        verbose_name_plural = _("İş Tecrübeleri")
        ordering = ["-baslangic_tarihi"]

    def __str__(self):
        return f"{self.firma_adi} - {self.pozisyon}"


class Yetenek(models.Model):
    """
    Vatandaşın yeteneklerini içerir.
    """

    vatandas = models.ForeignKey(
        Vatandas,
        on_delete=models.CASCADE,
        related_name="yetenekler",
        verbose_name=_("Vatandaş"),
        help_text=_("Bu yeteneğin ait olduğu vatandaş"),
    )
    yetenek = models.CharField(
        _("Yetenek"), max_length=100, help_text=_("Yetenek, beceri veya uzmanlık alanı")
    )
    seviye = models.PositiveSmallIntegerField(
        _("Seviye"),
        choices=YetenekSeviyeChoices.choices,
        default=YetenekSeviyeChoices.IYI,
        help_text=_("Bu yetenekteki uzmanlık seviyeniz"),
    )

    class Meta:
        verbose_name = _("Yetenek")
        verbose_name_plural = _("Yetenekler")

    def __str__(self):
        return f"{self.yetenek} - {self.get_seviye_display()}"


class Sertifika(models.Model):
    """
    Vatandaşın sertifikalarını içerir.
    """

    vatandas = models.ForeignKey(
        Vatandas,
        on_delete=models.CASCADE,
        related_name="sertifikalar",
        verbose_name=_("Vatandaş"),
        help_text=_("Bu sertifikanın ait olduğu vatandaş"),
    )
    sertifika_adi = models.CharField(
        _("Sertifika Adı"),
        max_length=200,
        help_text=_("Alınan sertifika veya belgenin adı"),
    )
    veren_kurum = models.CharField(
        _("Veren Kurum"),
        max_length=200,
        help_text=_("Sertifikayı veren kurum veya kuruluş"),
    )
    alis_tarihi = models.DateField(
        _("Alış Tarihi"), help_text=_("Sertifikanın alındığı tarih")
    )
    gecerlilik_tarihi = models.DateField(
        _("Geçerlilik Tarihi"),
        blank=True,
        null=True,
        help_text=_("Sertifikanın geçerlilik tarihi (süresiz ise boş bırakın)"),
    )
    sertifika_dosya = models.FileField(
        _("Sertifika Dosyası"),
        upload_to="sertifikalar/",
        blank=True,
        null=True,
        help_text=_("Sertifikanın dijital kopyası"),
    )

    class Meta:
        verbose_name = _("Sertifika")
        verbose_name_plural = _("Sertifikalar")
        ordering = ["-alis_tarihi"]

    def __str__(self):
        return f"{self.sertifika_adi} - {self.veren_kurum}"


class UstalikAlani(models.Model):
    """
    Vatandaşın ustalık alanlarını ve referanslarını içerir.
    """

    vatandas = models.ForeignKey(
        Vatandas,
        on_delete=models.CASCADE,
        related_name="ustalik_alanlari",
        verbose_name=_("Vatandaş"),
        help_text=_("Bu ustalık alanının ait olduğu vatandaş"),
    )
    meslek = models.ForeignKey(
        "ayarlar.Meslek",
        on_delete=models.CASCADE,
        related_name="ustalar",
        verbose_name=_("Meslek"),
        help_text=_("Ustalık yapılan meslek alanı"),
    )
    deneyim_yili = models.PositiveSmallIntegerField(
        _("Deneyim Yılı"), default=0, help_text=_("Bu meslekteki toplam deneyim yılı")
    )
    aciklama = models.TextField(
        _("Açıklama"),
        blank=True,
        null=True,
        help_text=_("Bu meslekteki ustalık hizmetleriniz hakkında bilgi"),
    )
    fiyat_bilgisi = models.CharField(
        _("Fiyat Bilgisi"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Sunulan hizmetin fiyat aralığı veya ücretlendirme bilgisi"),
    )

    class Meta:
        verbose_name = _("Ustalık Alanı")
        verbose_name_plural = _("Ustalık Alanları")
        unique_together = [["vatandas", "meslek"]]

    def __str__(self):
        return f"{self.meslek.ad} ({self.deneyim_yili} yıl)"


class CalismaSaatleri(models.Model):
    """
    Vatandaşın hizmet verebileceği günler ve saatleri içerir.
    Özellikle ustalar için çalışma saatlerini belirlemekte kullanılır.
    """

    vatandas = models.ForeignKey(
        Vatandas,
        on_delete=models.CASCADE,
        related_name="calisma_saatleri",
        verbose_name=_("Vatandaş"),
        help_text=_("Bu çalışma saatlerinin ait olduğu vatandaş"),
    )
    gun = models.CharField(
        _("Gün"),
        max_length=10,
        choices=CalismaGunleriChoices.choices,
        help_text=_("Çalışılabilecek gün"),
    )
    baslangic_saati = models.TimeField(
        _("Başlangıç Saati"), help_text=_("Çalışma başlangıç saati (örn: 09:00)")
    )
    bitis_saati = models.TimeField(
        _("Bitiş Saati"), help_text=_("Çalışma bitiş saati (örn: 18:00)")
    )
    aktif = models.BooleanField(
        _("Aktif"), default=True, help_text=_("Bu günün çalışma programı aktif mi?")
    )

    class Meta:
        verbose_name = _("Çalışma Saati")
        verbose_name_plural = _("Çalışma Saatleri")
        ordering = ["gun", "baslangic_saati"]
        unique_together = [["vatandas", "gun"]]

    def __str__(self):
        return f"{self.get_gun_display()}: {self.baslangic_saati.strftime('%H:%M')} - {self.bitis_saati.strftime('%H:%M')}"
