from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),

    path('register/<str:group_name>/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('login/', LoginView.as_view(template_name='work/registration/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('create_customer/', views.create_customer, name='create_customer'),
]
