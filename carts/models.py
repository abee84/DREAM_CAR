from django.db import models
from cars.models import Car
from django.contrib.auth.models import User
from contacts.models import Contact
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=255,null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.cart_id) or ''


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.car.price * self.quantity


    def __str__(self):
        return str(self.car) or ''


class Wishlist(models.Model):
    car=models.ForeignKey(Car, on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) or ''