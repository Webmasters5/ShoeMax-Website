from django.urls import path
from . import views

# cart/urls.py
app_name = 'cart'

urlpatterns=[
    path('', views.cart_summary, name="cart_summary"),
    path('checkout/', views.checkout, name="checkout"),
    path('search/', views.search_view, name="search"),
]
