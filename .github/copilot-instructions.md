# Sivas Belediyesi İstihdam Ofisi Web Uygulaması - Copilot Talimatları

Bu talimatlar, Sivas Belediyesi İstihdam Ofisi web uygulaması geliştirmesinde tutarlılık sağlamak için GitHub Copilot'a yönergeler sunmaktadır.

## Genel Mimari ve Teknoloji Yığını

- **Backend:** Django, Django Admin
- **Frontend:** Tailwind CSS
- **Tasarım:** Mobil öncelikli (Mobile first), tam duyarlı tasarım
- **Temalar:** Açık/koyu mod desteği

## Backend İlkeleri

### Django Proje Yapısı

Mevcut ana uygulamalar:
- `ayarlar`: Genel sistem ayarları (İl, İlçe, Mahalle, Sektör, Meslek)
- `hesap`: Kullanıcı hesapları (Kullanıcı, Vatandaş, Firma)
- `ilanlar`: İş ilanları yönetimi

### Kullanıcı Türleri ve Erişim Hakları

1. **Firma**
   - Giriş zorunlu
   - `/firma-yonetim/*` altındaki sayfalara erişim

2. **Usta**
   - Giriş zorunlu
   - `/usta-yonetim/*` altındaki sayfalara erişim

3. **Standart Kullanıcı**
   - Giriş zorunlu
   - `/kullanici-yonetim/*` altındaki sayfalara erişim

4. **Ziyaretçiler (Anonim Kullanıcılar)**
   - `/firmalar/**`, `/ustalar/**` ve `/ilanlar/**` sayfalarına erişebilir

### Modeller ve İlişkiler

Modelleri geliştirirken aşağıdaki kuralları takip et:
- Özel model yöneticileri (managers) tanımla
- SlugField'lar için otomatik slug üretimi sağla
- İlişkiler için açık ve anlamlı related_name'ler kullan
- İş ilanları için gerektiğinde çoklu dil desteği ekle

## Frontend İlkeleri

### Tasarım Yönergeleri

- **Renk Şeması:** Sivas Belediyesi kurumsal renkleri kullanılacak
  - Ana renk: #e30613 (Kırmızı)
  - İkincil renk: #004a93 (Lacivert)
  - Vurgu renk: #f7b500 (Sarı/Altın)
  - Metin koyu: #333333
  - Metin açık: #ffffff
  - Arkaplan açık mod: #f8f9fa
  - Arkaplan koyu mod: #121212

- **Tipografi:**
  - Ana başlıklar: Inter veya Poppins, kalın (700)
  - Alt başlıklar: Inter veya Poppins, yarı kalın (600)
  - Metin içeriği: Inter veya Poppins, normal (400)
  - Font boyutları mobil öncelikli ayarlanmalı

- **Bileşenler:**
  - Tüm butonlar, formlar ve kartlar tutarlı tasarıma sahip olmalı
  - Her bileşen hem açık hem de koyu tema için uyumlu olmalı
  - Erişilebilirlik standartlarına uygun olmalı (WCAG 2.1 AA)

### Tailwind CSS Kullanımı

- `tailwind.config.js` dosyasında Sivas Belediyesi renkleri tanımlanmalı
- Varsayılan utility sınıfları yerine tema renkleri kullanılmalı
- Responsive tasarım için Tailwind'in duyarlı öneklerini kullan (sm:, md:, lg:, xl:)
- Koyu/açık mod için Tailwind'in `dark:` önekini kullan

### Mobil Öncelikli Tasarım

- Tüm görünümler önce mobil için tasarlanmalı, ardından büyük ekranlar için genişletilmeli
- Duyarlı grid sistemleri ve esnek kutu modellerini kullan
- Dokunma hedeflerinin minimum 44px x 44px olmasını sağla
- Mobil cihazlarda gereksiz içeriklerin gizlenmesini sağla

## Şablon Yapısı

```
/templates/
  ├── layout.html             # Ana şablon (base template)
  ├── components/             # Yeniden kullanılabilir bileşenler
  │   ├── header.html         # Sayfa başlığı
  │   ├── footer.html         # Sayfa altlığı
  │   ├── sidebar.html        # Kenar çubuğu
  │   ├── navbar.html         # Navigasyon çubuğu
  │   ├── forms/              # Form bileşenleri
  │   └── cards/              # Kart bileşenleri
  ├── pages/                  # Sayfa şablonları
  │   ├── home.html           # Ana sayfa
  │   ├── about.html          # Hakkında sayfası
  │   ├── contact.html        # İletişim sayfası
  │   └── error.html          # Hata sayfası
  ├── firmalar/               # Firma ile ilgili şablonlar
  ├── ustalar/                # Usta ile ilgili şablonlar
  ├── ilanlar/                # İş ilanları ile ilgili şablonlar
  ├── kullanici-yonetim/      # Kullanıcı yönetimi şablonları
  ├── firma-yonetim/          # Firma yönetimi şablonları
  └── usta-yonetim/           # Usta yönetimi şablonları
```

