import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Category, SubCategory, Product

# --- 1. CATÉGORIES (Principales) ---
cat_smartphone, _ = Category.objects.get_or_create(name="Smartphone", slug="smartphone")
cat_electronique, _ = Category.objects.get_or_create(name="Electronique", slug="electronique")
cat_electromenager, _ = Category.objects.get_or_create(name="Electromenager", slug="electromenager")
cat_pc, _ = Category.objects.get_or_create(name="PC", slug="pc")
cat_textile, _ = Category.objects.get_or_create(name="Textile", slug="textile")
cat_artisanat, _ = Category.objects.get_or_create(name="Artisanat", slug="artisanat")

# --- 2. SOUS-CATÉGORIES ---
# Smartphone
sub_iphone, _ = SubCategory.objects.get_or_create(name="iPhone", category=cat_smartphone, slug="iphone")
sub_samsung, _ = SubCategory.objects.get_or_create(name="Samsung", category=cat_smartphone, slug="samsung")
sub_tecno, _ = SubCategory.objects.get_or_create(name="Tecno", category=cat_smartphone, slug="tecno")
sub_infinix, _ = SubCategory.objects.get_or_create(name="Infinix", category=cat_smartphone, slug="infinix")
sub_xiaomi, _ = SubCategory.objects.get_or_create(name="Xiaomi", category=cat_smartphone, slug="xiaomi")

# Electronique
sub_accessoires, _ = SubCategory.objects.get_or_create(name="Accessoires", category=cat_electronique, slug="accessoires")
sub_audio, _ = SubCategory.objects.get_or_create(name="Audio", category=cat_electronique, slug="audio")
sub_gaming, _ = SubCategory.objects.get_or_create(name="Gaming", category=cat_electronique, slug="gaming")
sub_chargeurs, _ = SubCategory.objects.get_or_create(name="Chargeurs & Batteries", category=cat_electronique, slug="chargeurs-et-batteries")

# Électroménager
sub_frigo, _ = SubCategory.objects.get_or_create(name="Réfrigérateurs & Congélateurs", category=cat_electromenager, slug="refrigerateurs-et-congelateurs")
sub_cuisine, _ = SubCategory.objects.get_or_create(name="Cuisinières & Fours", category=cat_electromenager, slug="cuisinieres-et-fours")
sub_climatisation, _ = SubCategory.objects.get_or_create(name="Climatisation", category=cat_electromenager, slug="climatisation")
sub_lavage, _ = SubCategory.objects.get_or_create(name="Machines à Laver", category=cat_electromenager, slug="machines-a-laver")

# PC
sub_portables, _ = SubCategory.objects.get_or_create(name="Ordinateurs Portables", category=cat_pc, slug="ordinateurs-portables")
sub_bureautique, _ = SubCategory.objects.get_or_create(name="PC de Bureau", category=cat_pc, slug="pc-de-bureau")
sub_composants, _ = SubCategory.objects.get_or_create(name="Composants PC", category=cat_pc, slug="composants-pc")

# Textile
sub_wax, _ = SubCategory.objects.get_or_create(name="Pagne Wax", category=cat_textile, slug="pagne-wax")
sub_tissus, _ = SubCategory.objects.get_or_create(name="Tissus Traditionnels", category=cat_textile, slug="tissus-traditionnels")
sub_vetements, _ = SubCategory.objects.get_or_create(name="Vêtements", category=cat_textile, slug="vetements")

# Artisanat
sub_sculptures, _ = SubCategory.objects.get_or_create(name="Sculptures & Statues", category=cat_artisanat, slug="sculptures-et-statues")
sub_bijoux, _ = SubCategory.objects.get_or_create(name="Bijoux & Accessoires", category=cat_artisanat, slug="bijoux-et-accessoires")
sub_paniers, _ = SubCategory.objects.get_or_create(name="Paniers & Vannerie", category=cat_artisanat, slug="paniers-et-vannerie")
sub_deco, _ = SubCategory.objects.get_or_create(name="Décoration", category=cat_artisanat, slug="decoration")

