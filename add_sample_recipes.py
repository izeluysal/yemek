#!/usr/bin/env python
"""Add sample Turkish recipes to the database"""
import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application import create_app
from models import db, Recipe, Tag

def add_sample_recipes():
    """Add 3 sample Turkish recipes to the database"""
    app = create_app()
    
    with app.app_context():
        # Define categories/tags to ensure they exist
        categories = ['Kahvaltı', 'Çorbalar', 'Zeytinyağlılar', 'Diğer']
        tags_dict = {}
        
        for cat_name in categories:
            tag = Tag.query.filter_by(name=cat_name).first()
            if not tag:
                tag = Tag(name=cat_name)
                db.session.add(tag)
                db.session.flush()
            tags_dict[cat_name] = tag
        
        db.session.commit()
        
        # Sample recipes
        recipes_data = [
            {
                'title': 'Mercimek Çorbası',
                'description': 'Kırmızı mercimekten yapılan, besleyici ve leziz geleneksel Türk çorbası. Sıcak ve misafirlerin severek yediği bir klasik.',
                'ingredients': [
                    '2 bardak kırmızı mercimek',
                    '1 soğan',
                    '2 yemek kaşığı tereyağı',
                    '1 litre su',
                    '1 tatlı kaşığı tuz',
                    '1/2 tatlı kaşığı karabiber',
                    'Kırmızı biber',
                    'Limon'
                ],
                'instructions': 'Tereyağda soğanı kavurın. Mercimekleri ekleyip 5 dakika kavrulmasını sağlayın. Su ekleyin. Mercimekler yumuşayana kadar kaynatın (yaklaşık 30 dakika). Blender ile pürüleyin. Tuz, karabiber ve kırmızı biber ekleyin. Limon ve kuru nane ile servis yapın.',
                'prep_time': 10,
                'cook_time': 35,
                'servings': 6,
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80',
                'tags': ['Çorbalar']
            },
            {
                'title': 'Menemen',
                'description': 'Domates, biber ve soğanla hazırlanan, yumurtayla servis edilen geleneksel Türk kahvaltısı. Hızlı ve doyurucu bir sabah yemeği.',
                'ingredients': [
                    '3 yumurta',
                    '1 domates',
                    '1 yeşil biber',
                    '1 kırmızı biber',
                    '1/2 soğan',
                    '2 yemek kaşığı zeytin yağı',
                    'Tuz ve karabiber',
                    'Kuru nane'
                ],
                'instructions': 'Zeytin yağında soğanı kavurun. Domatesle biberleri ekleyin. Sebzeler yumuşayana kadar pişirin. Yumurtalı tuzlu su ilave edin. Yumurtalar pişene kadar karıştırarak pişirin. Kuru nane ve karabiber ile garnitür yapın.',
                'prep_time': 5,
                'cook_time': 15,
                'servings': 3,
                'image_url': 'https://images.unsplash.com/photo-1533193566920-8dd03ffd7850?auto=format&fit=crop&w=600&q=80',
                'tags': ['Kahvaltı']
            },
            {
                'title': 'Biber Dolması',
                'description': 'Yeşil biberleri pirince, soğan ve baharat karışımıyla dolduran ve zeytinyağında pişirilen meşhur Türk zeytinyağlı yemeği. Harika bir başlangıç.',
                'ingredients': [
                    '6 adet yeşil biber',
                    '1 bardak pirinç',
                    '1 soğan (kıyılmış)',
                    '1/2 bardak çam fistiki',
                    '2 yemek kaşığı kuru üzüm',
                    '3 yemek kaşığı zeytin yağı',
                    '1 tatlı kaşığı tuz',
                    '1/2 tatlı kaşığı karabiber',
                    '1 tatlı kaşığı kuru dill',
                    'Su'
                ],
                'instructions': 'Biberlerin tepelerini kesin ve içindekileri çıkarın. Zeytin yağında soğanı kavurun. Pirinci ekleyin ve 2-3 dakika kavurun. Çam fistiki, üzüm, dill, tuz ve karabiberi ekleyin. Karışımı biberlere doldurun. Dolması kapları bir tava içine dizin. Üzerine su dökün. Ağır ateşte 45 dakika pişirin.',
                'prep_time': 20,
                'cook_time': 45,
                'servings': 4,
                'image_url': 'https://images.unsplash.com/photo-1505521585350-cb5ee113f50c?auto=format&fit=crop&w=600&q=80',
                'tags': ['Zeytinyağlılar']
            }
        ]
        
        # Add recipes to database
        for recipe_data in recipes_data:
            # Check if recipe already exists
            title = recipe_data['title']
            slug = Recipe.generate_slug(title)
            
            if Recipe.query.filter_by(slug=slug).first():
                print(f"⏭️  Tarif zaten var: {title}")
                continue
            
            # Create recipe
            recipe = Recipe(
                title=title,
                slug=slug,
                description=recipe_data['description'],
                ingredients=recipe_data['ingredients'],
                instructions=recipe_data['instructions'],
                prep_time=recipe_data['prep_time'],
                cook_time=recipe_data['cook_time'],
                servings=recipe_data['servings'],
                image_url=recipe_data['image_url'],
            )
            
            # Add tags
            for tag_name in recipe_data['tags']:
                tag = tags_dict.get(tag_name)
                if tag:
                    recipe.tags.append(tag)
            
            db.session.add(recipe)
            print(f"✅ Tarif eklendi: {title}")
        
        # Commit all changes
        db.session.commit()
        print("\n🎉 Tüm tarifler başarıyla veritabanına eklendi!")
        
        # Show summary
        total_recipes = Recipe.query.count()
        print(f"📊 Toplam tarif sayısı: {total_recipes}")

if __name__ == '__main__':
    add_sample_recipes()
