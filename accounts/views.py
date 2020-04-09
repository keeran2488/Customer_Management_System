from django.shortcuts import render
from django.http import HttpResponse

from .models import *


# Create your views here.


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


def customers(request):
    return HttpResponse("Customers")
