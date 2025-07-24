from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import Customer, Product, Order
from .forms import OrderForm
from django.forms import inlineformset_factory
from accounts.filters import OrderFilter


# Create your views here.
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

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def customers(request, pk_customer):
    customer = Customer.objects.get(id =pk_customer)
    orders = customer.order_set.all()
    orders_count = orders.count()
    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs
    context = {'customer': customer, 'orders': orders, 'orders_count': orders_count, 'orderFilter': orderFilter}
    return render(request, 'accounts/customers.html', context)

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

def deleteOrder(request, pk_delete_order):
    order = Order.objects.get(id =pk_delete_order)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
