from django.contrib import admin
from .models import Customer, UnitOfMeasurement, Product, Cart, CartItem

# Register your models here.
admin.site.register(UnitOfMeasurement),
admin.site.register(Customer),
admin.site.register(Product),
admin.site.register(Cart),
admin.site.register(CartItem),
