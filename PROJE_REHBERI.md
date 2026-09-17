# Proje: Yemek Tarifi Defteri
**Canlı Alan Adı:** `yemek.izeluysal.com.tr`

---

## 1. Dağıtım, Barındırma ve Mimari (Deployment)
* **Canlı Adres:** `yemek.izeluysal.com.tr`
* **Çalışma Ortamı:** Docker Konteyner (Docker & Docker Compose).
* **Sunucu Mimarisi:**
  * Uygulama izole bir Docker konteyneri içinde ayağa kalkacak.
  * Önünde Nginx (Ters Proxy) çalışacak ve gelen istekleri `yemek.izeluysal.com.tr` üzerinden konteynerin ilgili portuna yönlendirecek.
  * SSL sertifikası (HTTPS) tanımlı olacak.
* **Açılış/Yönetim:** Geliştirme aşamasında yerel makinede VS Code ve Docker Desktop üzerinden açılacak; canlıya alırken sunucudaki Docker üzerinde `docker compose up -d` ile çalıştırılacak.

---

## 2. Teknoloji Yığını (Tech Stack)
* **Backend:** Python (FastAPI veya Flask - REST API mimarisi).
* **Frontend:** Modern, sade, mobil uyumlu HTML5, TailwindCSS ve Vanilla JavaScript.
* **Veritabanı:** PostgreSQL (Konteyner içinde çalışan, izole ilişkisel veritabanı).
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

### A. Veritabanı Güvenliği (Kritik)
* **Üretimde SQLite yerine PostgreSQL zorunlu olmalı:** Docker içinde SQLite tek dosya yaklaşımı; eşzamanlılık, yedekleme ve veri bütünlüğü açısından canlı trafik için zayıftır.
* **Veritabanı dışa açılmamalı:** PostgreSQL portu (`5432`) host'a publish edilmemeli, sadece Docker internal network üzerinden backend konteyneri erişebilmelidir.
* **Least-privilege kullanıcı modeli:** Uygulama için ayrı bir DB kullanıcısı tanımlanmalı; `SUPERUSER`, `CREATEDB`, `CREATEROLE` yetkileri verilmemelidir.
* **Kimlik bilgisi yönetimi:** DB şifreleri `.env` düz metin yerine Docker secrets veya ortam değişkenleri izolasyonu ile tutulmalıdır.
* **Yedekleme ve geri dönüş planı:** Otomatik günlük yedek, saklama politikası (örn. 7/30 gün) ve point-in-time recovery stratejisi tanımlanmalıdır.
* **Migration disiplini:** Şema değişiklikleri manuel değil Alembic versiyonlu migration ile yönetilmelidir.

### B. Görsel Yükleme Boyut/Format Sınırları (Kritik)
* **Maksimum dosya boyutu sınırı:** Nginx ve uygulama seviyesinde 5 MB/10 MB sınırı uygulanmalıdır.
* **Dosya tür doğrulaması:** Sadece uzantı kontrolü yapılmamalı; MIME type ve magic bytes doğrulaması zorunlu olmalıdır.
* **İzinli format listesi:** Sadece `jpg`, `jpeg`, `png`, `webp` kabul edilmeli; SVG yüklemeleri (XSS riski) tamamen engellenmelidir.
* **Görsel güvenli işleme:** Yüklenen görseller sunucuda Python (Pillow) ile yeniden encode edilip EXIF verileri temizlenmeli, dosya adı UUID ile kaydedilmelidir.
* **Boyut ve optimizasyon:** En fazla 4096x4096 çözünürlük sınırı konulmalı, WebP formatına sıkıştırılarak `uploads/` dizininde saklanmalıdır.
* **Upload klasörü erişim kısıtı:** Yürütülebilir dosya çalıştırma engellenmeli, dizin listeleme (`autoindex`) kapalı olmalıdır.

### C. Nginx SSL ve Proxy Ayarları (Kritik)
* **TLS Hardening:** Sadece TLS 1.2 ve TLS 1.3 açık olmalı, zayıf şifreleme takımları devre dışı bırakılmalıdır.

* **HTTPS Yönlendirme:** Port 80 (HTTP) üzerinden gelen tüm trafik `301 Moved Permanently` ile HTTPS'e yönlendirilmelidir.

* **Güvenlik Başlıkları:** `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` ve uygun bir `Content-Security-Policy` eklenmelidir.
* **Proxy Header Standardı:** `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` başlıkları Nginx tarafından backend'e eksiksiz iletilmelidir.
* **Upload ve Timeout Senkronizasyonu:** `client_max_body_size`, `proxy_read_timeout` ve `proxy_send_timeout` değerleri backend limitleriyle uyumlu yapılandırılmalıdır.
* **Rate Limiting:** Özellikle `/admin` ve dosya yükleme endpoint'leri için Nginx rate limiting uygulanmalıdır.

### D. Güvenlik ve Admin Yetkilendirme (Kritik)
* **Kimlik Doğrulama Standardı:** Admin paneli için güvenli, imzalı Cookie tabanlı Session veya JWT altyapısı kurulmalıdır.
* **Parola Saklama Standardı:** Parolalar veritabanında asla düz metin tutulmamalı; `Argon2id` veya güçlü `bcrypt` ile hash'lenmelidir.
* **Brute-force Koruması:** Başarısız oturum açma denemelerine karşı kilitlenme, gecikme ve IP bazlı istek sınırlaması uygulanmalıdır.
* **Oturum Güvenliği:** Cookie'ler `HttpOnly`, `Secure`, `SameSite=Strict` bayraklarına sahip olmalı ve kısa geçerlilik süresi (TTL) bulunmalıdır.
* **CSRF ve XSS Kontrolleri:** Admin panelinde CSRF token doğrulaması, şablon seviyesinde otomatik escaping uygulanmalıdır.
* **Yetki ve Denetim (Audit):** Kritik admin işlemleri (tarif silme, düzenleme) için zaman damgalı log tutulmalıdır.