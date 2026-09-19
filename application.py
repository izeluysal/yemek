"""
Yemek Tarifi Defteri - Ana Uygulaması
Flask ile REST API
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

app = Flask(__name__)
CORS(app)

# Konfigürasyon
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

# Constants
DB_PATH = os.getenv('DB_PATH', 'data/app.db')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))  # 10MB

# Dosya yükleme klasörü oluştur
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('data', exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def init_db():
    """Veritabanını başlat ve şemayı oluştur"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # SQLite WAL modu etkinleştir
        cursor.execute('PRAGMA journal_mode=WAL;')
        
        # Tarifler tablosu
        cursor.execute('''
            CREATE TABLE recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                slug TEXT NOT NULL UNIQUE,
                description TEXT,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                image_url TEXT,
                prep_time INTEGER,
                cook_time INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Etiketler tablosu
        cursor.execute('''
            CREATE TABLE tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Tarifler-Etiketler ilişki tablosu (Many-to-Many)
        cursor.execute('''
            CREATE TABLE recipe_tags (
                recipe_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                PRIMARY KEY (recipe_id, tag_id),
                FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ Veritabanı '{DB_PATH}' oluşturuldu")


def get_db():
    """Veritabanı bağlantısı oluştur"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    """Açılış sayfası"""
    return jsonify({
        'mesaj': 'Yemek Tarifi Defteri API',
        'versiyon': '1.0.0',
        'durum': 'çalışıyor'
    })


@app.route('/api/health')
def health():
    """Sağlık kontrolü"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200


@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    """Tüm tarifleri getir"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Sayfalama parametreleri
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        # Arama ve filtreleme
        search = request.args.get('search', '', type=str).lower()
        tag = request.args.get('tag', '', type=str)
        
        query = 'SELECT * FROM recipes WHERE 1=1'
        params = []
        
        if search:
            query += ' AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?)'
            search_pattern = f'%{search}%'
            params.extend([search_pattern, search_pattern])
        
        if tag:
            query += ''' AND id IN (
                SELECT recipe_id FROM recipe_tags 
                WHERE tag_id IN (SELECT id FROM tags WHERE LOWER(name) = ?)
            )'''
            params.append(tag.lower())
        
        query += ' ORDER BY created_at DESC LIMIT ? OFFSET ?'
        params.extend([per_page, offset])
        
        cursor.execute(query, params)
        recipes = cursor.fetchall()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'data': [dict(r) for r in recipes],
            'page': page,
            'per_page': per_page
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/recipes/<slug>', methods=['GET'])
def get_recipe(slug):
    """Tek bir tarifi getir"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM recipes WHERE slug = ?', (slug,))
        recipe = cursor.fetchone()
        
        if not recipe:
            conn.close()
            return jsonify({'success': False, 'error': 'Tarif bulunamadı'}), 404
        
        # Etiketleri getir
        cursor.execute('''
            SELECT t.* FROM tags t
            JOIN recipe_tags rt ON t.id = rt.tag_id
            WHERE rt.recipe_id = ?
        ''', (recipe['id'],))
        tags = cursor.fetchall()
        
        conn.close()
        
        recipe_dict = dict(recipe)
        recipe_dict['tags'] = [dict(t) for t in tags]
        
        return jsonify({'success': True, 'data': recipe_dict}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """404 Hataları"""
    return jsonify({'success': False, 'error': 'Sayfa bulunamadı'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 Hataları"""
    return jsonify({'success': False, 'error': 'İç sunucu hatası'}), 500


if __name__ == '__main__':
    # Veritabanını başlat
    init_db()
    
    # Flask sunucusunu başlat
    debug = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))
    
    print(f"\n✓ Uygulaması başlatıldı")
    print(f"  Port: {port}")
    print(f"  Debug: {debug}")
    print(f"  Veritabanı: {DB_PATH}\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
