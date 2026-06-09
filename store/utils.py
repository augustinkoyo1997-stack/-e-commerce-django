# store/utils.py
from django.utils import timezone
from .models import MonthlySales, Product

def record_sale(product_id, quantity):
    """
    Enregistre une vente pour un produit dans le mois courant.
    Incrémente le champ quantity_sold pour la ligne MonthlySales correspondante.
    """
    product = Product.objects.get(id=product_id)
    now = timezone.now()
    # Premier jour du mois à 00:00:00
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    sale, created = MonthlySales.objects.get_or_create(
        product=product,
        month=first_day,
        defaults={'quantity_sold': quantity}
    )
    if not created:
        sale.quantity_sold += quantity
        sale.save()
    return sale