### Şablon Kuralları

- `layout.html` tüm şablonların temelini oluşturur
- Her şablon mümkün olduğunca parçalanmalı ve modüler olmalı
- Şablonlarda Tailwind CSS utility sınıfları kullanılmalı
- HTMX entegrasyonuna hazır olacak şekilde parçalama yapılmalı
- Her şablon için hem açık hem koyu mod desteklenmeli

## URL Yapısı

- `/`: Ana sayfa
- `/hakkimizda/`: Hakkımızda sayfası
- `/iletisim/`: İletişim sayfası

- `/firmalar/`: Firma listesi
- `/firmalar/<slug>/`: Firma detayı
- `/ustalar/`: Usta listesi
- `/ustalar/<slug>/`: Usta detayı
- `/ilanlar/`: İş ilanları listesi
- `/ilanlar/<slug>/`: İş ilanı detayı
- `/ilanlar/<slug>/basvur/`: İş ilanı başvuru formu

- `/hesap/giris/`: Giriş sayfası
- `/hesap/kayit/`: Kayıt sayfası
- `/hesap/sifremi-unuttum/`: Şifremi unuttum sayfası

- `/kullanici-yonetim/`: Kullanıcı yönetim paneli ana sayfası
- `/kullanici-yonetim/profil/`: Kullanıcı profil sayfası
- `/kullanici-yonetim/basvurularim/`: Kullanıcı iş başvuruları

- `/firma-yonetim/`: Firma yönetim paneli ana sayfası
- `/firma-yonetim/profil/`: Firma profil sayfası
- `/firma-yonetim/ilanlar/`: Firma iş ilanları listesi
- `/firma-yonetim/ilanlar/yeni/`: Yeni ilan oluşturma

- `/usta-yonetim/`: Usta yönetim paneli ana sayfası
- `/usta-yonetim/profil/`: Usta profil sayfası
- `/usta-yonetim/hizmetler/`: Usta hizmetleri listesi

## Açık/Koyu Mod Uygulaması

- Sistem ayarlarını takip eden otomatik tema
- Kullanıcı tarafından manuel seçim imkanı
- Kullanıcı tercihi yerel depolamada saklanmalı
- Tailwind'in dark: öneki kullanılmalı
- Tema değiştirme butonu header'da olmalı

## Mobil Uyumluluk

- Tüm görünümler 320px genişliğine kadar düzgün çalışmalı
- Karmaşık tablolar mobil görünümde kartlara dönüşmeli
- Mobilde hamburger menü kullanılmalı
- Dokunma hedefleri yeterince büyük olmalı (min 44px)
- Form elemanları mobil kullanım için optimize edilmeli

## Kod Standartları

- Tüm HTML belgeleri HTML5 standartlarına uygun olmalı
- Progressive enhancement prensibine göre geliştirme yapılmalı
- CSS sınıfları için BEM metodolojisi kullanılmalı
- JavaScript kodları modüllere ayrılmalı
- Erişilebilirlik (a11y) standartlarına uyulmalı
- Semantik HTML etiketleri kullanılmalı

## SEO Optimizasyonu

- Tüm sayfalarda uygun meta etiketleri olmalı
- Semantik heading yapısı kullanılmalı (h1, h2, h3)
- Görsel elementlerde alt öznitelikleri olmalı
- Canonical URL'ler doğru yapılandırılmalı
- Sitemap.xml ve robots.txt dosyaları oluşturulmalı

## Performans İlkeleri

- Görüntüler optimize edilmeli ve responsive olmalı
- Gereksiz JavaScript yükü azaltılmalı
- CSS ve JavaScript dosyaları minify edilmeli
- Font dosyalarının subset'leri kullanılmalı
- İçerik Dağıtım Ağı (CDN) kullanılmalı

## Güvenlik Önlemleri

- CSRF koruması her formda etkinleştirilmeli
- Kullanıcı girişleri valide edilmeli
- XSS saldırılarını önlemek için çıktı escape edilmeli
- Yetkisiz erişimlere karşı view'lar korunmalı
- Django'nun güvenlik ayarları doğru yapılandırılmalı
