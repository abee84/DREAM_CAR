from django.shortcuts import render, redirect
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts.models import Cart, CartItem
from orders.models import Order, OrderCar
from cars.models import Car
import requests


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in!!.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                #next/cart/checkout
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextpage = params['next']
                    return redirect(nextpage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                   messages.error(request, 'Email already exists') 
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email= email, password=password)
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in.')
                    # return redirect("dashboard")
                    user.save()
                    messages.success(request, 'User created successfully!!.')
                    return redirect('login')
        else:
            messages.error(request, 'password doesnot match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    # userprofile = User.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        # 'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/order.html', context)

# def edit_profile(request):
#     user = request.user
#     userprofile = get_object_or_404(User, user=request.user)
#     if request.method == 'POST':
#         # user_form = UserForm(request.POST, instance=request.user)
#         # profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
#         if user.is_valid():
#             user.save()
#             messages.success(request, 'Your profile has been updated.')
#             return redirect('edit_profile')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = UserProfileForm(instance=userprofile)
#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'userprofile': userprofile,
#     }
#     return render(request, 'Users/edit_profile.html', context)


def order_detail(request, order_id):
    order_detail = OrderCar.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.car_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)


def cancel_order(request, id):
    car = OrderCar.objects.get(pk=id, user=request.user)
    car.status = "Cancelled"
    car.save()
    # item = Car.objects.get(pk=car.car.id)
    # item.stock += car.quantity
    # item.save()
    return redirect("my_orders")

@login_required(login_url= 'login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are successfully logged out ')
        return redirect('home')
    return redirect('home')