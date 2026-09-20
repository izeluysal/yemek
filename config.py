"""Flask Configuration"""
import os
from pathlib import Path

class Config:
    """Application Configuration"""
    
    # Get base directory
    BASE_DIR = Path(__file__).parent.resolve()
    
    # Flask
    SECRET_KEY = 'yemek-tarifi-defteri-secret-key-2024'
    FLASK_ENV = 'development'
    DEBUG = True
    
    # Database - use absolute path with forward slashes for SQLite
    DATABASE_PATH = BASE_DIR / 'data' / 'app.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH.as_posix()}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Upload Settings
    UPLOAD_FOLDER = 'yemekfiles'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB max file size
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    
    # Admin Authentication
    ADMIN_PASSWORD = 'admin123'  # Hardcoded simple password
    
    # Application Settings
    RECIPES_PER_PAGE = 12
    HOST = '127.0.0.1'
    PORT = 5003
    
    # WAL Mode for SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {
            'timeout': 15,
            'check_same_thread': False,
        },
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }
