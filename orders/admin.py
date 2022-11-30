from django.contrib import admin
from orders.models import Payment, Order, OrderCar
# Register your models here.

class OrderCarInline(admin.TabularInline):
    model = OrderCar
    readonly_fields = ('payment', 'user', 'car', 'quantity',  'car_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter  = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderCarInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderCar)