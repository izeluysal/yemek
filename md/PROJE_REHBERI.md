# Proje: Yemek Tarifi Defteri
**Canlı Alan Adı:** `yemek.izeluysal.com.tr`

---

## 1. Dağıtım, Barındırma ve Mimari (Deployment)
* **Canlı Alan Adı:** `yemek.izeluysal.com.tr`
* **Geliştirme Ortamı:** Yerel bilgisayarda Python venv içinde.
* **Veritabanı Depolama:** SQLite dosyası (`data/app.db`) yerel klasörde konumlandırılacak.
* **Açılış/Yönetim:** VS Code ve Python venv üzerinden `python application.py` ile çalıştırılacak.

---

## 2. Teknoloji Yığını (Tech Stack)
* **Backend:** Python (FastAPI veya Flask - REST API mimarisi).
* **Frontend:** Modern, sade, mobil uyumlu HTML5, TailwindCSS ve Vanilla JavaScript.
* **Veritabanı:** SQLite 3 (Dosya tabanlı, `data/` klasöründe konumlandırılacak).
* **Görsel/Medya Depolama:** Sunucu üzerinde `uploads/` volume dizini (Docker bind mount).

---

## 3. Veritabanı ve Veri Modeli
Veritabanında tutulacak temel tablolar ve alanlar:

### A. Tarifler Tablosu (Recipes)
* `id`: Benzersiz kimlik
* `title`: Yemek başlığı (Örn: "Zeytinyağlı Biber Dolması")
* `slug`: URL dostu başlık (Örn: `zeytinyagli-biber-dolmasi`)
* `description`: Kısa özet / açıklama
* `ingredients`: Malzeme listesi (Dizi/JSON formatında)
* `instructions`: Adım adım yapılış süreci
* `image_url`: Yemeğin fotoğraf dosya yolu
* `prep_time`: Hazırlama süresi (dakika)
* `cook_time`: Pişirme süresi (dakika)
* `created_at`: Eklenme tarihi/zamanı (Otomatik damga)
* `updated_at`: Güncellenme tarihi

### B. Etiketler Tablosu (Tags)
* `id`: Benzersiz kimlik
* `name`: Etiket adı (Örn: `tuz`, `zeytinyağlı`, `fırın`, `pratik`)
* *İlişki:* Bir tarifin birden fazla etiketi olabilir (Many-to-Many).

---

## 4. Kullanıcı Etkileşimi ve Yorum Politikası
* **Yorum Durumu:** Sitede ziyaretçilerin yorum yazma alanı **OLMAYACAK**.
* **Gerekçe:** Proje kişisel, sade ve reklamsız bir dijital tarif defteri olarak tasarlandığı için harici kullanıcı etkileşimi, spam riskleri ve bildirim altyapısı devre dışı bırakılmıştır.

---

## 5. Ekran Tasarımları ve Sayfa Akışı

### A. Açılış Sayfası (Home Page - `/`)
* **Üst Kısım (Hero):** Minimalist bir arama çubuğu ve popüler etiket filtreleri.
* **Orta Kısım (Grid Vitrin):** 
  * Kartlar halinde en son eklenen tarifler.
  * Her kartta: Yemek fotoğrafı, yemek başlığı, etiketler ve hazırlanma süresi rozeti.
* **Alt Kısım:** Sayfalama veya sade bir alt bilgi (Footer).

### B. Arama ve Filtreleme Sayfası (`/search`)
* **Metin Bazlı Arama:** Yemek başlığında ve tarif açıklamasında eşzamanlı arama (Örn: "makarna").
* **Etiket / Malzeme Filtresi:** Arama kutusuna `tuz` yazıldığında veya "tuz" etiketine tıklandığında içinde o etiket bulunan tüm tarifleri listeleme.
* **Anlık Sonuç:** Filtrelere göre yenilenen dinamik sonuç listesi.

