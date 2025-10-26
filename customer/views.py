from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer, Order, OrderItem
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomerForm, UserForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def profile(request):
    customer = get_object_or_404(Customer, user=request.user)
    return render(request, "customer/profile.html", {"customer": customer})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

def info(request):
    customer = request.user.customer

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        customer_form = CustomerForm(request.POST, instance=customer)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            return redirect("customer_profile")
    else:
        user_form = UserForm(instance=request.user)
        customer_form = CustomerForm(instance=customer)

    return render(request, "customer/info.html", {
        "user_form": user_form,
        "customer_form": customer_form
    })

def orders(request):
    orders = request.user.customer.orders.all()
    return render(request, "customer/orders.html", {"orders": orders})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    return render(request, "customer/order_detail.html", {"order": order})

def password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Keep the user logged in after changing password
            update_session_auth_hash(request, user)
            return redirect("customer_profile")  # or another success page
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, "customer/password.html", {"form": form})

def notifications(request):
    return render(request, "customer/notifications.html")

def settings(request):
    customer = request.user.customer
    if request.method == "POST":
        theme = request.POST.get("theme")
        if theme in ["light", "dark"]:
            customer.theme_preference = theme
            customer.save()
        return redirect("customer_settings")
    return render(request, "customer/settings.html", {"customer": customer})
