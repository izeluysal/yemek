# 🍳 Yemek Tarifi Defteri

**Modern, Minimalist, Türkçe Dijital Tarif Defteri**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)
[![Flask: 3.0.0](https://img.shields.io/badge/Flask-3.0.0-green)](https://flask.palletsprojects.com/)
[![Bootstrap: 5.3.0](https://img.shields.io/badge/Bootstrap-5.3.0-purple)](https://getbootstrap.com/)

---

## ✨ Özellikler

- 🔍 **Metin Araması & Etiket Filtreleri:** Hızlı tarif bulma
- 🖼️ **Görselli Tarif Kartları:** Responsive grid tasarımı
- 📱 **Mobil Uyumlu:** Bootstrap 5 ile tüm cihazlarda çalışır
- 🔐 **Admin Paneli:** Tarif ekleme, düzenleme, silme işlevleri
- 🗄️ **SQLite Veritabanı:** Hafif, dosya tabanlı, kurulum gerektirmeyen
- 🎨 **Sade Tasarım:** Dikkat dağıtıcı öğeler olmadan, reklamsız
- 🚀 **Hızlı:** Flask + SQLAlchemy ile optimized performans

---

## 🛠️ Tech Stack

| Bileşen | Teknoloji |
|---------|-----------|
| **Backend** | Python + Flask 3.0.0 |
| **ORM** | SQLAlchemy + Flask-SQLAlchemy |
| **Veritabanı** | SQLite 3 |
| **Frontend Framework** | Bootstrap 5.3.0 |
| **Frontend Logic** | Vanilla JavaScript |
| **Görsel İşleme** | Pillow |
| **Deployment** | Local Python venv |

---

## 📋 Hızlı Başlangıç

### Gereksinimler
- Python 3.9+
- Git

### Kurulum
```bash
# Projeyi clone et
git clone https://github.com/izeluysal/yemek-tarifi-defteri.git
cd yemek-tarifi-defteri

# Sanal ortam oluştur
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
# veya: source .venv/bin/activate  # macOS/Linux

# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı çalıştır
python application.py
```

### Erişim
- **Anasayfa:** http://127.0.0.1:5000/
- **Admin Paneli:** http://127.0.0.1:5000/admin/login
- **Şifre:** `admin123` (değiştirilmek önerilir)

---

## 📚 Dokümantasyon

- [**SETUP.md**](md/SETUP.md) — Detaylı kurulum ve konfigürasyon rehberi
- [**PROJE_REHBERI.md**](md/PROJE_REHBERI.md) — Proje spesifikasyonu ve teknik detaylar

---

## 📂 Dosya Yapısı

```
yemek-tarifi-defteri/
├── application.py          # Flask ana uygulaması
├── config.py              # Konfigürasyon
├── models.py              # Database modelleri
├── requirements.txt       # Python bağımlılıkları
├── test_setup.py          # Setup test scripti
│
├── templates/             # HTML şablonları
│   ├── base.html          # Temel şablon
│   ├── index.html         # Anasayfa
│   ├── recipe_detail.html # Tarif detayı
│   ├── search.html        # Arama sayfası
│   ├── admin_login.html   # Admin giriş
│   └── admin/
│       ├── panel.html     # Admin dashboard
│       └── recipe_form.html # Tarif formu
│
├── data/
│   └── app.db             # SQLite veritabanı
│
├── uploads/               # Tarif görselleri
│
└── md/
    ├── SETUP.md           # Kurulum kılavuzu
    └── PROJE_REHBERI.md   # Proje dokümantasyonu
```

---

## 🎯 Özellik Listesi

### ✅ Tamamlanmış
- [x] Flask backend ve SQLAlchemy ORM
- [x] SQLite veritabanı entegrasyonu
- [x] Responsive HTML şablonları (Bootstrap 5)
- [x] Admin paneli (tarif CRUD)
- [x] Metin araması ve etiket filtreleri
- [x] Görsel yükleme ve işleme
- [x] Session-based admin authentication

### 📋 Gelecek Sürümler (İsteğe Bağlı)
- [ ] Baskı-uyumlu tarif sayfası
- [ ] Malzeme hesaplayıcı (porsiyon ayarlı)
- [ ] Takvim temelli tarif planlayıcı
- [ ] PDF export
- [ ] Sosyal medya share butonları
- [ ] Kullanıcı rating sistemi (yorum olmayan)

---

## 🔒 Güvenlik Notları

- Admin şifresi `config.py`'da hardcoded tutulur (geliştirme için uygundur)
- Production ortamında:
  - Parolayı environment variable'dan oku
  - Parola hash'leme (bcrypt/Argon2) kullan
  - HTTPS/SSL etkinleştir
  - CSRF protection ekle

---

## 📸 Ekran Görüntüleri

### Anasayfa
```
[Navbar: Logo | Ara | Admin | Logout]
[Arama Çubuğu]
[Popüler Etiketler]
[Tarif Kartları Grid - 3 Sütun]
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │   Görsel    │  │   Görsel    │  │   Görsel    │
  │  Başlık     │  │  Başlık     │  │  Başlık     │
  │  Etiketler  │  │  Etiketler  │  │  Etiketler  │
  │  Sureleri   │  │  Sureleri   │  │  Sureleri   │
  └─────────────┘  └─────────────┘  └─────────────┘
[Sayfalama: < 1 2 3 >]
```

### Tarif Detayı
```
[Navbar]
[Tam Genişlik Görsel]
[Başlık & Açıklama]
[Info: Süre | Porsiyon | Tarih | Etiketler]
┌─────────────────────────────────┐
│ Sol (40%)      │   Sağ (60%)    │
│ Malzemeler     │   Yapılış      │
│ ☐ Mal 1        │ 1. Adım 1      │
│ ☐ Mal 2        │ 2. Adım 2      │
│ ☐ Mal 3        │ 3. Adım 3      │
└─────────────────────────────────┘
[Geri Dön Butonu]
```

---

## 🤝 Katkıda Bulunma

Bu proje kişisel bir proje olsa da, bug raporları ve önerileri kabul ediyor:

1. Fork'la
2. Feature branch oluştur (`git checkout -b feature/amazing-feature`)
3. Commit'le (`git commit -m 'Harika özellik ekle'`)
4. Push'la (`git push origin feature/amazing-feature`)
5. Pull Request aç

---

## 📄 Lisans

MIT Lisansı altında yayınlanmıştır. Bkz: [LICENSE](LICENSE)

---

## 👤 Yazar

**İzel Uysal**  
📧 [izeluysal@gmail.com](mailto:izeluysal@gmail.com)  
🌐 [izeluysal.com.tr](https://izeluysal.com.tr)  
🍳 [yemek.izeluysal.com.tr](https://yemek.izeluysal.com.tr)

---

## 🙏 Teşekkürler

- Flask ve Pallets ekibine
- SQLAlchemy ve Mike Bayer'e
- Bootstrap ekibine
- Python topluluğuna

---

## 📞 Destek

Sorular veya sorunlar için:
- GitHub Issues açın
- E-mail gönderin: izeluysal@gmail.com

---

<div align="center">

**Made with ❤️ by İzel Uysal**

⭐ Beğendiysen star ver! | 🔄 Paylaş!

*Türkçe Tarif Defteri - Modern, Minimalist, Reklamsız*

</div>
