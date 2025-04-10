import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CalismaModeliChoices(models.TextChoices):
    """İş ilanı çalışma modeli seçenekleri"""

    TAM_ZAMANLI = "tam_zamanli", _("Tam Zamanlı")
    YARI_ZAMANLI = "yari_zamanli", _("Yarı Zamanlı")
    PROJE_BAZLI = "proje_bazli", _("Proje Bazlı")
    STAJYER = "stajyer", _("Stajyer")
    GUNLUK = "gunluk", _("Günlük")
    DONUSUMLU = "donusumlu", _("Dönüşümlü")


class CalismaYeriChoices(models.TextChoices):
    """İş ilanı çalışma yeri seçenekleri"""

    OFISTE = "ofiste", _("Ofiste")
    UZAKTAN = "uzaktan", _("Uzaktan")
    HIBRIT = "hibrit", _("Hibrit")


class EgitimDuzeyiChoices(models.TextChoices):
    """İş ilanı için gerekli eğitim düzeyi seçenekleri"""

    ILKOKUL = "ilkokul", _("İlkokul")
    ORTAOKUL = "ortaokul", _("Ortaokul")
    LISE = "lise", _("Lise")
    ONLISANS = "onlisans", _("Önlisans")
    LISANS = "lisans", _("Lisans")
    YUKSEK_LISANS = "yuksek_lisans", _("Yüksek Lisans")
    DOKTORA = "doktora", _("Doktora")
    FARKETMEZ = "farketmez", _("Farketmez")


class DeneyimDuzeyiChoices(models.TextChoices):
    """İş ilanı için gerekli deneyim düzeyi seçenekleri"""

    DENEYIMSIZ = "deneyimsiz", _("Deneyimsiz")
    STAJYER = "stajyer", _("Stajyer")
    AZ_TECRUBELI = "az_tecrubeli", _("Az Tecrübeli (0-2 Yıl)")
    ORTA_TECRUBELI = "orta_tecrubeli", _("Orta Tecrübeli (2-5 Yıl)")
    TECRUBELI = "tecrubeli", _("Tecrübeli (5-10 Yıl)")
    UZMAN = "uzman", _("Uzman (10+ Yıl)")
    FARKETMEZ = "farketmez", _("Farketmez")


class IlanDurumChoices(models.TextChoices):
    """İş ilanının durum seçenekleri"""

    TASLAK = "taslak", _("Taslak")
    YAYINDA = "yayinda", _("Yayında")
    DURDURULDU = "durduruldu", _("Durduruldu")
    SONLANDI = "sonlandi", _("Sonlandırıldı")
    IPTAL = "iptal", _("İptal Edildi")


