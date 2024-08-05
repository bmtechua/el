from django import forms
from .models import Customer, Product, Category, UnitOfMeasurement, Order
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'address']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'unit']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class UnitOfMeasurementForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasurement
        fields = ['name', 'abbreviation']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'address']


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'executor']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
        }
