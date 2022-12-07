from django.shortcuts import render, redirect, get_object_or_404
from cars.models import Car
from carts .models import Cart , CartItem, Wishlist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart



def add_cart(request, id):
    current_user = request.user
    car = Car.objects.get(id=id)

    if current_user.is_authenticated:
        is_cart_item_exists = CartItem.objects.filter(car=car, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.get(car=car, user=current_user)
            cart_item.quantity += 1
            cart_item.save()

        else:
            item = CartItem.objects.create(car=car, quantity=1, user=current_user)
            item.save()
        return redirect('cart')
    
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(car=car, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(car=car, cart=cart)
            cart_item.quantity += 1
            cart_item.save()

        else:
            item = CartItem.objects.create(car=car, quantity=1,cart=cart)
            item.save()
        return redirect('cart')

    



def remove_cart(request, id, cart_item_id):
     
    car = get_object_or_404(Car, id=id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(car=car, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(car=car, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1                                                                                                       
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, id, cart_item_id):
    car = get_object_or_404(Car, id=id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(car=car, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(car=car, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
 
def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.car.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        
    }
    
    return render(request, 'carts/cart.html', context)

@login_required(login_url = 'login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.car.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        
    }
    return render(request, 'carts/checkout.html', context)

def view_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context={
        'wishlist':wishlist,
    }
    return render(request, 'carts/wishlist.html',context)

# def add_wishlist(request, id):
#     car= Car.objects.get(id=id)
#     print(car)
#     if request.user.is_authenticated:
#         wishlist = Wishlist.objects.filter(user=request.user)
#     if Wishlist.objects.filter(car=car,user=request.user).exists():
#        messages.success(request, 'Car is present in the Wishlist !!..')
#     else:
#         Wishlist.objects.create(car=car,user=request.user)
#         messages.success(request, 'Car is added to Wishlist !!..')
#     return redirect("wishlist")

def add_wishlist(request, id):
    current_user = request.user
    car = Car.objects.get(id=id)

    if current_user.is_authenticated:
        is_wishlist_item_exists = Wishlist.objects.filter(car=car, user=current_user).exists()
        if is_wishlist_item_exists:
            wishlist_item = Wishlist.objects.get(car=car, user=current_user)
            wishlist_item += 1
            wishlist_item.save()

        else:
            item = Wishlist.objects.create(car=car, user=current_user)
            item.save()
        return redirect('wishlist')
    
    else:
       pass

def remove_wishlist(request, id):
    wishlist = Wishlist.objects.get(user=request.user, car_id=id)
    print('fdf')
    if wishlist:
        wishlist.delete()
    return redirect("wishlist")