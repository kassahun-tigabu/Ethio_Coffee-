from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from products.models import CoffeeProduct
from .models import Cart, CartItem
from .utils import get_or_create_cart

def cart_detail(request):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all(),
    }
    return render(request, 'cart/detail.html', context)

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(CoffeeProduct, id=product_id)
    cart = get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_total': cart.total_items,
            'item_total': cart_item.total_price,
        })
    
    return redirect('cart:detail')

@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=get_or_create_cart(request))
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart_item.cart.total_items,
            'item_total': cart_item.total_price,
            'cart_subtotal': cart_item.cart.total_price,
        })
    
    return redirect('cart:detail')

@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=get_or_create_cart(request))
    cart_item.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_total': cart_item.cart.total_items,
            'cart_subtotal': cart_item.cart.total_price,
        })
    
    return redirect('cart:detail')