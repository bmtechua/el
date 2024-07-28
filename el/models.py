from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class UnitOfMeasurement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    unit = models.ForeignKey(
        UnitOfMeasurement, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    items = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def total_price(self):
        return self.quantity * self.product.price


class SiteVisitCounter(models.Model):
    visit_count = models.PositiveIntegerField(default=0)
    # Додаємо поле для зберігання останнього відвідування
    last_visit = models.DateTimeField(null=True, blank=True)

    @classmethod
    def increment(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        obj.visit_count += 1
        obj.last_visit = timezone.now()  # Оновлюємо дату та час останнього відвідування
        obj.save()


class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(
        default=timezone.now)  # Додаємо поле дати та часу

    def __str__(self):
        return f'{self.user.username} - {self.visit_count}'

    @classmethod
    def increment_visit_count(cls, user):
        obj, created = cls.objects.get_or_create(user=user)
        obj.visit_count += 1
        obj.timestamp = timezone.now()  # Оновлюємо дату та час відвідування
        obj.save()
