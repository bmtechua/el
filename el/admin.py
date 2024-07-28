from django.contrib import admin
from .models import Customer, UnitOfMeasurement, Product, Cart, CartItem, UserVisit, SiteVisitCounter
from django.contrib.sessions.models import Session

# Register your models here.
admin.site.register(UnitOfMeasurement),
admin.site.register(Customer),
admin.site.register(Product),
admin.site.register(Cart),
admin.site.register(CartItem),


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'session_data', 'expire_date')
    search_fields = ('session_key',)
    list_filter = ('expire_date',)


@admin.register(SiteVisitCounter)
class SiteVisitCounterAdmin(admin.ModelAdmin):
    list_display = ('user', 'visit_count')
    change_list_template = 'admin/sitevisitcounter/change_list.html'


@admin.register(UserVisit)
class UserVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'visit_count')
    search_fields = ('user__username',)
