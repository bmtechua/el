from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm, CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group


# Create your views here.


def index(request):
    return redirect('home.html')


def home(request):
    customer = Customer.objects.all()
    context = {
        'customer': customer,
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
    return render(request, 'work/registration/register.html', {'form': form, 'group_name': group_name})


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
