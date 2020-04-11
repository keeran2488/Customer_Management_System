from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import *
from .models import *
from .filters import OrderFilter


# Create your views here.


def loginPage(request):

    context = {

    }

    return render(request, 'accounts/login.html', context)


def registerPage(request):

    context = {

    }

    return render(request, 'accounts/register.html', context)


def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()

    context={
        'customers': customers,
        'orders' : orders,
        'total_orders' : total_orders,
        'orders_delivered' : orders_delivered,
        'orders_pending' : orders_pending,
    }
    return render(request,"accounts/dashboard.html", context)


def products(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, "accounts/products.html", context)


def customers(request, pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()

    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context={
        'customer':customer,
        'orders':orders,
        'total_orders':total_orders,
        'myFilter':myFilter,
    }

    return render(request, "accounts/customer.html", context)


def createOrder(request):
    form = OrderForm()

    if request.method ==  "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context={
        'form':form
    }

    return render(request, "accounts/order_form.html", context)



def updateOrder(request, pk):
    order = Order.objects.get(id = pk)

    form = OrderForm(instance=order)

    if request.method ==  "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context={
        'form':form,
    }

    return render(request,"accounts/order_form.html", context)


def deleteOrder(request, pk):
    order = Order.objects.get(id = pk)

    if request.method == "POST":
        order.delete()
        return redirect("/")

    context={
        'item': order,
    }

    return render(request, "accounts/delete.html", context)
