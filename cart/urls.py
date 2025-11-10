from django.urls import path
from . import views

urlpatterns=[
    #cart
    path('',views.cart_summary,name="cart_summary"),
    path('add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    #checkout
    path('checkout/',views.checkout,name="checkout"),
    
    #search
    path("search/", views.search_view, name="search"),

]