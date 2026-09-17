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