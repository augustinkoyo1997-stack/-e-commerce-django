from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    # Nouveaux produits
    new_products = Product.objects.filter(is_new=True)[:8]

    # Top ventes (version temporaire : les 6 plus récents)
    # Remplacez ceci par votre logique MonthlySales si nécessaire
    top_products = Product.objects.order_by('-created_at')[:6]

    all_products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'new_products': new_products,
        'top_products': top_products,
        'all_products': all_products,
        'categories': categories,
    }
    return render(request, 'store/home.html', context)

def category_products(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    # Si votre modèle Category possède un champ 'subcategories', décommentez la ligne suivante
    # subcategories = category.subcategories.all()
    subcategories = []  # Valeur par défaut

    context = {
        'category': category,
        'products': products,
        'subcategories': subcategories,
    }
    return render(request, 'store/category.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

# store/views.py
# store/views.py
# store/views.py
from django.http import JsonResponse
from .models import Product

def api_products(request):
    products = Product.objects.all()
    data = []
    for p in products:
        # URL de l'image : si absente, image par défaut
        image_url = p.image.url if p.image else 'https://via.placeholder.com/200x150?text=Image+manquante'
        data.append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'category': p.category.name,
            'subCategory': p.subcategory.name if p.subcategory else '',
            'supplier': p.supplier,
            'rating': float(p.rating),
            'image': image_url,
            'isNew': p.is_new,
            'salesCount': p.sales_count,
        })
    return JsonResponse(data, safe=False)


# store/views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.utils import timezone


@csrf_exempt  # uniquement en développement ; en production utilisez une vraie clé CSRF
def api_record_sale(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        product = Product.objects.get(id=product_id)
        now = timezone.now()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        sale, created = MonthlySales.objects.get_or_create(
            product=product,
            month=first_day,
            defaults={'quantity_sold': quantity}
        )
        if not created:
            sale.quantity_sold += quantity
            sale.save()

        return JsonResponse({'status': 'ok', 'message': f'Vente enregistrée pour {product.name}'})

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Produit introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def product_detail(request, slug):
    """Affiche la page détail d'un produit"""
    product = get_object_or_404(Product, slug=slug)
    # Récupérer les produits similaires (même catégorie)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {
        'product': product,
        'similar_products': similar_products,
    }
    return render(request, 'store/product_detail.html', context)