# --- 3. PRODUITS (Exhaustif) ---
# --- SMART PHONES ---
products_smartphone = [
    # iPhone
    {"name": "iPhone 13 128Go Reconditionné", "slug": "iphone-13-128", "subcat": sub_iphone, "price": 425000, "supplier": "iStore Bénin", "rating": 4.8, "image": "products/iphone13.jpg", "is_new": False, "sales_count": 15},
    {"name": "iPhone 14 Pro Max 256Go", "slug": "iphone-14-pro-max", "subcat": sub_iphone, "price": 950000, "supplier": "EasyTech", "rating": 4.9, "image": "products/iphone14promax.jpg", "is_new": True, "sales_count": 8},
    {"name": "iPhone 12 64Go Reconditionné", "slug": "iphone-12-64", "subcat": sub_iphone, "price": 310000, "supplier": "iStore Bénin", "rating": 4.7, "image": "products/iphone12.jpg", "is_new": False, "sales_count": 20},
    # Samsung
    {"name": "Samsung Galaxy S23 Ultra 256Go", "slug": "samsung-s23-ultra", "subcat": sub_samsung, "price": 700000, "supplier": "Samsung Bénin", "rating": 4.9, "image": "products/samsung-s23-ultra.jpg", "is_new": True, "sales_count": 12},
    {"name": "Samsung Galaxy A54 128Go", "slug": "samsung-a54", "subcat": sub_samsung, "price": 250000, "supplier": "Samsung Bénin", "rating": 4.6, "image": "products/samsung-a54.jpg", "is_new": True, "sales_count": 30},
    {"name": "Samsung Galaxy A14 64Go", "slug": "samsung-a14", "subcat": sub_samsung, "price": 145000, "supplier": "Samsung Bénin", "rating": 4.4, "image": "products/samsung-a14.jpg", "is_new": False, "sales_count": 45},
    {"name": "Samsung Galaxy Z Fold 5 512Go", "slug": "samsung-z-fold5", "subcat": sub_samsung, "price": 1250000, "supplier": "Samsung Bénin", "rating": 4.8, "image": "products/samsung-zfold5.jpg", "is_new": True, "sales_count": 3},
    # Tecno
    {"name": "Tecno Spark 10 Pro 256Go", "slug": "tecno-spark-10-pro", "subcat": sub_tecno, "price": 135000, "supplier": "Tecno Mobile", "rating": 4.5, "image": "products/tecno-spark-10-pro.jpg", "is_new": False, "sales_count": 60},
    {"name": "Tecno Camon 20 Premier 256Go", "slug": "tecno-camon-20-premier", "subcat": sub_tecno, "price": 220000, "supplier": "Tecno Mobile", "rating": 4.7, "image": "products/tecno-camon-20-premier.jpg", "is_new": True, "sales_count": 28},
    {"name": "Tecno Pova 5 Pro 128Go", "slug": "tecno-pova-5-pro", "subcat": sub_tecno, "price": 165000, "supplier": "Tecno Mobile", "rating": 4.6, "image": "products/tecno-pova-5-pro.jpg", "is_new": True, "sales_count": 35},
    # Infinix
    {"name": "Infinix Note 30 256Go", "slug": "infinix-note-30", "subcat": sub_infinix, "price": 155000, "supplier": "Infinix", "rating": 4.5, "image": "products/infinix-note-30.jpg", "is_new": False, "sales_count": 42},
    {"name": "Infinix Hot 30 128Go", "slug": "infinix-hot-30", "subcat": sub_infinix, "price": 110000, "supplier": "Infinix", "rating": 4.4, "image": "products/infinix-hot-30.jpg", "is_new": False, "sales_count": 55},
    {"name": "Infinix Zero 30 5G 256Go", "slug": "infinix-zero-30-5g", "subcat": sub_infinix, "price": 250000, "supplier": "Infinix", "rating": 4.7, "image": "products/infinix-zero-30-5g.jpg", "is_new": True, "sales_count": 18},
    # Xiaomi
    {"name": "Xiaomi Redmi Note 12 128Go", "slug": "xiaomi-redmi-note-12", "subcat": sub_xiaomi, "price": 175000, "supplier": "Xiaomi", "rating": 4.6, "image": "products/xiaomi-redmi-note-12.jpg", "is_new": False, "sales_count": 33},
    {"name": "Xiaomi 13 Lite 256Go", "slug": "xiaomi-13-lite", "subcat": sub_xiaomi, "price": 290000, "supplier": "Xiaomi", "rating": 4.8, "image": "products/xiaomi-13-lite.jpg", "is_new": True, "sales_count": 22},
    {"name": "Xiaomi Poco X5 Pro 128Go", "slug": "xiaomi-poco-x5-pro", "subcat": sub_xiaomi, "price": 230000, "supplier": "Xiaomi", "rating": 4.7, "image": "products/xiaomi-poco-x5-pro.jpg", "is_new": True, "sales_count": 25},
]

