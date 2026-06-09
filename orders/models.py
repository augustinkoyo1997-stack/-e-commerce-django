# orders/models.py
from django.db import models
from store.models import Product

class Order(models.Model):
    """Commande principale après paiement réussi"""
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('shipped', 'Expédié'),
        ('delivered', 'Livré'),
        ('cancelled', 'Annulé'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.IntegerField()  # montant total en FCFA
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    # Informations client (optionnel – à étendre plus tard)
    customer_name = models.CharField(max_length=100, blank=True)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    shipping_address = models.TextField(blank=True)

    def __str__(self):
        return f"Commande #{self.id}"

class OrderItem(models.Model):
    """Ligne de commande (produit, quantité, prix unitaire)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price = models.IntegerField()  # prix unitaire au moment de l'achat (en FCFA)

    def __str__(self):
        return f"{self.product.name if self.product else 'Produit supprimé'} x {self.quantity}"