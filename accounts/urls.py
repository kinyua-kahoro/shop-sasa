from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk_customer>/', views.customers, name='customer'),
    path('create_order/<str:pk_create_order>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk_update_order>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk_delete_order>/', views.deleteOrder, name='delete_order'),
]