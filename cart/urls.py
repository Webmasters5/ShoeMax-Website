from django.urls import path
from . import views

urlpatterns=[
    #cart
    path('',views.cart_summary,name="cart_summary"),

    #checkout
    path('checkout/',views.checkout,name="checkout"),
    
    #search
    path("search/", views.search_view, name="search"),

]