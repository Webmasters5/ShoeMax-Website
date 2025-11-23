from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'customer'

urlpatterns = [
    path("profile/", views.profile, name="customer_profile"),
    path("info/", views.info, name="customer_info"),
    path("orders/", views.orders, name="customer_orders"),
    path("orders/<int:order_id>/", views.order_detail, name="customer_order_detail"),
    path("password/", views.password, name="customer_password"),
    path("notifications/", views.notifications, name="customer_notifications"),
    path("notifications/mark-read/<int:notification_id>/", views.mark_notification_read, name="mark_notification_read"),
    path("notifications/mark-all/", views.mark_all_notifications_read, name="mark_all_notifications_read"),
    path("settings/", views.settings, name="customer_settings"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
