from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Product, CartItem, Category, UnitOfMeasurement, Cart, Order, OrderItem, UserVisit, SiteVisitCounter, Work
from .forms import CustomerForm, CustomUserCreationForm, CustomAuthenticationForm, ProductForm, CategoryForm, UnitOfMeasurementForm, WorkForm, OrderForm, OrderStatusForm
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
    return redirect('work/work.html')


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

    return render(request, 'work/work.html', context)


def work(request):
   # Логіка для отримання товарів та іншого контексту
    cart_count = get_cart_count(request)

    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'cart_count': cart_count,
        'categories': categories
    }
    return render(request, 'work/work.html', context)


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
            return redirect('work')
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
                return redirect('work')
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
    return render(request, 'home.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('work')


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
    # Логіка для отримання товарів та іншого контексту
    cart_count = get_cart_count(request)

    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    context = {
        'products': products,
        'cart_count': cart_count,
        'categories': categories
    }
    return render(request, 'work/work.html', context)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'work/home.html', {'categories': categories})


def unit_list(request):
    units = UnitOfMeasurement.objects.all()
    return render(request, 'work/home.html', {'units': units})

# cart

# registered user


def add_to_cart_for_reg(request, product_id):
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


def add_to_cart_for_unreg(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Use session to store cart for unregistered users
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('view_cart')


def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)
        user = request.user

        if user.is_authenticated:
            # Для зареєстрованих користувачів
            cart, created = Cart.objects.get_or_create(user=user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # Для незареєстрованих користувачів
            cart = request.session.get('cart', {})
            if product_id in cart:
                cart[product_id] += quantity
            else:
                cart[product_id] = quantity
            request.session['cart'] = cart

        return redirect('view_cart')

# preview for registered users


@login_required
def view_cart(request):

    orders = Order.objects.filter(user=request.user)

    # Перевірка, чи є користувач менеджером або адміністратором
    is_manager_or_admin = request.user.groups.filter(
        name__in=['manager', 'administrator']).exists()

    cart = get_object_or_404(Cart, user=request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)

    context = {'orders': orders,
               'items': items,
               'is_manager_or_admin': is_manager_or_admin,
               'total': total,
               }
    return render(request, 'work/cart/view_cart.html', context)

# preview for unregistered users


def view_cart(request):
    cart_count = 0
    cart_items = []
    total = 0

    if request.user.is_authenticated:
        # Обробка корзини для авторизованих користувачів
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = cart_items.count()
            total = sum(item.total_price() for item in cart_items)

        # Отримання замовлень користувача з деталями
        orders = Order.objects.filter(
            user=request.user).prefetch_related('items__product')

        context = {'cart_items': cart_items, 'total': total,
                   'cart_count': cart_count, 'orders': orders}
    else:
        # Обробка корзини для неавторизованих користувачів
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': product.price * quantity,
            })
            total += product.price * quantity
        cart_count = len(cart_items)
        context = {'cart_items': cart_items,
                   'total': total, 'cart_count': cart_count}

    return render(request, 'work/cart/view_cart.html', context)


def get_cart_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return CartItem.objects.filter(cart=cart).count()
    else:
        cart = request.session.get('cart', {})
        return len(cart)  # Кількість товарів у сесії
    return 0


def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))

        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, id=item_id)
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart = request.session.get('cart', {})
            if item_id in cart:
                cart[item_id] = quantity
                request.session['cart'] = cart

    return redirect('view_cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    customer = None
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            use_existing_data = form.cleaned_data.pop('use_existing_data')
            if use_existing_data and customer:
                order = Order.objects.create(
                    user=request.user,
                    first_name=customer.first_name,
                    last_name=customer.last_name,
                    email=customer.email,
                    phone_number=customer.phone_number,
                    address=customer.address
                )
            else:
                order = form.save(commit=False)
                order.user = request.user
                order.save()

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_items.delete()

            return redirect('order_success')
    else:
        initial_data = {}
        if customer:
            initial_data = {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'phone_number': customer.phone_number,
                'address': customer.address
            }
        form = OrderForm(initial=initial_data)

    return render(request, 'work/cart/checkout.html', {'form': form, 'cart_items': cart_items})


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


def clear_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            CartItem.objects.filter(cart=cart).delete()
    else:
        request.session['cart'] = {}

    return redirect('view_cart')

# checkout


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)  # Отримання корзини
    # Отримання всіх товарів в корзині
    cart_items = CartItem.objects.filter(cart=cart)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # Зв'язати товар з замовленням
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Очистити корзину
            cart_items.delete()

            return redirect('order_success')
    else:
        form = OrderForm()

    return render(request, 'work/cart/checkout.html', {'form': form, 'cart_items': cart_items})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'work/cart/order_confirmation.html', {'order': order})


def order_success(request):
    return render(request, 'work/cart/order_success.html')


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'work/order_detail.html', context)


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


def is_administrator(user):
    return user.groups.filter(name='administrator').exists()


def is_manager(user):
    return user.groups.filter(name__in=['manager', 'administrator']).exists()


@login_required
@user_passes_test(is_manager)
def manager_orders(request):
    orders = Order.objects.all()  # Отримати всі замовлення
    return render(request, 'work/manager_orders.html', {'orders': orders})


@login_required
@user_passes_test(is_administrator)
def admin_cabinet(request):
    return render(request, 'work/admin_cabinet.html')


@login_required
@user_passes_test(is_manager)
def manager_cabinet(request):
    return render(request, 'work/manager_cabinet.html')


@login_required
def user_cabinet(request):
    if request.user.groups.filter(name='user').exists():
        return render(request, 'work/user_cabinet.html')
    return redirect('login')


def some_view(request):
    is_admin = request.user.groups.filter(name='administrator').exists()
    is_manager = request.user.groups.filter(name='manager').exists()
    is_user = request.user.groups.filter(name='user').exists()

    context = {
        'is_admin': is_admin,
        'is_manager': is_manager,
        'is_user': is_user,
        # Додайте інші змінні, які вам потрібні
    }

    return render(request, 'index.html', context)


@login_required
@user_passes_test(is_manager)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'update_order_status.html', {'form': form, 'order': order})


@login_required
@user_passes_test(is_manager)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'work/cart/order_detail.html', {'order': order})


@login_required
@user_passes_test(is_manager)
def edit_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('manager_orders')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'work/cart/edit_order_status.html', {'form': form, 'order': order})


def our_works(request):
    works = Work.objects.all()
    return render(request, 'work/our_works.html', {'works': works})


def admin_cabinet(request):
    product_form = ProductForm()
    category_form = CategoryForm()
    unit_form = UnitOfMeasurementForm()
    work_form = WorkForm()

    if request.method == 'POST':
        if 'product_submit' in request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product_form.save()
        elif 'category_submit' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
        elif 'unit_submit' in request.POST:
            unit_form = UnitOfMeasurementForm(request.POST)
            if unit_form.is_valid():
                unit_form.save()
        elif 'work_submit' in request.POST:
            work_form = WorkForm(request.POST, request.FILES)
            if work_form.is_valid():
                work_form.save()

    context = {
        'product_form': product_form,
        'category_form': category_form,
        'unit_form': unit_form,
        'work_form': work_form,
    }
    return render(request, 'work/admin_cabinet.html', context)
