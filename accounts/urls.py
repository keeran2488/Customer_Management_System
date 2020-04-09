from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('product/',views.products, name="product"),
    path('cutomer/<str:pk>/',views.customers, name="customer"),
]
