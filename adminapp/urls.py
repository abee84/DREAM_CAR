from django.urls import path
from .import views

urlpatterns = [
    path('', views.signin, name='admin_signin'),
    path('signout/', views.signout, name='signout'),
    path('home/', views.admin_home, name='admin_home'),
    path('contact/', views.contacted_user, name='contacted_user'),
    path('cars/',views.car_list , name='car-list'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('block/<int:id>/', views.user_block ,name='block' ),
    path('unblock/<int:id>/', views.user_unblock ,name='unblock' ),
    path('order/', views.order_car, name='order_car'),
    path('add/', views.add_car, name='add_car'),
    path('update/<int:id>/', views.update_car, name='update_car'),
    path('change/<int:id>/', views.change_status, name= 'change_status'),
    path('admindash/', views.dash, name='admindash'),
]
