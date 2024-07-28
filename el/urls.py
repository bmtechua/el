from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('work/', views.work, name='work'),
    path('product_list/', views.product_list, name='product_list'),
    path('my_view/', views.my_view, name='my_view'),

    path('register/<str:group_name>/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'),

    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category'),
    path('add_unit/', views.add_unit, name='add_unit'),

    path('change_product/', views.change_product, name='change_product'),
    path('change_product/<int:product_id>/',
         views.change_product, name='edit_product'),
    path('change_product/category/<int:category_id>/',
         views.change_product, name='edit_category'),
    path('change_product/unit/<int:unit_id>/',
         views.change_product, name='edit_unit'),

    path('product_list/', views.product_list, name='product_list'),
    path('category_list/', views.category_list, name='category_list'),
    path('unit_list/', views.unit_list, name='unit_list'),

    path('add-to-cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),

    # path('add_to_cart/<int:product_id>/',
    # views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/',
         views.remove_from_cart, name='remove_from_cart'),

    path('create_customer/', views.create_customer, name='create_customer'),
]
