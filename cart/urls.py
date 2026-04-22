"""from django.urls import path
from . import views
from .views import cart_summary_api
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name="summary"),
    path('add/', views.add_to_cart, name='add_item'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_item'),
    path('checkout/', views.checkout, name="checkout"),
    path("summary/api/", cart_summary_api, name="cart_summary_api"),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'), 
   
    path('api/token/', obtain_auth_token),
]"""


from django.urls import path
from . import views
from .views import cart_summary_api
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name="summary"),
    path('add/', views.add_to_cart, name='add_item'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_item'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path("summary/api/", cart_summary_api, name="cart_summary_api"),
    path('checkout/', views.checkout, name="checkout"),
    path('api/token/', obtain_auth_token),
]