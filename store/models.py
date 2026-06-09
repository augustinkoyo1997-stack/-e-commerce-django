# store/models.py
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    """Catégorie mère (ex: Smartphone, Électronique, etc.)"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """Sous-catégorie (ex: iPhone, Samsung pour Smartphone)"""
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} / {self.name}"

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    price = models.IntegerField()  # en FCFA
    supplier = models.CharField(max_length=100)  # fournisseur
    rating = models.FloatField(default=4.5)  # note sur 5
    image = models.ImageField(upload_to='products/', default='products/default.jpg', blank=True)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # Pour gérer les ventes mensuelles, on aura un modèle séparé plus tard
    sales_count = models.IntegerField(default=0)  # total ventes (optionnel)
    # store/models.py (ajoutez ce champ dans la classe Product)
    stock = models.IntegerField(default=0, help_text="Quantité en stock")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# store/models.py
from django.db import models
from django.utils import timezone

class MonthlySales(models.Model):
    """Ventes mensuelles par produit"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='monthly_sales')
    month = models.DateField()   # premier jour du mois (ex: 2025-05-01)
    quantity_sold = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'month')   # un seul enregistrement par produit et mois

    def __str__(self):
        return f"{self.product.name} - {self.month.strftime('%b %Y')} : {self.quantity_sold}"