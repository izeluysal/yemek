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
* **Veritabanı:** PostgreSQL veya SQLite (Konteyner içinde çalışan, ilişkisel veritabanı).
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
* **Least-privilege kullanıcı modeli eksik:** Uygulama için ayrı bir DB kullanıcısı tanımlanmalı; `SUPERUSER`, `CREATEDB`, `CREATEROLE` yetkileri verilmemelidir.
* **Kimlik bilgisi yönetimi eksik:** DB şifreleri `.env` düz metin yerine Docker secrets veya sunucu secret manager ile tutulmalıdır.
* **Yedekleme/geri dönüş planı yok:** Otomatik günlük yedek, saklama politikası (örn. 7/30 gün), periyodik restore testi ve point-in-time recovery stratejisi tanımlanmalıdır.
* **Migration disiplini belirtilmeli:** Şema değişiklikleri manuel değil Alembic benzeri versiyonlu migration ile yönetilmelidir.

### B. Görsel Yükleme Boyut/Format Sınırları (Kritik)
* **Maksimum dosya boyutu tanımsız:** Uygulama ve Nginx seviyesinde net limit konulmalı (örn. `10MB`), aksi halde DoS ve disk şişmesi riski oluşur.
* **Dosya tür doğrulaması eksik:** Sadece uzantı kontrolü yeterli değildir; MIME + magic number doğrulaması zorunlu olmalıdır.
* **İzinli format listesi net olmalı:** `jpg`, `jpeg`, `png`, `webp` gibi beyaz liste uygulanmalı; SVG varsayılan olarak kapatılmalıdır (XSS riski).
* **Görsel güvenli işleme eksik:** Sunucu tarafında yeniden encode edilerek EXIF temizlenmeli, rastgele ad (UUID) ile kaydedilmeli, kullanıcı kaynaklı dosya adı doğrudan kullanılmamalıdır.
* **Boyut ve çözünürlük politikası yok:** Örn. en fazla `4096x4096`, otomatik thumbnail üretimi ve kalite sıkıştırma ile depolama/performans dengesi kurulmalıdır.
* **Upload klasörü için erişim kısıtı eksik:** Yürütülebilir dosya çalıştırma kapatılmalı; dizin gezme (`autoindex`) devre dışı olmalıdır.

### C. Nginx SSL ve Proxy Ayarları (Kritik)
* **TLS hardening detayları eksik:** Sadece TLS 1.2/1.3 açık olmalı, zayıf şifre takımları kapatılmalıdır.
* **HTTP -> HTTPS zorunlu yönlendirme belirtilmeli:** 80 portundan gelen tüm trafik 301 ile HTTPS'e yönlendirilmelidir.
* **HSTS ve temel güvenlik başlıkları yok:** `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, uygun bir `Content-Security-Policy` eklenmelidir.
* **Proxy header standardı eksik:** `Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto` doğru aktarılmalı; backend bu header'lara göre trusted proxy yapılandırması yapmalıdır.
* **Upload ve timeout senkronizasyonu eksik:** `client_max_body_size`, `proxy_read_timeout`, `proxy_send_timeout` değerleri backend limitleri ile uyumlu olmalıdır.
* **Rate limit/WAF katmanı yok:** Özellikle `/admin` ve upload endpointleri için Nginx rate limit ve mümkünse fail2ban/WAF katmanı tanımlanmalıdır.

### D. Güvenlik ve Admin Yetkilendirme (Kritik)
* **"Şifreli alan" ifadesi yetersiz:** Kimlik doğrulama yöntemi netleşmeli (session-cookie veya JWT), üretim için güvenli varsayılanlar belirlenmelidir.
* **Parola saklama standardı belirtilmeli:** Parolalar `Argon2id` (tercihen) veya güçlü `bcrypt` ile hashlenmeli; düz metin/asla geri çözülebilir format kullanılmamalıdır.
* **Brute-force koruması eksik:** Başarısız giriş deneme limiti, artan gecikme, geçici kilit ve IP bazlı rate limit uygulanmalıdır.
* **Oturum güvenliği eksik:** Cookie kullanılıyorsa `HttpOnly`, `Secure`, `SameSite=Strict/Lax`, kısa TTL ve düzenli session rotation zorunlu olmalıdır.
* **CSRF/XSS kontrolleri belirtilmeli:** Admin panelinde CSRF token, output escaping ve input validation katmanları zorunlu olmalıdır.
* **Yetki ve izleme eksik:** Tek rol olsa bile açık RBAC tanımı, kritik işlem audit log'u (kim, ne zaman, neyi değiştirdi) ve alarm mekanizması eklenmelidir.
* **Ek sertleştirme önerisi:** Mümkünse admin girişinde 2FA ve/veya IP allowlist uygulanmalıdır.