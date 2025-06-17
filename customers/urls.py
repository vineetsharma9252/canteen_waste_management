# customers/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('customer/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customer/add/', views.customer_create, name='customer_create'),
]
