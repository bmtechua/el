from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm

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
