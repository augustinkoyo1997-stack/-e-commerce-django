# download_product_images_pexels.py
import os
import requests
import django
import time

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product
from django.conf import settings

# ==== Configuration Pexels ====
PEXELS_API_KEY = "rYPFVLovPCOtnnsFFRqFVriQkEjg4hlTP13sDyBTwnBe019jX4yGqJpi"  # ⚠️ Remplacez par votre clé
PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"

def search_and_download_image(product_name, output_path):
    """Recherche une image sur Pexels et la sauvegarde localement."""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": product_name,
        "per_page": 1,                 # Une seule image par recherche
        "orientation": "square"        # Format carré
    }

    try:
        # 1. Recherche via l'API
        response = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # 2. Extraction de l'URL de la première image
        if data.get("photos"):
            image_url = data["photos"][0]["src"]["medium"]  # Taille moyenne
            img_response = requests.get(image_url)
            img_response.raise_for_status()

            # 3. Sauvegarde locale
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            print(f"✓ Téléchargée : {product_name}")
            return True
        else:
            print(f"✗ Aucune image trouvée pour : {product_name}")
            return False

    except Exception as e:
        print(f"✗ Erreur pour {product_name} : {e}")
        return False

def main():
    products = Product.objects.all()
    media_root = settings.MEDIA_ROOT
    products_dir = os.path.join(media_root, "products")
    os.makedirs(products_dir, exist_ok=True)

    # Limite pour ne pas surcharger l'API
    REQUESTS_PER_HOUR = 200
    DELAY_BETWEEN_CALLS = 3600 / REQUESTS_PER_HOUR  # ~18 secondes entre chaque appel

    for idx, product in enumerate(products):
        # Détermination du nom de fichier attendu (comme dans votre peuplement)
        image_rel_path = product.image.name if product.image else ""
        if not image_rel_path:
            filename = f"{product.slug}.jpg"
        else:
            filename = os.path.basename(image_rel_path)
        output_path = os.path.join(products_dir, filename)

        # Ignorer les images déjà présentes
        if os.path.exists(output_path):
            print(f"⏩ Déjà présent : {product.name}")
            continue

        # Construction de la requête : nom + catégorie
        search_query = f"{product.name} {product.category.name}"
        success = search_and_download_image(search_query, output_path)

        # Second essai sans catégorie si le premier échoue
        if not success:
            time.sleep(2)  # Petite pause avant le deuxième essai
            search_and_download_image(product.name, output_path)

        # Respect strict de la limite de requêtes
        time.sleep(DELAY_BETWEEN_CALLS)

if __name__ == "__main__":
    main()