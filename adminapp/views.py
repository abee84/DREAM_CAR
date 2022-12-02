from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from cars . models import Car
from contacts .models import Contact
from orders.models import OrderCar, Payment
from .forms import AddCarForm, UpdateCarForm
from orders.views import payments


# Create your views here.
def admin_dashboard(request):
    return render(request, 'adminapp/index.html')

@login_required(login_url="admin_signin")
def admin_home(request):
    users = User.objects.filter(is_superuser=False)
    context = {
        'users': users,
    }
    return render(request, 'adminapp/userdashboard.html', context)
    

def contacted_user(request):
    
    user = Contact.objects.all()
    print(user)
    context = {
        'user': user,
    }
    return render(request, 'adminapp/contacted_user.html', context)




@login_required(login_url="admin_signin")
def car_list(request):
    cars = Car.objects.all()
    context = {
        'cars': cars,
    }
    return render(request, 'adminapp/cars.html', context)



def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(
            username=username, password=password
        )

        if user is not None and user.is_superuser:
            # request.session["key"] = "value"
            auth.login(request, user)
            messages.success(request, "Admin Online")
            return redirect("admin_home")
        else:
            messages.error(request, "You are not an admin")
            return redirect("admin_signin")
    messages.error(request,'Invalid Entry')
    return render(request, "adminapp/signin.html")


@login_required(login_url="admin_signin")
def signout(request):
    auth.logout(request)
    return redirect("admin_signin")
    # if request.session.has_key("key"):
    #     del request.session["key"]
    #     request.session.modified = True
    # return redirect("admin_signin")



def user_block(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect("admin_home")

def user_unblock(request, id):
    user = User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect("admin_home")

def order_car(request):
    order_car=OrderCar.objects.all()
    context = {
        'ordercar': order_car,
    }
    return render(request, 'adminapp/ordercar.html', context)



def change_status(request,id):
    if request.method == 'POST':
        status=request.POST['status']
        car= OrderCar.objects.get(id=id)
        car.status=status
        car.save()
        return redirect('order_car')

def update_car(request,id):
    car=Car.objects.get(id=id)
    form= UpdateCarForm(instance= car)
    if request.method == "POST":
        form= UpdateCarForm(request.POST, request.FILES , instance= car)
        if form.is_valid():
            form.save()
            
            return redirect('product-list')
    
    context= {'form':form}
    return render(request, 'adminapp/update_car.html',context)

def add_car(request):
    print('jfjf')
    form = AddCarForm()
    if request.method == "POST":
        print('dxdg')
        form= AddCarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print('vnbbvb')
    context={'form':form}

    return render(request, 'adminapp/add_car.html', context)

def dash(request):
    New=0
    Accepted=0
    Completed=0
    Cancelled=0
    cars=Car.objects.all().count()
    users=User.objects.all().count()
    sales=OrderCar.objects.all().count()
    revenue= Payment.objects.all()
    amount=0
    for i in revenue:
        amount+=float(i.amount_paid)
    amt=round(amount,2)
    labels=[]
    data=[]

    queryset= OrderCar.objects.all().order_by('-created_at')
    for car in queryset:
        if car.status == 'New':
            New+=1
        elif car.status == 'Accepted':
            Accepted+=1
        elif car.status == 'Completed':
            Completed+=1
        else:
            Cancelled+=1

    print(New)
    print(Accepted)
    print(Completed)
    print(Cancelled)

    labels=["New","Accepted","Completed","Cancelled"]
    data=[New,Accepted,Completed,Cancelled]
         
    
    context={
        'product_count':cars,
        'user_count' : users,
        'sales_count' : sales,
        'revenue' : amt,
        'data':data,
        'labels':labels,
    }
    return render(request,'adminapp/admindash.html',context)