from django.contrib import admin
from .models import Customer, UnitOfMeasurement, Product, Cart, CartItem, UserVisit, SiteVisitCounter, Order, OrderItem, Work, Category
from django.contrib.sessions.models import Session

# Register your models here.


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'session_data', 'expire_date')
    search_fields = ('session_key',)
    list_filter = ('expire_date',)


@admin.register(SiteVisitCounter)
class SiteVisitCounterAdmin(admin.ModelAdmin):
    list_display = ('visit_count', 'last_visit')
    change_list_template = 'admin/sitevisitcounter/change_list.html'


@admin.register(UserVisit)
class UserVisitAdmin(admin.ModelAdmin):
    list_display = ('user', 'visit_count', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)


admin.site.register(UnitOfMeasurement),
admin.site.register(Customer),
admin.site.register(Product),
admin.site.register(Category),
admin.site.register(Cart),
admin.site.register(CartItem),
admin.site.register(Work),
