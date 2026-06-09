# payments/utils.py
from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation(order, customer_email):
    subject = f"Confirmation de commande #{order.id} - DipitaShop"
    message = f"""
    Bonjour,

    Votre commande #{order.id} a été confirmée.
    Montant total : {order.total_amount} CFA

    Merci de votre confiance !
    DipitaShop - Cotonou, Bénin
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [customer_email])