# --- ÉLECTRONIQUE ---
products_electronique = [
    {"name": "Casque Bluetooth Sony WH-1000XM5", "slug": "casque-sony-wh-1000xm5", "subcat": sub_audio, "price": 250000, "supplier": "Sony Pro", "rating": 4.9, "image": "products/sony-wh1000xm5.jpg", "is_new": True, "sales_count": 10},
    {"name": "Écouteurs TWS Samsung Galaxy Buds2 Pro", "slug": "ecouteurs-samsung-buds2-pro", "subcat": sub_audio, "price": 95000, "supplier": "Samsung Bénin", "rating": 4.7, "image": "products/samsung-buds2-pro.jpg", "is_new": True, "sales_count": 28},
    {"name": "Chargeur Rapide 65W GaN", "slug": "chargeur-rapide-65w-gan", "subcat": sub_chargeurs, "price": 12500, "supplier": "AccessTech", "rating": 4.5, "image": "products/chargeur-65w-gan.jpg", "is_new": False, "sales_count": 75},
    {"name": "Power Bank 20000mAh", "slug": "power-bank-20000mah", "subcat": sub_chargeurs, "price": 18000, "supplier": "AccessTech", "rating": 4.6, "image": "products/powerbank-20000.jpg", "is_new": False, "sales_count": 62},
    {"name": "Manette de Jeu PS5 DualSense", "slug": "manette-ps5-dualsense", "subcat": sub_gaming, "price": 55000, "supplier": "GameStore", "rating": 4.9, "image": "products/ps5-dualsense.jpg", "is_new": True, "sales_count": 18},
    {"name": "Support Téléphone Aimanté pour Voiture", "slug": "support-telephone-aimante-voiture", "subcat": sub_accessoires, "price": 5500, "supplier": "AccessTech", "rating": 4.4, "image": "products/support-voiture-aimante.jpg", "is_new": False, "sales_count": 110},
]

# --- ÉLECTROMÉNAGER ---
products_electromenager = [
    {"name": "Réfrigérateur Samsung 320L No Frost", "slug": "refrigerateur-samsung-320l", "subcat": sub_frigo, "price": 450000, "supplier": "Samsung Electromenager", "rating": 4.8, "image": "products/samsung-fridge-320l.jpg", "is_new": True, "sales_count": 9},
    {"name": "Climatiseur Split Inverter 12000 BTU", "slug": "climatiseur-split-inverter-12000", "subcat": sub_climatisation, "price": 350000, "supplier": "ClimTech", "rating": 4.7, "image": "products/clim-12000-btu.jpg", "is_new": True, "sales_count": 15},
    {"name": "Machine à Laver Automatique 7kg", "slug": "machine-a-laver-auto-7kg", "subcat": sub_lavage, "price": 220000, "supplier": "Hisense Bénin", "rating": 4.6, "image": "products/lave-linge-7kg.jpg", "is_new": False, "sales_count": 20},
    {"name": "Cuisinière 4 Feux + Four", "slug": "cuisiniere-4-feux-four", "subcat": sub_cuisine, "price": 185000, "supplier": "Ménager Pro", "rating": 4.5, "image": "products/cuisiniere-4-feux.jpg", "is_new": False, "sales_count": 25},
    {"name": "Micro-ondes 25L", "slug": "micro-ondes-25l", "subcat": sub_cuisine, "price": 85000, "supplier": "Ménager Pro", "rating": 4.7, "image": "products/micro-ondes-25l.jpg", "is_new": True, "sales_count": 30},
]

# --- PC & INFORMATIQUE ---
products_pc = [
    {"name": "MacBook Air M1 8Go 256Go", "slug": "macbook-air-m1", "subcat": sub_portables, "price": 650000, "supplier": "Apple Bénin", "rating": 4.9, "image": "products/macbook-air-m1.jpg", "is_new": False, "sales_count": 14},
    {"name": "PC Portable Gaming Lenovo Legion 5", "slug": "pc-gaming-lenovo-legion-5", "subcat": sub_portables, "price": 850000, "supplier": "Lenovo Store", "rating": 4.8, "image": "products/lenovo-legion5.jpg", "is_new": True, "sales_count": 7},
    {"name": "Ordinateur de Bureau HP EliteDesk", "slug": "pc-bureau-hp-elitedesk", "subcat": sub_bureautique, "price": 280000, "supplier": "HP Pro", "rating": 4.5, "image": "products/hp-elitedesk.jpg", "is_new": False, "sales_count": 18},
    {"name": "SSD 1To NVMe", "slug": "ssd-1to-nvme", "subcat": sub_composants, "price": 55000, "supplier": "PC Parts", "rating": 4.7, "image": "products/ssd-1to-nvme.jpg", "is_new": True, "sales_count": 32},
    {"name": "Écran 24'' Full HD", "slug": "ecran-24-full-hd", "subcat": sub_composants, "price": 95000, "supplier": "PC Parts", "rating": 4.6, "image": "products/ecran-24-fhd.jpg", "is_new": False, "sales_count": 22},
]