### C. Tarif Detay Sayfası (`/tarif/{slug}`)
* En üstte yüksek çözünürlüklü yatay yemek fotoğrafı.
* Başlık, eklenme tarihi, porsiyon ve süre bilgileri.
* Etiket butonları.
* Yan yana iki sütun: Sol sütunda onay kutucuklu malzemeler listesi, sağ sütunda numaralandırılmış adım adım hazırlanış.

### D. Tarif Yönetim Paneli (Admin - `/admin`)
* Sadece site sahibinin giriş yapabileceği şifreli yönetim alanı.
* Yeni tarif ekleme, fotoğraf yükleme, etiket tanımlama ve var olan tarifleri silme/düzenleme işlevleri.

---

## 6. Teknik Eksikler ve İyileştirmeler

### A. Veritabanı Güvenliği (SQLite)
* **SQLite WAL Modu:** Dosya, WAL (Write-Ahead Logging) modu etkinleştirilip açılmalıdır (`PRAGMA journal_mode=WAL;`), eşzamanlılık ve crash recovery için.
* **Veritabanı Dosya İzinleri:** SQLite dosyası (`data/app.db`) ve ilişkili dosyaları (`data/app.db-wal`, `data/app.db-shm`) sadece uygulama kullanıcısına erişilebilir olmalı (640 permissions).
* **Backup Stratejisi:** Dosya basit şekilde backup alınabilir; otomatik günlük yedekleme cron veya uygulama başlatma sırasında yapılmalı. Minimum 7 günlük saklama.
* **Veritabanı Dosya Lokasyonu:** Üretim ortamında `data/` klasörü ayrı bir volume olarak mount edilmelidir, container yeniden başlatıldığında veri kaybolmaz.
* **Migration Disiplini:** Şema değişiklikleri manuel değil Alembic veya benzer versiyonlu migration tool ile yönetilmelidir.

### B. Görsel Yükleme Boyut/Format Sınırları (Kritik)
* **Maksimum dosya boyutu sınırı:** Nginx ve uygulama seviyesinde 5 MB/10 MB sınırı uygulanmalıdır.
* **Dosya tür doğrulaması:** Sadece uzantı kontrolü yapılmamalı; MIME type ve magic bytes doğrulaması zorunlu olmalıdır.
* **İzinli format listesi:** Sadece `jpg`, `jpeg`, `png`, `webp` kabul edilmeli; SVG yüklemeleri (XSS riski) tamamen engellenmelidir.
* **Görsel güvenli işleme:** Yüklenen görseller sunucuda Python (Pillow) ile yeniden encode edilip EXIF verileri temizlenmeli, dosya adı UUID ile kaydedilmelidir.
* **Boyut ve optimizasyon:** En fazla 4096x4096 çözünürlük sınırı konulmalı, WebP formatına sıkıştırılarak `uploads/` dizininde saklanmalıdır.
* **Upload klasörü erişim kısıtı:** Yürütülebilir dosya çalıştırma engellenmeli, dizin listeleme (`autoindex`) kapalı olmalıdır.

### C. Güvenlik ve Admin Yetkilendirme (Kritik)
* **Kimlik Doğrulama Standardı:** Admin paneli için güvenli, imzalı Cookie tabanlı Session veya JWT altyapısı kurulmalıdır.
* **Parola Saklama Standardı:** Parolalar veritabanında asla düz metin tutulmamalı; `Argon2id` veya güçlü `bcrypt` ile hash'lenmelidir.
* **Brute-force Koruması:** Başarısız oturum açma denemelerine karşı kilitlenme, gecikme ve IP bazlı istek sınırlaması uygulanmalıdır.
* **Oturum Güvenliği:** Cookie'ler `HttpOnly`, `Secure`, `SameSite=Strict` bayraklarına sahip olmalı ve kısa geçerlilik süresi (TTL) bulunmalıdır.
* **CSRF ve XSS Kontrolleri:** Admin panelinde CSRF token doğrulaması, şablon seviyesinde otomatik escaping uygulanmalıdır.
* **Yetki ve Denetim (Audit):** Kritik admin işlemleri (tarif silme, düzenleme) için zaman damgalı log tutulmalıdır.