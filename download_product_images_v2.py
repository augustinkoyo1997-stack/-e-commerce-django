import os
import requests
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from store.models import Product
from django.conf import settings

UNSPLASH_ACCESS_KEY = "OBqpsoZ04ep2_hT3LbVvWzpUWx38ftDZZP-xvoL8Sa4"
UNSPLASH_URL = "https://api.unsplash.com/search/photos"

def search_and_download_image(product_name, output_path):
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {
        "query": product_name,
        "per_page": 1,
        "orientation": "squarish"
    }
    try:
        response = requests.get(UNSPLASH_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            image_url = data["results"][0]["urls"]["small"]
            img_response = requests.get(image_url)
            img_response.raise_for_status()
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

    for idx, product in enumerate(products):
        image_rel_path = product.image.name if product.image else ""
        if not image_rel_path:
            filename = f"{product.slug}.jpg"
        else:
            filename = os.path.basename(image_rel_path)
        output_path = os.path.join(products_dir, filename)

        if os.path.exists(output_path):
            print(f"⏩ Déjà présent : {product.name}")
            continue

        # Pause de 2 secondes entre chaque requête
        time.sleep(2)

        search_query = f"{product.name} {product.category.name}"
        success = search_and_download_image(search_query, output_path)
        if not success:
            time.sleep(1)
            search_and_download_image(product.name, output_path)

if __name__ == "__main__":
    main()