class IsBilgileri(models.Model):
    """
    İş İlanı modeli, firmaların yayınladığı iş ilanlarını içerir.
    """

    # Temel Bilgiler
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("İlanı benzersiz şekilde tanımlayan UUID"),
    )
    baslik = models.CharField(
        _("İlan Başlığı"), max_length=200, help_text=_("İş ilanının başlığı")
    )
    slug = models.SlugField(
        _("Slug"),
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text=_("İlanın URL'de kullanılacak kısa adı"),
    )
    firma = models.ForeignKey(
        "hesap.Firma",
        on_delete=models.CASCADE,
        related_name="is_ilanlari",
        verbose_name=_("Firma"),
        help_text=_("İlanı yayınlayan firma"),
    )

    # İş Detayları
    pozisyon = models.CharField(
        _("Pozisyon"), max_length=100, help_text=_("İş pozisyonu/ünvanı")
    )
    aciklama = models.TextField(
        _("İş Açıklaması"), help_text=_("İş hakkında detaylı açıklama")
    )
    sektor = models.ForeignKey(
        "ayarlar.Sektor",
        on_delete=models.SET_NULL,
        related_name="is_ilanlari",
        verbose_name=_("Sektör"),
        null=True,
        blank=True,
        help_text=_("İlanın ilgili olduğu sektör"),
    )
    departman = models.CharField(
        _("Departman"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("İşin hangi departmanda olduğu"),
    )
    calisma_modeli = models.CharField(
        _("Çalışma Modeli"),
        max_length=20,
        choices=CalismaModeliChoices.choices,
        default=CalismaModeliChoices.TAM_ZAMANLI,
        help_text=_("İşin çalışma şekli (tam zamanlı, yarı zamanlı vb.)"),
    )
    calisma_yeri = models.CharField(
        _("Çalışma Yeri"),
        max_length=20,
        choices=CalismaYeriChoices.choices,
        default=CalismaYeriChoices.OFISTE,
        help_text=_("İşin yapılacağı yer (ofiste, uzaktan vb.)"),
    )

    # Konum Bilgileri
    il = models.ForeignKey(
        "ayarlar.Il",
        on_delete=models.SET_NULL,
        related_name="is_ilanlari",
        verbose_name=_("İl"),
        null=True,
        blank=True,
        help_text=_("İşin yapılacağı il"),
    )
    ilce = models.ForeignKey(
        "ayarlar.Ilce",
        on_delete=models.SET_NULL,
        related_name="is_ilanlari",
        verbose_name=_("İlçe"),
        null=True,
        blank=True,
        help_text=_("İşin yapılacağı ilçe"),
    )
    adres = models.TextField(
        _("Adres"), blank=True, null=True, help_text=_("İş yerinin açık adresi")
    )

    # Aranan Nitelikler
    gerekli_nitelikler = models.TextField(
        _("Gerekli Nitelikler"), help_text=_("Adayda bulunması gereken nitelikler")
    )
    tercih_nitelikleri = models.TextField(
        _("Tercih Nedeni Nitelikler"),
        blank=True,
        null=True,
        help_text=_("Adayda bulunması tercih edilen ancak zorunlu olmayan nitelikler"),
    )
    egitim_duzey = models.CharField(
        _("Eğitim Düzeyi"),
        max_length=20,
        choices=EgitimDuzeyiChoices.choices,
        default=EgitimDuzeyiChoices.FARKETMEZ,
        help_text=_("Aranan minimum eğitim düzeyi"),
    )
    deneyim_duzey = models.CharField(
        _("Deneyim Düzeyi"),
        max_length=20,
        choices=DeneyimDuzeyiChoices.choices,
        default=DeneyimDuzeyiChoices.FARKETMEZ,
        help_text=_("Aranan deneyim düzeyi"),
    )

    # Ücret ve Yan Haklar
    maas_bilgisi = models.CharField(
        _("Maaş Bilgisi"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Maaş aralığı veya bilgisi (ör: 10.000TL-15.000TL)"),
    )
    maas_gizli = models.BooleanField(
        _("Maaş Bilgisi Gizli"),
        default=True,
        help_text=_("Maaş bilgisinin ilanda gizlenmesi"),
    )
    yan_haklar = models.TextField(
        _("Yan Haklar"),
        blank=True,
        null=True,
        help_text=_("Sunulan yan haklar (yemek, servis, sağlık sigortası vb.)"),
    )

    # Başvuru Bilgileri
    basvuru_baslangic = models.DateField(
        _("Başvuru Başlangıç Tarihi"),
        help_text=_("Başvuruların kabul edilmeye başlanacağı tarih"),
    )
    basvuru_bitis = models.DateField(
        _("Son Başvuru Tarihi"),
        blank=True,
        null=True,
        help_text=_("Başvuruların kabul edileceği son tarih (boş ise süresiz)"),
    )
    beklenen_basvuru = models.PositiveIntegerField(
        _("Beklenen Başvuru Sayısı"),
        blank=True,
        null=True,
        help_text=_("Beklenen yaklaşık başvuru sayısı"),
    )
    alinacak_kisi = models.PositiveIntegerField(
        _("Alınacak Kişi Sayısı"), default=1, help_text=_("Alınacak kişi sayısı")
    )

    # Durum ve İstatistikler
    durum = models.CharField(
        _("İlan Durumu"),
        max_length=20,
        choices=IlanDurumChoices.choices,
        default=IlanDurumChoices.TASLAK,
        help_text=_("İlanın mevcut durumu"),
    )
    one_cikartilmis = models.BooleanField(
        _("Öne Çıkartılmış"),
        default=False,
        help_text=_("İlanın öne çıkartılmış olup olmadığı"),
    )
    basvuru_sayisi = models.PositiveIntegerField(
        _("Başvuru Sayısı"), default=0, help_text=_("İlana yapılan başvuru sayısı")
    )
    goruntuleme_sayisi = models.PositiveIntegerField(
        _("Görüntülenme Sayısı"), default=0, help_text=_("İlanın görüntülenme sayısı")
    )

    # Tarihler
    olusturma_tarihi = models.DateTimeField(
        _("Oluşturulma Tarihi"),
        auto_now_add=True,
        help_text=_("İlanın oluşturulduğu tarih"),
    )
    guncelleme_tarihi = models.DateTimeField(
        _("Güncellenme Tarihi"),
        auto_now=True,
        help_text=_("İlanın son güncellendiği tarih"),
    )
    yayinlanma_tarihi = models.DateTimeField(
        _("Yayınlanma Tarihi"),
        blank=True,
        null=True,
        help_text=_("İlanın yayınlandığı tarih"),
    )

    class Meta:
        verbose_name = _("İş İlanı")
        verbose_name_plural = _("İş İlanları")
        ordering = ["-olusturma_tarihi"]

    def __str__(self):
        return f"{self.baslik} - {self.firma.ad}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.baslik)
        super().save(*args, **kwargs)


class IlanAnahtar(models.Model):
    """
    İş ilanları için anahtar kelimeler.
    """

    ilan = models.ForeignKey(
        IsBilgileri,
        on_delete=models.CASCADE,
        related_name="anahtar_kelimeler",
        verbose_name=_("İş İlanı"),
        help_text=_("Bu anahtar kelimenin bağlı olduğu ilan"),
    )
    anahtar_kelime = models.CharField(
        _("Anahtar Kelime"), max_length=50, help_text=_("İlanla ilgili anahtar kelime")
    )

    class Meta:
        verbose_name = _("İlan Anahtar Kelime")
        verbose_name_plural = _("İlan Anahtar Kelimeler")
        unique_together = [["ilan", "anahtar_kelime"]]

    def __str__(self):
        return self.anahtar_kelime


class IlanDil(models.Model):
    """
    İş ilanı için istenen dil bilgisi.
    """

    class DilSeviyeChoices(models.TextChoices):
        BASLANGIC = "baslangic", _("Başlangıç")
        ORTA = "orta", _("Orta")
        IYI = "iyi", _("İyi")
        COK_IYI = "cok_iyi", _("Çok İyi")
        ILERI = "ileri", _("İleri")
        ANADIL = "anadil", _("Anadil")

    ilan = models.ForeignKey(
        IsBilgileri,
        on_delete=models.CASCADE,
        related_name="istenen_diller",
        verbose_name=_("İş İlanı"),
        help_text=_("Bu dil şartının bağlı olduğu ilan"),
    )
    dil = models.CharField(_("Dil"), max_length=50, help_text=_("İstenen dil"))
    seviye = models.CharField(
        _("Seviye"),
        max_length=10,
        choices=DilSeviyeChoices.choices,
        default=DilSeviyeChoices.ORTA,
        help_text=_("İstenen dil seviyesi"),
    )
    zorunlu = models.BooleanField(
        _("Zorunlu"), default=True, help_text=_("Bu dilin zorunlu olup olmadığı")
    )

    class Meta:
        verbose_name = _("İlan Dil Şartı")
        verbose_name_plural = _("İlan Dil Şartları")
        unique_together = [["ilan", "dil"]]

    def __str__(self):
        return f"{self.dil} - {self.get_seviye_display()}"


class IlanSoru(models.Model):
    """
    İş ilanına başvuru sırasında sorulacak sorular.
    """

    class SoruTipiChoices(models.TextChoices):
        METIN = "metin", _("Metin")
        COKTAN_SECMELI = "coktan_secmeli", _("Çoktan Seçmeli")
        EVET_HAYIR = "evet_hayir", _("Evet/Hayır")

    ilan = models.ForeignKey(
        IsBilgileri,
        on_delete=models.CASCADE,
        related_name="sorular",
        verbose_name=_("İş İlanı"),
        help_text=_("Bu sorunun bağlı olduğu ilan"),
    )
    soru = models.CharField(
        _("Soru"), max_length=255, help_text=_("Başvuru sırasında sorulacak soru")
    )
    soru_tipi = models.CharField(
        _("Soru Tipi"),
        max_length=20,
        choices=SoruTipiChoices.choices,
        default=SoruTipiChoices.METIN,
        help_text=_("Sorunun cevap tipi"),
    )
    secenekler = models.TextField(
        _("Seçenekler"),
        blank=True,
        null=True,
        help_text=_("Çoktan seçmeli soru için seçenekler (her satıra bir seçenek)"),
    )
    zorunlu = models.BooleanField(
        _("Zorunlu"),
        default=True,
        help_text=_("Bu soruya cevap verilmesinin zorunlu olup olmadığı"),
    )
    sira = models.PositiveSmallIntegerField(
        _("Sıra"), default=0, help_text=_("Sorunun görüntülenme sırası")
    )

    class Meta:
        verbose_name = _("İlan Soru")
        verbose_name_plural = _("İlan Soruları")
        ordering = ["sira"]

    def __str__(self):
        return self.soru


class BasvuruDurumChoices(models.TextChoices):
    """Başvuru durumu seçenekleri"""

    BEKLEMEDE = "beklemede", _("Beklemede")
    INCELENDI = "incelendi", _("İncelendi")
    MUSAKAT = "musakat", _("Mülakata Çağrıldı")
    RED = "red", _("Reddedildi")
    KABUL = "kabul", _("Kabul Edildi")
    IPTAL = "iptal", _("İptal Edildi")


class IlanBasvuru(models.Model):
    """
    İş ilanlarına yapılan başvuruları içeren model
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("Başvuruyu benzersiz şekilde tanımlayan UUID"),
    )
    ilan = models.ForeignKey(
        IsBilgileri,
        on_delete=models.CASCADE,
        related_name="basvurular",
        verbose_name=_("İş İlanı"),
        help_text=_("Başvuru yapılan iş ilanı"),
    )
    vatandas = models.ForeignKey(
        "hesap.Vatandas",
        on_delete=models.CASCADE,
        related_name="is_basvurulari",
        verbose_name=_("Başvuran"),
        help_text=_("İş ilanına başvuran kişi"),
    )
    ozgecmis = models.FileField(
        _("Özgeçmiş"),
        upload_to="basvurular/ozgecmis/",
        blank=True,
        null=True,
        help_text=_("Başvuru için yüklenen özgeçmiş dosyası"),
    )
    on_yazi = models.TextField(
        _("Ön Yazı"),
        blank=True,
        null=True,
        help_text=_("Başvuru için yazılan tanıtım/motivasyon yazısı"),
    )
    durum = models.CharField(
        _("Durum"),
        max_length=15,
        choices=BasvuruDurumChoices.choices,
        default=BasvuruDurumChoices.BEKLEMEDE,
        help_text=_("Başvurunun mevcut durumu"),
    )

    # İşveren Değerlendirme Bilgileri
    degerlendirme_notu = models.TextField(
        _("Değerlendirme Notu"),
        blank=True,
        null=True,
        help_text=_("İşverenin başvuru hakkındaki değerlendirme notu"),
    )
    puan = models.PositiveSmallIntegerField(
        _("Puan"),
        blank=True,
        null=True,
        help_text=_("Başvuruya verilen puan (1-10 arası)"),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    # Takip Bilgileri
    basvuru_tarihi = models.DateTimeField(
        _("Başvuru Tarihi"),
        auto_now_add=True,
        help_text=_("Başvurunun yapıldığı tarih"),
    )
    guncelleme_tarihi = models.DateTimeField(
        _("Güncelleme Tarihi"),
        auto_now=True,
        help_text=_("Başvurunun son güncellenme tarihi"),
    )
    son_islem_tarihi = models.DateTimeField(
        _("Son İşlem Tarihi"),
        blank=True,
        null=True,
        help_text=_(
            "Başvuru üzerinde yapılan son işlemin tarihi (durum değişikliği vb.)"
        ),
    )

    # Öne Çıkan ve Özel Alanlar
    okundu = models.BooleanField(
        _("Okundu"),
        default=False,
        help_text=_("Başvurunun işveren tarafından okunup okunmadığı"),
    )
    favorilendi = models.BooleanField(
        _("Favorilendi"),
        default=False,
        help_text=_("Başvurunun işveren tarafından favorilere eklenip eklenmediği"),
    )

    class Meta:
        verbose_name = _("İlan Başvuru")
        verbose_name_plural = _("İlan Başvuruları")
        ordering = ["-basvuru_tarihi"]
        unique_together = [["ilan", "vatandas"]]

    def __str__(self):
        return f"{self.vatandas} - {self.ilan.baslik}"

    def save(self, *args, **kwargs):
        # Durum değişikliğinde son işlem tarihini güncelle
        if self.pk:
            old_instance = IlanBasvuru.objects.get(pk=self.pk)
            if old_instance.durum != self.durum:
                from django.utils import timezone

                self.son_islem_tarihi = timezone.now()

        super().save(*args, **kwargs)


class BasvuruCevap(models.Model):
    """
    Başvuru sırasında sorulan sorulara verilen cevapları içeren model
    """

    basvuru = models.ForeignKey(
        IlanBasvuru,
        on_delete=models.CASCADE,
        related_name="cevaplar",
        verbose_name=_("Başvuru"),
        help_text=_("Bu cevabın ait olduğu başvuru"),
    )
    soru = models.ForeignKey(
        IlanSoru,
        on_delete=models.CASCADE,
        related_name="cevaplar",
        verbose_name=_("Soru"),
        help_text=_("Cevaplanan soru"),
    )
    cevap = models.TextField(_("Cevap"), help_text=_("Soruya verilen cevap"))

    class Meta:
        verbose_name = _("Başvuru Cevabı")
        verbose_name_plural = _("Başvuru Cevapları")
        unique_together = [["basvuru", "soru"]]

    def __str__(self):
        return f"{self.soru} - {self.basvuru}"


class IlanSonuc(models.Model):
    """
    İş ilanı sonuçlarını ve sürecin tamamlanma detaylarını içeren model
    """

    ilan = models.OneToOneField(
        IsBilgileri,
        on_delete=models.CASCADE,
        related_name="sonuc",
        verbose_name=_("İş İlanı"),
        help_text=_("Sonucun ait olduğu iş ilanı"),
    )

    # Tamamlanma Bilgileri
    tamamlandi = models.BooleanField(
        _("Tamamlandı"),
        default=False,
        help_text=_("İş ilanı sürecinin tamamlanıp tamamlanmadığı"),
    )
    tamamlanma_tarihi = models.DateTimeField(
        _("Tamamlanma Tarihi"),
        blank=True,
        null=True,
        help_text=_("İş ilanı sürecinin tamamlandığı tarih"),
    )

    # İstatistikler
    toplam_basvuru = models.PositiveIntegerField(
        _("Toplam Başvuru"), default=0, help_text=_("Alınan toplam başvuru sayısı")
    )
    mulakat_yapilan = models.PositiveIntegerField(
        _("Mülakat Yapılan"), default=0, help_text=_("Mülakat yapılan aday sayısı")
    )
    ise_alinan = models.PositiveIntegerField(
        _("İşe Alınan"), default=0, help_text=_("İşe alınan kişi sayısı")
    )

    # Sonuç Değerlendirme
    aciklama = models.TextField(
        _("Açıklama"),
        blank=True,
        null=True,
        help_text=_("İlan sonucu hakkında genel açıklama"),
    )

    # İşe alınan kişiler (çoklu seçim)
    ise_alinanlar = models.ManyToManyField(
        IlanBasvuru,
        related_name="ise_alinan_ilanlar",
        verbose_name=_("İşe Alınanlar"),
        blank=True,
        help_text=_("Bu ilanda işe alınan kişiler"),
    )

    # İç değerlendirme
    basari_puani = models.PositiveSmallIntegerField(
        _("Başarı Puanı"),
        blank=True,
        null=True,
        help_text=_("İş ilanı sürecinin başarı puanı (1-10)"),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    ic_degerlendirme = models.TextField(
        _("İç Değerlendirme"),
        blank=True,
        null=True,
        help_text=_("İlan süreci hakkında firma içi değerlendirme notları"),
    )

    class Meta:
        verbose_name = _("İlan Sonucu")
        verbose_name_plural = _("İlan Sonuçları")

    def __str__(self):
        return f"{self.ilan.baslik} - {'Tamamlandı' if self.tamamlandi else 'Devam Ediyor'}"

    def save(self, *args, **kwargs):
        # İlan tamamlandıysa ve tarih yoksa, tarihi otomatik ayarla
        if self.tamamlandi and not self.tamamlanma_tarihi:
            from django.utils import timezone

            self.tamamlanma_tarihi = timezone.now()

        # İlan tamamlandıysa, ilgili ilanın durumunu "sonlandi" olarak ayarla
        if self.tamamlandi and hasattr(self, "ilan"):
            self.ilan.durum = "sonlandi"
            self.ilan.save()

        super().save(*args, **kwargs)
