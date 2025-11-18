from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from models_app.models import Customer, Order
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect
from models_app.models import Notification  # assuming you have this model

# Only staff users can access
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff, login_url='/accounts/login/')(view_func)

@staff_required
def dashboard(request):
    total_customers = Customer.objects.count()
    total_orders = Order.objects.count()
    delivered_orders = Order.objects.filter(status='Delivered').count()
    pending_orders = Order.objects.filter(status='Pending').count()
    return render(request, 'adminpanel/dashboard.html', {
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
    })
"""
@staff_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'adminpanel/customers.html', {'customers': customers})

@staff_required
def order_list(request):
    orders = Order.objects.all().select_related('customer')
    return render(request, 'adminpanel/orders.html', {'orders': orders})

@staff_required
def notifications(request):
    return render(request, 'adminpanel/notifications.html')

@staff_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'adminpanel/order_detail.html', {'order': order})

@staff_required
def notifications(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/notifications.html', {'notifications': notifications})

@staff_required
def delete_notification(request, notif_id):
    notif = get_object_or_404(Notification, id=notif_id)
    notif.delete()
    return redirect('adminpanel:notifications') """