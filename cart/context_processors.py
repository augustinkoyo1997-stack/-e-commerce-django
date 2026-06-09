def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, qty in cart.items():
        from store import Product
        product = Product.objects.get(id=int(product_id))
        items.append({'product': product, 'quantity': qty, 'total_price': product.price * qty})
        total += product.price * qty
    return {'cart_items': items, 'cart_total': total, 'cart_count': sum(cart.values())}