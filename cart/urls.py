from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name="summary"),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('search/', views.search_view, name="search"),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'), 
]
