# payments/views.py
import json
import stripe
import logging
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from store.models import Product
from orders.models import Order, OrderItem
from store.utils import record_sale   # votre fonction utilitaire

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@require_http_methods(["POST"])
def create_checkout_session(request):
    try:
        body = request.body.decode('utf-8')
        if not body:
            return JsonResponse({'error': 'Corps vide'}, status=400)

        data = json.loads(body)
        cart_items = data.get('cart')
        if not cart_items:
            return JsonResponse({'error': 'Panier manquant'}, status=400)

        line_items = []
        for item in cart_items:
            product_id = item.get('id')
            quantity = item.get('quantity')
            if not product_id or not quantity:
                return JsonResponse({'error': 'Produit ou quantité manquant'}, status=400)

            try:
                product = Product.objects.get(id=int(product_id))
            except Product.DoesNotExist:
                return JsonResponse({'error': f'Produit {product_id} introuvable'}, status=404)

            line_items.append({
                'price_data': {
                    'currency': 'xof',
                    'unit_amount': int(product.price),
                    'product_data': {'name': product.name},
                },
                'quantity': int(quantity),
            })

        success_url = request.build_absolute_uri('/payments/success/')
        cancel_url = request.build_absolute_uri('/payments/cancel/')

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return JsonResponse({'url': session.url})

    except json.JSONDecodeError as e:
        logger.error(f"JSON invalide : {e}")
        return JsonResponse({'error': 'JSON invalide'}, status=400)
    except stripe.error.StripeError as e:
        logger.error(f"Erreur Stripe : {e}")
        return JsonResponse({'error': f'Stripe : {str(e)}'}, status=400)
    except Exception as e:
        logger.error(f"Erreur inattendue : {e}")
        return JsonResponse({'error': f'Erreur interne : {str(e)}'}, status=500)

def payment_success(request):
    """Page affichée après un paiement réussi."""
    return render(request, 'payments/success.html')

def payment_cancel(request):
    """Page affichée si l'utilisateur annule le paiement."""
    return render(request, 'payments/cancel.html')

@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=100)
        total = session['amount_total']

        order = Order.objects.create(
            status='paid',
            total_amount=total,
            stripe_payment_intent_id=session['payment_intent'],
        )

        for item in line_items:
            product_name = item['description']
            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                continue
            quantity = item['quantity']
            price = item['amount_total'] // quantity
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )
            record_sale(product.id, quantity)

    return HttpResponse(status=200)