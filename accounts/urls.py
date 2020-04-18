from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('user/', views.userPage, name = 'user-page'),
    path('account/', views.accountSettings, name="account"),

    path('',views.home, name="home"),
    path('product/',views.products, name="product"),
    path('cutomer/<str:pk>/',views.customers, name="customer"),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
]
