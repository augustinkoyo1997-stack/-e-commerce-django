from django.shortcuts import render, redirect
from django.http import JsonResponse
from store.models import Product   # ✅ correction ici

def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok', 'cart_count': sum(cart.values())})
        return redirect('cart_view')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_update(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        if quantity <= 0:
            cart.pop(str(product_id), None)
        else:
            cart[str(product_id)] = quantity
        request.session['cart'] = cart
        return redirect('cart_view')

def cart_view(request):
    return render(request, 'cart/cart.html')

def cart_detail(request):
    """Affiche le contenu du panier"""
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=int(product_id))
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'cart/cart.html', {'cart_items': items, 'total': total})

def add_to_cart(request):
    """Ajoute un produit au panier (via POST)"""
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
        request.session['cart'] = cart
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok', 'cart_count': sum(cart.values())})
        return redirect('cart_detail')

def remove_from_cart(request, product_id):
    """Retire un produit du panier"""
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart_detail')

def update_cart(request, product_id):
    """Met à jour la quantité d'un produit"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        cart = request.session.get('cart', {})
        if quantity <= 0:
            cart.pop(str(product_id), None)
        else:
            cart[str(product_id)] = quantity
        request.session['cart'] = cart
        return redirect('cart_detail')