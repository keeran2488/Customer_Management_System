from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
from .filters import OrderFilter


# Create your views here.


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username or Password invalid!")

        context = {

        }

        return render(request, 'accounts/login.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data("username")
                messages.success(request, "Account was created for " + user)
                return redirect("login")

        context = {
            'form':form,
        }

        return render(request, 'accounts/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
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


@login_required(login_url="login")
def products(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request, "accounts/products.html", context)


@login_required(login_url="login")
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


@login_required(login_url="login")
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


@login_required(login_url="login")
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


@login_required(login_url="login")
def deleteOrder(request, pk):
    order = Order.objects.get(id = pk)

    if request.method == "POST":
        order.delete()
        return redirect("/")

    context={
        'item': order,
    }

    return render(request, "accounts/delete.html", context)
