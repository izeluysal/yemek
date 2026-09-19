# Yemek Tarifi Defteri - Kurulum ve Çalıştırma Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler
- **Python:** 3.9+ (Test edilmiş: Python 3.11.9)
- **İşletim Sistemi:** Windows / macOS / Linux
- **Git:** Versiyon kontrolü için

### 2. Projeyi Clone Et
```bash
git clone https://github.com/izeluysal/yemek-tarifi-defteri.git
cd yemek-tarifi-defteri
```

### 3. Sanal Ortam Oluştur
**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 5. Uygulamayı Çalıştır
```bash
python application.py
```

**Çıktı:**
```
 * Running on http://127.0.0.1:5000
```

### 6. Tarayıcıda Aç
- **Anasayfa:** http://127.0.0.1:5000/
- **Admin Paneli:** http://127.0.0.1:5000/admin/login
- **Admin Şifresi:** `admin123`

---

## 📁 Dosya Yapısı

```
yemek-tarifi-defteri/
├── application.py          # Flask ana uygulaması
├── config.py              # Konfigürasyon (hardcoded settings)
├── models.py              # SQLAlchemy ORM modelleri
├── requirements.txt       # Python bağımlılıkları
├── test_setup.py          # Setup test scripti
├── .gitignore             # Git ignore kuralları
│
├── data/
│   └── app.db             # SQLite veritabanı (otomatik oluşturulur)
│
├── uploads/               # Yüklenen tarifler görselleri
│   └── (recipe images)
│
├── templates/             # HTML şablonları (Jinja2)
│   ├── base.html          # Temel şablon (navbar, footer)
│   ├── index.html         # Anasayfa (tarifler grid)
│   ├── recipe_detail.html # Tarif detay sayfası
│   ├── search.html        # Arama ve filtreleme
│   ├── admin_login.html   # Admin giriş formu
│   └── admin/
│       ├── panel.html     # Admin dashboard
│       └── recipe_form.html # Tarif ekleme/düzenleme formu
│
└── md/
    ├── PROJE_REHBERI.md   # Proje belgelendirmesi
    └── SETUP.md           # Bu dosya
```

---

## ⚙️ Konfigürasyon

### config.py
Tüm ayarlar `config.py` dosyasında hardcoded olarak tanımlanmıştır:

```python
# Admin Şifresi
ADMIN_PASSWORD = 'admin123'

# Veritabanı
SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/proje/yemek-tarifi-defteri/data/app.db'

# Dosya Yükleme
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB max

# İzinli Dosya Türleri
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
```

**Not:** Production ortamında bu ayarları environment variables'a taşıyın.

---

## 🗂️ Teknoloji Stack

| Bileşen | Teknoloji | Versiyon |
|---------|-----------|---------|
| **Backend Framework** | Flask | 3.0.0 |
| **ORM / Database** | SQLAlchemy + Flask-SQLAlchemy | 2.0.23 / 3.1.1 |
| **Veritabanı** | SQLite 3 | (file-based) |
| **Frontend CSS** | Bootstrap | 5.3.0 (CDN) |
| **Frontend JS** | Vanilla JavaScript | - |
| **Görsel İşleme** | Pillow | 10.1.0 |
| **Web Server (Dev)** | Werkzeug | 3.0.1 |
| **Tarih Kütüphanesi** | python-dateutil | 2.8.2 |

---

## 🧪 Setup Testi

Uygulamanın düzgün kurulduğunu kontrol etmek için:

```bash
python test_setup.py
```

**Beklenen Çıktı:**
```
✓ Uygulama başarıyla yüklendi
✓ Veritabanı: sqlite:///C:/proje/yemek-tarifi-defteri/data/app.db
✓ Admin Şifresi: admin123
✓ Upload Klasörü: uploads
✓ Host: 127.0.0.1
✓ Port: 5000
```

---

## 🎯 İlk Adımlar

### Admin Paneline Gir
1. http://127.0.0.1:5000/admin/login
2. Şifre: `admin123`
3. **Giriş Yap** tuşuna tıkla

### İlk Tarifi Ekle
1. Admin panelinde **Yeni Tarif Ekle** butonuna tıkla
2. Form alanlarını doldur:
   - **Tarif Başlığı:** Örn: "Menemen"
   - **Kısa Açıklama:** Tarif hakkında kısa bilgi
   - **Malzemeler:** Her satırda bir malzeme (newline-separated)
   - **Yapılış:** Adım adım talimatlar
   - **Fotoğraf:** Tarif görseli (JPG, PNG, WebP)
   - **Hazırlık Süresi:** Dakika cinsinden
   - **Pişirme Süresi:** Dakika cinsinden
   - **Porsiyon:** Kişi sayısı
3. **Tarifi Ekle** butonuna tıkla

### Anasayfada Görüntüle
1. http://127.0.0.1:5000/
2. Eklediğin tarif grid'te görünecektir
3. Tarife tıklayarak detay sayfasını aç

### Arama ve Filtreleme
1. http://127.0.0.1:5000/search
2. **Metin araması:** Tarif adına göre ara
3. **Etiket filtresi:** Etiketlere göre filtrele

---

## 🐛 Sorun Giderme

### "unable to open database file" Hatası
```bash
# data/ klasörünü manuel oluştur
mkdir data
```

### Port 5000 zaten kullanılıyor
config.py dosyasında portu değiştir:
```python
PORT = 5001  # Başka bir port seç
```

### Modül import hatası ("ModuleNotFoundError")
Sanal ortamın aktivasyon işlemini kontrol et:
```bash
# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### Görsel yükleme başarısız
- Dosya boyutu 10 MB'dan küçük mü? (MAX_CONTENT_LENGTH)
- Dosya türü destekleniyor mu? (jpg, jpeg, png, webp)
- `uploads/` klasörü var mı ve yazılabilir mi?

---

## 📝 Git Workflow

Her dosya değişikliğinden sonra:

```bash
# Dosyaları commit'e ekle
git add .

# Değişiklikleri commit'le
git commit -m "Açıklayıcı mesaj (Türkçe veya İngilizce)"

# GitHub'a push'la
git push
```

Örnek:
```bash
git add templates/index.html
git commit -m "Update homepage grid layout"
git push
```

---

## 🚀 Production Hazırlığı (İleride)

Üretim ortamında şunları yapınız:

1. **Parola Değiştir**
   - `config.py`'da `ADMIN_PASSWORD` güçlü bir parola ile değiştir

2. **Güvenlik Ayarları**
   - `DEBUG = False`
   - `SECRET_KEY`'ı rastgele bir değerle değiştir

3. **Web Server**
   - Geliştirme sunucusu yerine production WSGI server (Gunicorn, uWSGI) kullan
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 127.0.0.1:5000 application:create_app()
   ```

4. **Ters Proxy (Nginx)**
   - Gunicorn'un önüne Nginx koy
   - SSL/TLS sertifikası konfigüre et

5. **Veritabanı Yedekleme**
   - `data/app.db` dosyasını periyodik olarak yedekle

---

## 📞 Destek

Sorunlar için GitHub Issues'ı ziyaret et veya izeluysal@gmail.com ile iletişim kur.

**Proje Sahibi:** İzel Uysal  
**Başlangıç Tarihi:** Eylül 2026  
**Canlı Site:** https://yemek.izeluysal.com.tr
