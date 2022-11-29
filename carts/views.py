from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from . models import Cart, CartItem
from django.http import  HttpResponse
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()

    return cart

def add_cart(request, product_id):
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            print(key, value)

    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request))

    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart = cart,
            quantity = 1,
        )
        cart_item.save()

    # return HttpResponse(cart_item.quantity)
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart = cart)

    if cart_item.quantity > 1 :
        cart_item.quantity = cart_item.quantity - 1
        cart_item.save()
    else:
        cart_item.delete()

    print(cart_item.quantity)

    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product, cart = cart)

    cart_item.delete()
    return redirect('cart')


def cart(request):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart)

        total = 0
        quantity = 0
        for cart_item in cart_items:
            total = total + (cart_item.product.price * cart_item.quantity)
            quantity =+ cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

        context = {
            'total':total,
            'quantity':quantity,
            'cart_items':cart_items,
            'tax':tax,
            'grand_total':grand_total,
        }
    except ObjectDoesNotExist:
        pass

    return render(request, 'store/cart.html', context)