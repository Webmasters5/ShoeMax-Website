from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("profile/", views.profile, name="customer_profile"),
    path("info/", views.info, name="customer_info"),
    path("orders/", views.orders, name="customer_orders"),
    path("orders/<int:order_id>/", views.order_detail, name="customer_order_detail"),
    path("password/", views.password, name="customer_password"),
    path("notifications/", views.notifications, name="customer_notifications"),
    path("settings/", views.settings, name="customer_settings"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
