# orders/forms.py
from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'shipping_address']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse de livraison (rue, code postal, ville)', 'rows': 3}),
        }