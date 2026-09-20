"""Seed script to populate database with 20 Turkish recipes"""
from application import create_app
from models import db, Recipe, Tag
import json

def seed_database():
    """Populate database with 20 authentic Turkish recipes"""
    
    app = create_app()
    
    with app.app_context():
        # Completely reset database
        db.drop_all()
        db.create_all()
        
        # Create categories
        categories = {
            'Zeytinyağlılar': 'Zeytinyağlılar',
            'Çorbalar': 'Çorbalar',
            'Ana Yemekler': 'Ana Yemekler',
            'Tatlılar': 'Tatlılar',
            'Kahvaltı': 'Kahvaltı',
            'Diğer': 'Diğer'
        }
        
        tags_dict = {}
        for tag_name in categories.values():
            tag = Tag(name=tag_name)
            db.session.add(tag)
            tags_dict[tag_name] = tag
        db.session.flush()  # Flush to get IDs before using in recipes
        db.session.commit()
        
        # Define 20 recipes
        recipes_data = [
            # Zeytinyağlılar (6)
            {
                'title': 'İmam Bayıldı',
                'category': 'Zeytinyağlılar',
                'description': 'Patlıcanın içine soğan ve domates doldurularak zeytinyağında pişirilen leziz bir yemek.',
                'prep_time': 20,
                'cook_time': 40,
                'servings': 4,
                'ingredients': ['4 adet patlıcan', '2 adet soğan', '3 adet domates', '100 ml zeytinyağı', '3 diş sarımsak', 'Tuz', 'Karabiber', 'Maydanoz'],
                'instructions': '1. Patlıcanları uzunlamasına yarıya böl, özsüyünü al\n2. Soğan ve domatesi ince kıyarak sarımsak ekle\n3. Patlıcanların içine doldurmayı koy\n4. Zeytinyağda 40 dakika pişir\n5. Sıcak veya soğuk olarak servis et',
                'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Dolma',
                'category': 'Zeytinyağlılar',
                'description': 'Asma yaprağına sarılmış pirinç, çam fistığı ve kuru üzüm dolması.',
                'prep_time': 30,
                'cook_time': 45,
                'servings': 6,
                'ingredients': ['40 adet asma yaprağı', '2 su bardağı pirinç', '50 g çam fıstığı', '50 g kuru üzüm', '2 adet soğan', '100 ml zeytinyağı', 'Tuz', 'Karabiber', 'Nane'],
                'instructions': '1. Pirin, soğan, çam fıstığı ve üzümü karıştır\n2. Her asma yaprağının parlak yüzüne malzeme koy\n3. Tıkırdatmadan doldur ve rulo şeklinde sar\n4. Zeytinyağda 45 dakika pişir\n5. Soğumadan önce limonla servis et',
                'image_url': 'https://images.unsplash.com/photo-1571877227200-a0ca208b3fd3?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Zeytinyağlı Fasulye',
                'category': 'Zeytinyağlılar',
                'description': 'Beyaz fasülyenin zeytinyağda, domates ve soğanla pişirilmiş tarifi.',
                'prep_time': 15,
                'cook_time': 50,
                'servings': 4,
                'ingredients': ['400 g beyaz fasülye (kurutulmuş, ıslatılmış)', '3 adet domates', '2 adet soğan', '100 ml zeytinyağı', '3 diş sarımsak', 'Tuz', 'Karabiber', 'Kuru rigani'],
                'instructions': '1. Fasulyeyi öncesinde ıslatıp haşla\n2. Soğan ve sarımsağı zeytinyağda kızart\n3. Domatesi ekle, sofra tuzunu konserve et\n4. Pişmiş fasulyeyi ekle\n5. 50 dakika yavaş ateşte kaynat',
                'image_url': 'https://images.unsplash.com/photo-1609070099919-ef77cc08ae5a?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Yaprak Sarması',
                'category': 'Zeytinyağlılar',
                'description': 'Marul ve lahana yaprağına sarılmış pirinçli, kuru üzümle zenginleştirilmiş tarif.',
                'prep_time': 25,
                'cook_time': 40,
                'servings': 6,
                'ingredients': ['30 adet lahana yaprağı', '2 su bardağı pirinç', '100 g kuru üzüm', '2 adet soğan', '80 ml zeytinyağı', '50 g çam fıstığı', 'Tuz', 'Karabiber'],
                'instructions': '1. Lahana yapraklarını haşla ve soğut\n2. Pirinç, üzüm, fıstık ve soğanı harmanla\n3. Her yaprağa doldurmayı yerleştir\n4. Sıkıca sar ve katlanmış şekilde tepsiye koy\n5. Zeytinyağ ekleyip 40 dakika pişir',
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Karnıyarık',
                'category': 'Zeytinyağlılar',
                'description': 'Patlıcanın yarısı zeytinyağlı sebzeler, diğer yarısı kıymalı dolgu içerir.',
                'prep_time': 20,
                'cook_time': 35,
                'servings': 4,
                'ingredients': ['4 adet patlıcan', '250 g kıyma', '2 adet soğan', '2 adet domates', '100 ml zeytinyağı', '3 diş sarımsak', 'Tuz', 'Karabiber', 'Maydanoz'],
                'instructions': '1. Patlıcanları uzunlamasına yarıya böl\n2. Bir tarafa domates-soğan, diğer tarafa kıymalı dolgu koy\n3. Zeytinyağda 35 dakika pişir\n4. Sıcak olarak servis et\n5. Maydanoz ile garnir yap',
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Kabak Mücver',
                'category': 'Zeytinyağlılar',
                'description': 'Kabaktan yapılan, peynirli ve otlu tatlı mücverler.',
                'prep_time': 20,
                'cook_time': 20,
                'servings': 4,
                'ingredients': ['1 kg kabak', '2 adet soğan', '200 g beyaz peynir', '2 adet yumurta', '200 g un', '100 ml zeytinyağı', 'Tuz', 'Karabiber', 'Dil otı'],
                'instructions': '1. Kabağı rende et, tuz atıp 15 dakika beklet\n2. Suyu sıkıp soğan ve peynir ekle\n3. Yumurta ve un karıştır\n4. Zeytinyağda kızart\n5. Soğuk olarak suyu diye servis et',
                'image_url': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?auto=format&fit=crop&w=600&q=80'
            },
            
            # Çorbalar (5)
            {
                'title': 'Mercimek Çorbası',
                'category': 'Çorbalar',
                'description': 'Kırmızı mercimekten yapılan, ılık veya sıcak içilir, beslenme değeri yüksek bir çorba.',
                'prep_time': 10,
                'cook_time': 30,
                'servings': 6,
                'ingredients': ['1.5 su bardağı kırmızı mercimek', '1 adet soğan', '2 adet havuç', '2 patates', '2 litre su', '4 kaşık un', '2 kaşık tereyağı', 'Tuz', 'Karabiber', 'Kırmızı biber'],
                'instructions': '1. Tereyağda soğanı kızart\n2. Unu hafif kavrulmuş renkte pişir\n3. Suyu ekle ve kaynattır\n4. Havuç, patates ve mercimeği ekle\n5. 30 dakika pişir ve blenderdan geçir',
                'image_url': 'https://images.unsplash.com/photo-1547592166-23ac45744acd?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Işkembe Çorbası',
                'category': 'Çorbalar',
                'description': 'Tripe çorbasının geleneksel Türk haline, sarımsak ve limonla servis edilir.',
                'prep_time': 15,
                'cook_time': 90,
                'servings': 6,
                'ingredients': ['500 g işkembe', '3 litre kemik suyu', '3 adet soğan', '4 kaşık tereyağı', '4 kaşık un', '3 litre. süt', 'Tuz', 'Karabiber', 'Sarımsak', 'Limon'],
                'instructions': '1. İşkembe temizle ve haşla\n2. Tereyağda soğanı kızart, unu ekle\n3. Işkembe suyunu ve sütü ekle\n4. 90 dakika pişir\n5. Sarımsak ve limonla servis et',
                'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Yayla Çorbası',
                'category': 'Çorbalar',
                'description': 'Yoğurt, pirinç ve et bulyon ile yapılan, besleyici bir tartar çorbası.',
                'prep_time': 15,
                'cook_time': 40,
                'servings': 6,
                'ingredients': ['2 litre tavuk bulyon', '1.5 su bardağı yoğurt', '100 g pirinç', '2 adet yumurta', '3 kaşık un', '3 kaşık tereyağı', 'Nane', 'Tuz', 'Karabiber'],
                'instructions': '1. Pirinçi tereyağda kızart\n2. Bulyon ekle ve pirinç pişinceye kadar kaynat\n3. Yoğurt ve yumurtayı karıştır\n4. Sıcak çorbaya yavaş yavaş ekle\n5. Nane ile servis et',
                'image_url': 'https://images.unsplash.com/photo-1537357652180-4f9e5e0b2f7e?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Sebze Çorbası',
                'category': 'Çorbalar',
                'description': 'Mevsimsel sebzelerle zengin, besleyici ve hafif bir çorba tarifi.',
                'prep_time': 20,
                'cook_time': 35,
                'servings': 6,
                'ingredients': ['2 adet havuç', '2 adet kereviz kökü', '150 g kabak', '2 adet patates', '100 g taze fasülye', '2 litre sebze bulyon', '2 kaşık tereyağı', '1 adet soğan', 'Tuz', 'Karabiber', 'Maydanoz'],
                'instructions': '1. Sebzeleri küçük küpler olarak kes\n2. Tereyağda soğanı kızart\n3. Sebzeleri sırayla ekle\n4. Bulyon ekleyip 35 dakika pişir\n5. Maydanoz serpiştirerek sun',
                'image_url': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Akça Çorba',
                'category': 'Çorbalar',
                'description': 'Yoğurt tabanında, et bulyon ve un ile yapılan beyaz, bağlantılı tartar.',
                'prep_time': 15,
                'cook_time': 30,
                'servings': 6,
                'ingredients': ['1.5 su bardağı yoğurt', '3 litre et bulyon', '4 kaşık un', '3 kaşık tereyağı', '2 adet yumurta', 'Tuz', 'Karabiber', 'Nane'],
                'instructions': '1. Yoğurtu oda sıcaklığında tutun\n2. Yumurta ve unu yoğurta ekle\n3. Sıcak bulyonu yavaş yavaş ekle\n4. Tüm çorbayı kaynaya getir\n5. Nane serpiştirerek servis et',
                'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80'
            },
            
            # Ana Yemekler (5)
            {
                'title': 'Adana Kebap',
                'category': 'Ana Yemekler',
                'description': 'Baharat ve pul biber içeren kıymadan yapılan Adanada doğma İşin lezzetli kebap.',
                'prep_time': 25,
                'cook_time': 20,
                'servings': 4,
                'ingredients': ['500 g kıyma (dana ve kuzu karışımı)', '2 adet soğan', '1 bademli pul biber', '2 kaşık cıız', '2 diş sarımsak', 'Kırmızı biber', 'Tuz', 'Karabiber', 'Maydanoz', 'Kuru nane'],
                'instructions': '1. Kıyma, baharatlar ve ince kıyılmış soğanı karıştır\n2. Porsiyonları ıslak elleriyle şekillendirerek şişe sar\n3. Orta-yüksek ateşte 15-20 dakika pişir\n4. Taze soğan, limon ve maydanozla servis et\n5. İsteğe bağlı pide ekmek ile beraber sun',
                'image_url': 'https://images.unsplash.com/photo-1565958011504-4b852f45fb50?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Mantı',
                'category': 'Ana Yemekler',
                'description': 'İçi kıyma dolu, ufak işçi tatlı ve soslu, Anadolu\'ya en ünlü yemeği.',
                'prep_time': 60,
                'cook_time': 25,
                'servings': 6,
                'ingredients': ['3 su bardağı un', '1 adet yumurta', '250 g kıyma', '1 adet soğan', '2 kaşık tereyağı', 'Tuz', 'Karabiber', '1 su bardağı yoğurt', '1 litre tavuk bulyon', 'Pul biber', 'Kırmızı biber'],
                'instructions': '1. Un, yumurta ve tuz ile hamur yapıştır\n2. Kıymayı soğan, tuz ve karabiberle hazırla\n3. Hamurdan küçük kare parçalar kes\n4. Her parçaya kıyma koy ve köşelerini birleştir\n5. Kaynamış bulyonda 15 dakika pişir\n6. Yoğurt sosuna batırılarak servis et',
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Mücver Pilavi',
                'category': 'Ana Yemekler',
                'description': 'Kabak mücverin yanında servis edilen, zeytinyağlı pirinç pilavı.',
                'prep_time': 30,
                'cook_time': 40,
                'servings': 4,
                'ingredients': ['2 su bardağı pirinç', '1 kg kabak', '2 adet soğan', '200 g peynir', '2 adet yumurta', '100 ml zeytinyağı', '500 ml tavuk bulyon', 'Tuz', 'Karabiber', 'Dil otı', 'Un'],
                'instructions': '1. Kabağı rende edip tuzu çekme\n2. Mücver hamurunu hazırla ve tepsiye dökerek kızart\n3. Soğanı zeytinyağında kızart, pirinçi ekle\n4. Bulyonu ekleyip kapatıp 20 dakika pişir\n5. Mücver ve pilav beraber servis et',
                'image_url': 'https://images.unsplash.com/photo-1609070099919-ef77cc08ae5a?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Şiş Köfte',
                'category': 'Ana Yemekler',
                'description': 'Baharat, ekmek kırması ve soğanla hazırlanmış, şişte pişirilen leziz köfte.',
                'prep_time': 20,
                'cook_time': 20,
                'servings': 4,
                'ingredients': ['500 g kıyma', '100 g ekmek kırması', '1 adet soğan', '2 diş sarımsak', '1 adet yumurta', '2 kaşık parsley', 'Tuz', 'Karabiber', 'Kimyon', 'Kırmızı biber'],
                'instructions': '1. Kıymaya ekmek kırması, yumurta ve baharatlar ekle\n2. Elleriyle iyice karıştır\n3. Şişe sarılı halde şekillendirerek sarılı şişe atar\n4. Orta ateşte 18-20 dakika pişir\n5. Soğan, limon ve maydanozla servis et',
                'image_url': 'https://images.unsplash.com/photo-1565958011504-4b852f45fb50?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Pastırmalı Mercimek',
                'category': 'Ana Yemekler',
                'description': 'Kırmızı mercimeğe pastırma ekenerek lezzetin arttırıldığı bir ana yemek.',
                'prep_time': 20,
                'cook_time': 40,
                'servings': 4,
                'ingredients': ['1.5 su bardağı kırmızı mercimek', '200 g pastırma', '2 adet soğan', '100 ml zeytinyağı', '3 adet domates', '1 litre tavuk bulyon', '3 diş sarımsak', 'Tuz', 'Karabiber', 'Pul biber'],
                'instructions': '1. Soğan ve sarımsağı zeytinyağında kızart\n2. Domatesi ekleyip kısını ver\n3. Mercimeği ekle ve bulyonu dök\n4. 30 dakika pişir\n5. Pastırmayı yüzeyine koyup 10 dakika daha pişir',
                'image_url': 'https://images.unsplash.com/photo-1609070099919-ef77cc08ae5a?auto=format&fit=crop&w=600&q=80'
            },
            
            # Tatlılar (3)
            {
                'title': 'Baklava',
                'category': 'Tatlılar',
                'description': 'Yufka arasına fındık ve ceviz konularak tereyağda pişirilen, şerbet uygulanmış tatlı.',
                'prep_time': 30,
                'cook_time': 40,
                'servings': 8,
                'ingredients': ['16 yufka yaprağı', '200 g fındık', '200 g ceviz', '200 g tereyağı', '250 g şeker', '250 ml su', '1 çay kaşığı limon suyu', 'Tarçın', '1 yumurta akı'],
                'instructions': '1. Fındık ve cevizi rende et\n2. Tereyağlı tepsiye yufka yayıp kaynuoğu serp\n3. Katman katman tekrar et\n4. Tereyağla ilişkiler, dilimle ve fırına koy\n5. 180°C\'de 40 dakika pişir\n6. Şerbet uyguLA ve soğumaya bırak',
                'image_url': 'https://images.unsplash.com/photo-1599599810694-b5ac4dd64b73?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Sütlaç',
                'category': 'Tatlılar',
                'description': 'Pirinç unundan yapılan, süt ve şeker ile tatlandırılmış, fırında pişirilen geleneksel pudding.',
                'prep_time': 10,
                'cook_time': 30,
                'servings': 6,
                'ingredients': ['1 su bardağı pirinç unu', '1 litre süt', '150 g şeker', '30 g tereyağı', '1 çay kaşığı vanilya', 'Tuz', 'Tarçın'],
                'instructions': '1. Sütü ısıt ama kaynattma\n2. Pirinç ununu soğuk sütlü harmanla\n3. Sıcak süte yavaş yavaş ekle\n4. 10 dakika ısıtarak karıştır\n5. Porsiyonlara böl, tarçın serp\n6. 180°C fırında 20 dakika pişir',
                'image_url': 'https://images.unsplash.com/photo-1571897943214-4fa1d58a3d9c?auto=format&fit=crop&w=600&q=80'
            },
            {
                'title': 'Revani',
                'category': 'Tatlılar',
                'description': 'Yoğurt ve irmik ile yapılan, üzerine şerbet çalı bir tatlı keki.',
                'prep_time': 15,
                'cook_time': 35,
                'servings': 8,
                'ingredients': ['2 su bardağı irmik', '1 su bardağı yoğurt', '1 su bardağı şeker', '100 ml zeytinyağı', '2 çay kaşığı koku tuzu unu', '50 g hindistancevizi rendelemesi', '24 fındık çekirdeği', '250 g şeker (şerbet için)', '250 ml su (şerbet için)'],
                'instructions': '1. İrmiği, yoğurdu, şekeri ve yağı karıştır\n2. Hindistancevizi ekle\n3. Tepsiye dök, fındık yerleştir\n4. 180°C fırında 35 dakika pişir\n5. Hazır şerbeti sıcak kekeği üzerine dök',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=600&q=80'
            },
            
            # Kahvaltı (1)
            {
                'title': 'Menenici Salatası',
                'category': 'Kahvaltı',
                'description': 'Çoban salatamızı andıran, nane ve limonla hazırlanmış taze malzemesel bahçıvan salatası.',
                'prep_time': 15,
                'cook_time': 0,
                'servings': 4,
                'ingredients': ['4 adet domates', '3 adet salatalık', '1 adet kırmızı soğan', '1 demet maydanoz', '1 demet nane', '100 ml zeytinyağı', '3 limon suyu', 'Tuz', 'Karabiber'],
                'instructions': '1. Domatesleri ve salatalığı küçük küpler kes\n2. Soğanı ince ince kıyıp tuzla\n3. Tüm malzemeleri bir kasede karıştır\n4. Zeytinyağ ve limon sası hazırla\n5. Üzerine dök ve muhafaza et',
                'image_url': 'https://images.unsplash.com/photo-1540189549336-e6e99c3679fe?auto=format&fit=crop&w=600&q=80'
            }
        ]
        
        # Insert recipes
        for recipe_data in recipes_data:
            category_name = recipe_data.pop('category')
            
            recipe = Recipe(
                title=recipe_data['title'],
                slug=recipe_data['title'].lower().replace(' ', '-').replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i').replace('ö', 'o').replace('ş', 's').replace('ü', 'u'),
                description=recipe_data.get('description', ''),
                ingredients=recipe_data['ingredients'],
                instructions=recipe_data['instructions'],
                image_url=recipe_data.get('image_url', ''),
                prep_time=recipe_data.get('prep_time'),
                cook_time=recipe_data.get('cook_time'),
                servings=recipe_data.get('servings', 4)
            )
            
            # Add category tag
            tag = tags_dict.get(category_name)
            if tag:
                recipe.tags.append(tag)
            
            db.session.add(recipe)
        
        db.session.commit()
        print("✅ Database seed completed!")
        print(f"   - Added {len(recipes_data)} recipes")
        print(f"   - Categories: Zeytinyağlılar (6), Çorbalar (5), Ana Yemekler (5), Tatlılar (3), Kahvaltı (1)")
        print(f"   - All recipes have ingredients for 'Dolapta Ne Var?' filter")

if __name__ == '__main__':
    seed_database()
