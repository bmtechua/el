from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, CartItem, Category, UnitOfMeasurement, Cart, UserVisit, SiteVisitCounter
from .forms import CustomerForm, CustomUserCreationForm, CustomAuthenticationForm, ProductForm, CategoryForm, UnitOfMeasurementForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    is_admin = request.user.groups.filter(
        name='administrator').exists() if request.user.is_authenticated else False
    is_manager = request.user.groups.filter(
        name='manager').exists() if request.user.is_authenticated else False
    is_customer = request.user.groups.filter(
        name='user').exists() if request.user.is_authenticated else False

    context = {
        'is_admin': is_admin,
        'is_manager': is_manager,
        'is_customer': is_customer
    }
    return redirect('work/product/product_list.html')


@login_required
def home1(request):
    SiteVisitCounter.increment()
    UserVisit.increment_visit_count(request.user)
    return render(request, 'home.html')


@login_required
def home(request):
    SiteVisitCounter.increment()
    UserVisit.increment_visit_count(request.user)
    # Отримуємо всі продукти та категорії
    customer = Customer.objects.all()
    products = Product.objects.all()
    categories = Category.objects.all()

    # Перевіряємо ролі користувача
    is_admin = request.user.groups.filter(name='Admin').exists()
    is_manager = request.user.groups.filter(name='Manager').exists()
    is_customer = request.user.groups.filter(name='Customer').exists()

    print(f"User: {request.user.username}")

    # Додаємо відлагодження у вигляді виводу на консоль
    print('is_admin:', is_admin)
    print('is_manager:', is_manager)
    print('is_customer:', is_customer)
    print('is empty')

    context = {
        'customer': customer,
        'products': products,
        'categories': categories,
        'is_admin': is_admin,
        'is_manager': is_manager,
        'is_customer': is_customer
    }

    return render(request, 'work/home.html', context)


def create_customer(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to success page or another view
            return redirect('home')
    else:
        form = CustomerForm()

    context = {
        'form': form,
    }
    return render(request, 'work/customer/create_customer.html', context)

# registration


def register_view(request, group_name):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'group_name': group_name})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data.get(
                'username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()

    is_admin = request.user.groups.filter(
        name='administrator').exists() if request.user.is_authenticated else False
    is_manager = request.user.groups.filter(
        name='manager').exists() if request.user.is_authenticated else False
    is_customer = request.user.groups.filter(
        name='user').exists() if request.user.is_authenticated else False

    return render(request, 'work/registration/login.html', {
        'form': form,
        'is_admin': is_admin,
        'is_manager': is_manager,
        'is_customer': is_customer
    })


def profile(request):
    return render(request, 'registration/profile.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def group_required(*group_names):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


@login_required
@group_required('administrator')
def admin_view(request):
    return render(request, 'admin_dashboard.html')


@login_required
@group_required('manager')
def manager_view(request):
    return render(request, 'manager_dashboard.html')


@login_required
@group_required('user')
def customer_view(request):
    return render(request, 'customer_dashboard.html')

# product


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'work/product/add_product.html', {'form': form})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'work/product/add_category.html', {'form': form})


def add_unit(request):
    if request.method == 'POST':
        form = UnitOfMeasurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unit_list')
    else:
        form = UnitOfMeasurementForm()
    return render(request, 'work/product/add_unit.html', {'form': form})


def change_product(request):
    category_form = CategoryForm()
    product_form = ProductForm()
    unit_form = UnitOfMeasurementForm()

    if request.method == 'POST':
        if 'product_submit' in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
                return redirect('product_list')

        if 'category_submit' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('product_list')

        if 'unit_submit' in request.POST:
            unit_form = UnitOfMeasurementForm(request.POST)
            if unit_form.is_valid():
                unit_form.save()
                return redirect('product_list')

    context = {
        'product_form': product_form,
        'category_form': category_form,
        'unit_form': unit_form,
    }
    return render(request, 'work/product/change_product.html', context)


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'work/home.html', {'products': products, 'categories': categories})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'work/home.html', {'categories': categories})


def unit_list(request):
    units = UnitOfMeasurement.objects.all()
    return render(request, 'work/home.html', {'units': units})

# cart


@login_required
def add_to_cart_old(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

# registered user


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Get or create cart for the user
    cart, created = Cart.objects.get_or_create(user=user)

    # Update or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

# unregistered user


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Use session to store cart for unregistered users
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('view_cart')


@login_required
def view_cart_old(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'work/cart/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})

# preview for registered users


@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'work/cart/view_cart.html', {'items': items})

# preview for unregistered users


def view_cart(request):
    cart = request.session.get('cart', {})
    product_ids = list(cart.keys())
    products = Product.objects.filter(id__in=product_ids)

    items = [{'product': product, 'quantity': cart[str(
        product.id)]} for product in products]

    return render(request, 'work/cart/view_cart.html', {'items': items})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


# counter global
def update_global_visit_count():
    SiteVisitCounter.increment()

# counter local


@login_required
def my_view(request):
    update_global_visit_count()
    UserVisit.increment_visit_count(request.user)

    visit_count = UserVisit.objects.get(user=request.user).visit_count
    global_visit_count = SiteVisitCounter.objects.first().visit_count

    return render(request, 'my_template.html', {
        'visit_count': visit_count,
        'global_visit_count': global_visit_count,
    })
