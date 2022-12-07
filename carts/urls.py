from django.urls import path
from .import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('wishlist',views.view_wishlist, name='wishlist'),
    path('addwishlist/<int:id>/', views.add_wishlist , name='addwishlist'),
    path('remove/<int:id>/', views.remove_wishlist , name='remove_wishlist'),
    path('checkout', views.checkout, name='checkout'),
]
