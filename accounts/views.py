from django.shortcuts import render, redirect
from accounts.models import Customer, Product, Order
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from accounts.filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    latest_orders = Order.objects.order_by('-date_created')[:5]
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'latest_orders':latest_orders , 'customers': customers, 'total_customers': total_customers, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_customer):
    customer = Customer.objects.get(id =pk_customer)
    orders = customer.order_set.all()
    orders_count = orders.count()
    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs
    context = {'customer': customer, 'orders': orders, 'orders_count': orders_count, 'orderFilter': orderFilter}
    return render(request, 'accounts/customers.html', context)

@login_required(login_url='login')
def createOrder(request, pk_create_order):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    customer = Customer.objects.get(id =pk_create_order)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk_update_order):
    order = Order.objects.get(id =pk_update_order)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk_delete_order):
    order = Order.objects.get(id =pk_delete_order)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'total_orders': total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSetttings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form }
    return render(request, 'accounts/account_settings.html', context)
