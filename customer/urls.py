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
    path("orders/<int:order_id>/cancel/", views.cancel_order, name="customer_order_cancel"),
    path("password/", views.password, name="customer_password"),
    path("notifications/", views.notifications, name="customer_notifications"),
    path("payment-methods/", views.payment_methods, name="customer_payment_methods"),
    # Class-based views for payment methods
    path('payment-methods/list/', views.PaymentMethodListView.as_view(), name='paymentmethod_list'),
    path('payment-methods/add/', views.PaymentMethodCreateView.as_view(), name='paymentmethod_add'),
    path('payment-methods/<int:pk>/', views.PaymentMethodDetailView.as_view(), name='paymentmethod_detail'),
    path('payment-methods/<int:pk>/edit/', views.PaymentMethodUpdateView.as_view(), name='paymentmethod_edit'),
    path('payment-methods/<int:pk>/delete/', views.PaymentMethodDeleteView.as_view(), name='paymentmethod_delete'),
    path('payment-methods/<int:pk>/set-default/', views.set_default_payment_method, name='paymentmethod_set_default'),
    path("notifications/mark-read/<int:notification_id>/", views.mark_notification_read, name="mark_notification_read"),
    path("notifications/mark-all/", views.mark_all_notifications_read, name="mark_all_notifications_read"),
    path("settings/", views.settings, name="customer_settings"),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
