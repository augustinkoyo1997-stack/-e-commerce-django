import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from cart.views import *
from .models import Order, OrderItem
from .forms import OrderCreateForm  # formulaire simple pour adresse
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY

def order_create(request):
    cart = get_cart(request)
    if not cart.items.exists():
        return redirect('store:product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Créer la commande à partir du panier
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            order.total_amount = cart.total_price()
            order.save()

            # Copier les articles du panier vers OrderItem
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity,
                )

            # Vider le panier
            cart.items.all().delete()

            # Créer la session Stripe Checkout
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {'name': f'Commande {order.id}'},
                        'unit_amount': int(order.total_amount * 100),  # en centimes
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('orders:payment_success')),
                cancel_url=request.build_absolute_uri(reverse('orders:payment_cancel')),
                metadata={'order_id': order.id},
            )
            # Stocker l'ID de session dans la session Django
            request.session['stripe_session_id'] = session.id
            return redirect(session.url, code=303)
    else:
        # Pré-remplir avec les infos de l'utilisateur si connecté
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial)
    return render(request, 'orders/create.html', {'form': form, 'cart': cart})

def payment_success(request):
    return render(request, 'orders/success.html')

def payment_cancel(request):
    return render(request, 'orders/cancel.html')