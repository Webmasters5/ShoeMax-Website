from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomerForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from models_app.models import Customer, Order, OrderItem, Notification
from django.urls import reverse 
from django.views.decorators.http import require_POST
from django.contrib import messages

def get_customer_or_redirect_login(request):
	# check for customer profile
	customer = getattr(request.user, "customer_profile", None)
	if not customer:
		return redirect('core:login')
	return customer

# Create your views here.
@login_required
def profile(request):
	customer = get_customer_or_redirect_login(request)
	
	if not isinstance(customer, Customer):
		return customer
	return render(request, "customer/profile.html", {"customer": customer})

# Use UserForm defined in customer.forms (remove local duplicate)
@login_required
def info(request):
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer

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
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer
	orders = customer.orders.all()
	return render(request, "customer/orders.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer
	order = get_object_or_404(Order, order_id=order_id, customer=customer)
	return render(request, "customer/order_detail.html", {"order": order})


@login_required
def cancel_order(request, order_id):
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer

	order = get_object_or_404(Order, order_id=order_id, customer=customer)

	# Only allow cancel if order is pending
	if order.status.lower() != 'pending':
		messages.error(request, "Only pending orders can be cancelled.")
		return redirect(reverse('customer:customer_order_detail', args=[order.order_id]))

	order.status = 'cancelled'
	order.save()

	# Create a notification for the customer
	Notification.objects.create(
		customer=customer,
		message=f"Your order #{order.order_id} has been cancelled.",
		related_order=order
	)

	messages.success(request, f"Order #{order.order_id} cancelled.")
	return redirect(reverse('customer:customer_orders'))

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
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer
	notifications = customer.notifications.all().order_by('-created_at')
	return render(request, "customer/notifications.html", {"notifications": notifications})

@login_required
def settings(request):
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer
	if request.method == "POST":
		theme = request.POST.get("theme")
		if theme in ["light", "dark"]:
			customer.theme_preference = theme
			customer.save()
		return redirect("customer:customer_settings")
	return render(request, "customer/settings.html", {"customer": customer})

@login_required
def mark_notification_read(request, notification_id):
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer
	notification = get_object_or_404(Notification, id=notification_id, customer=customer)
	notification.is_read = True
	notification.save()
	return redirect('customer:customer_notifications')

@login_required
def mark_all_notifications_read(request):
	customer = get_customer_or_redirect_login(request)
	if not isinstance(customer, Customer):
		return customer
	notifications = customer.notifications.all()
	notifications.update(is_read=True)
	return redirect('customer:customer_notifications')