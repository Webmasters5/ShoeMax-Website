from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customer_list, name='customers'),
    path('orders/', views.order_list, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/delete/<int:notif_id>/', views.delete_notification, name='delete_notification'),
]