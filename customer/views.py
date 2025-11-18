from django.shortcuts import render, redirect, get_object_or_404
from models_app.models import Customer, Order, OrderItem, Notification
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomerForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profile(request):
    customer = get_object_or_404(Customer, user=request.user)
    return render(request, "customer/profile.html", {"customer": customer})

# Use UserForm defined in customer.forms (remove local duplicate)
@login_required
def info(request):
    customer = request.user.customer

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        customer_form = CustomerForm(request.POST, instance=customer)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            return redirect("customer:customer_profile")
    else:
        user_form = UserForm(instance=request.user)
        customer_form = CustomerForm(instance=customer)

    return render(request, "customer/info.html", {
        "user_form": user_form,
        "customer_form": customer_form
    })

@login_required
def orders(request):
    orders = request.user.customer.orders.all()
    return render(request, "customer/orders.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    return render(request, "customer/order_detail.html", {"order": order})

@login_required
def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after changing password
            update_session_auth_hash(request, user)
            return redirect("customer:customer_profile")  # or another success page
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, "customer/password.html", {"form": form})

@login_required
def notifications(request):
    customer = request.user.customer
    notifications = customer.notifications.all().order_by('-created_at')
    return render(request, "customer/notifications.html", {"notifications": notifications})

@login_required
def settings(request):
    customer = request.user.customer
    if request.method == "POST":
        theme = request.POST.get("theme")
        if theme in ["light", "dark"]:
            customer.theme_preference = theme
            customer.save()
        return redirect("customer:customer_settings")
    return render(request, "customer/settings.html", {"customer": customer})

@login_required
def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id, customer=request.user.customer)
    notification.is_read = True
    notification.save()
    return redirect('customer:customer_notifications')

@login_required
def mark_all_notifications_read(request):
    notifications = request.user.customer.notifications.all()
    notifications.update(is_read=True)
    return redirect('customer:customer_notifications')