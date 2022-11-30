from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from carts.views import _cart_id
from carts.models import Cart, CartItem
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
    return render(request, 'accounts/dashboard.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        # messages.success(request, 'You are successfully logged out ')
        return redirect('home')
    return redirect('home')