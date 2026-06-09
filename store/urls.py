from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # ← ajoutez cette ligne pour la racine
    path('api/products/', views.api_products, name='api_products'),
    path('categorie/<slug:category_slug>/', views.category_products, name='category_products'),
    path('produit/<slug:slug>/', views.product_detail, name='product_detail'),
    path('api/record-sale/', views.api_record_sale, name='api_record_sale'),
    path('produit/<slug:slug>/', views.product_detail, name='product_detail'),
]