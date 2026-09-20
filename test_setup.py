#!/usr/bin/env python
"""Test script to verify application setup"""

from application import create_app

try:
    app = create_app()
    print("✓ Uygulama başarıyla yüklendi")
    print(f"✓ Veritabanı: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"✓ Admin Şifresi: {app.config['ADMIN_PASSWORD']}")
    print(f"✓ Yemek Dosyaları Klasörü: {app.config['UPLOAD_FOLDER']}")
    print(f"✓ Host: {app.config['HOST']}")
    print(f"✓ Port: {app.config['PORT']}")
    print("\n✓ Kurulum başarılı! Sunucuyu başlatmak için çalıştırın:")
    print("  python application.py")
except Exception as e:
    print(f"✗ Hata: {e}")
    import traceback
    traceback.print_exc()