# --- TEXTILE ---
products_textile = [
    {"name": "Pagne Wax Vlisco 6 Yar\u0441\u0435ss", "slug": "pagne-wax-vlisco-6y", "subcat": sub_wax, "price": 85000, "supplier": "LUXE Shop", "rating": 4.8, "image": "products/vlisco-wax.jpg", "is_new": True, "sales_count": 25},
    {"name": "Tissu Bogolan Fait Main", "slug": "tissu-bogolan-fait-main", "subcat": sub_tissus, "price": 25000, "supplier": "Artisanat du Bénin", "rating": 4.9, "image": "products/bogolan.jpg", "is_new": False, "sales_count": 40},
    {"name": "Robe Tendance en Wax", "slug": "robe-tendance-wax", "subcat": sub_vetements, "price": 35000, "supplier": "Mode Africa", "rating": 4.7, "image": "products/robe-wax.jpg", "is_new": True, "sales_count": 18},
    {"name": "Ensemble Boubou Homme en Bazin", "slug": "boubou-homme-bazin", "subcat": sub_vetements, "price": 55000, "supplier": "Mode Africa", "rating": 4.8, "image": "products/boubou-bazin.jpg", "is_new": True, "sales_count": 22},
]

# --- ARTISANAT ---
products_artisanat = [
    {"name": "Statue en Bois d'Ébène", "slug": "statue-bois-ebene", "subcat": sub_sculptures, "price": 45000, "supplier": "Artisanat du Bénin", "rating": 4.9, "image": "products/statue-ebene.jpg", "is_new": False, "sales_count": 15},
    {"name": "Sac en Bande de Pneu", "slug": "sac-bande-pneu", "subcat": sub_bijoux, "price": 12000, "supplier": "Artisanat du Bénin", "rating": 4.7, "image": "products/sac-pneu.jpg", "is_new": True, "sales_count": 45},
    {"name": "Panier Tissé en Raphia", "slug": "panier-tisse-raphia", "subcat": sub_paniers, "price": 8500, "supplier": "Artisanat du Bénin", "rating": 4.6, "image": "products/panier-raphia.jpg", "is_new": False, "sales_count": 60},
    {"name": "Lot de 4 Tasses en Céramique", "slug": "lot-tasses-ceramique", "subcat": sub_deco, "price": 15000, "supplier": "Artisanat du Bénin", "rating": 4.8, "image": "products/tasses-ceramique.jpg", "is_new": True, "sales_count": 28},
]

# --- 4. INSERTION DANS LA BASE DE DONNÉES ---
print("Début du peuplement de la base de données...")

for p in products_smartphone:
    Product.objects.create(
        name=p["name"], slug=p["slug"], category=cat_smartphone, subcategory=p["subcat"],
        price=p["price"], supplier=p["supplier"], rating=p["rating"], image=p["image"],
        is_new=p["is_new"], sales_count=p["sales_count"]
    )
    print(f"Ajouté: {p['name']}")

for p in products_electronique:
    Product.objects.create(
        name=p["name"], slug=p["slug"], category=cat_electronique, subcategory=p["subcat"],
        price=p["price"], supplier=p["supplier"], rating=p["rating"], image=p["image"],
        is_new=p["is_new"], sales_count=p["sales_count"]
    )
    print(f"Ajouté: {p['name']}")

for p in products_electromenager:
    Product.objects.create(
        name=p["name"], slug=p["slug"], category=cat_electromenager, subcategory=p["subcat"],
        price=p["price"], supplier=p["supplier"], rating=p["rating"], image=p["image"],
        is_new=p["is_new"], sales_count=p["sales_count"]
    )
    print(f"Ajouté: {p['name']}")

for p in products_pc:
    Product.objects.create(
        name=p["name"], slug=p["slug"], category=cat_pc, subcategory=p["subcat"],
        price=p["price"], supplier=p["supplier"], rating=p["rating"], image=p["image"],
        is_new=p["is_new"], sales_count=p["sales_count"]
    )
    print(f"Ajouté: {p['name']}")

for p in products_textile:
    Product.objects.create(
        name=p["name"], slug=p["slug"], category=cat_textile, subcategory=p["subcat"],
        price=p["price"], supplier=p["supplier"], rating=p["rating"], image=p["image"],
        is_new=p["is_new"], sales_count=p["sales_count"]
    )
    print(f"Ajouté: {p['name']}")

for p in products_artisanat:
    Product.objects.create(
        name=p["name"], slug=p["slug"], category=cat_artisanat, subcategory=p["subcat"],
        price=p["price"], supplier=p["supplier"], rating=p["rating"], image=p["image"],
        is_new=p["is_new"], sales_count=p["sales_count"]
    )
    print(f"Ajouté: {p['name']}")

print("Peuplement terminé avec succès !")