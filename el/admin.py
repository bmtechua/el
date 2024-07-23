from django.contrib import admin
from .models import Customer, UnitOfMeasurement

# Register your models here.
admin.site.register(UnitOfMeasurement),
admin.site.register(Customer),
