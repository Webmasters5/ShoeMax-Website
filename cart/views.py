from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from models_app.models import ShoeVariant
from models_app.models import CartItem
from models_app.models import Order, OrderItem, Notification
from models_app.models import Address, PaymentMethod
from django.core.exceptions import ValidationError
from .forms import AddressForm, PaymentMethodForm, ContactForm
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
def add_to_cart(request):
    variant_id = request.POST.get('variant')
    variant = get_object_or_404(ShoeVariant, variant_id=variant_id)
    customer = request.user.customer_profile

    cart_item, created = CartItem.objects.get_or_create(
        customer=customer,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:summary')


@login_required
def cart_summary(request):
    customer = request.user.customer_profile
    cart_items = CartItem.objects.filter(customer=customer)

    total = sum(item.total_price for item in cart_items)
    discount = 0
    final_total = total - discount

    return render(request, 'cart/summary.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, customer=request.user.customer_profile)
    item.delete()
    return redirect('cart:summary')

@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, customer=request.user.customer_profile)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increment':
            item.quantity += 1
            item.save()
            
        elif action == 'decrement':
            if item.quantity > 1: 
                item.quantity -= 1
                item.save()

    return redirect('cart:summary')

@login_required
def checkout(request):
    customer = request.user.customer_profile
    cart_items = customer.cart_items.all()  # via related name
    addresses = customer.addresses.all()
    payment_methods = customer.payment_methods.all()

    # Prefill contact from the logged-in user
    contact_initial = {
        'full_name': customer.full_name,
        'email': request.user.email,
        'phone': customer.phone or '',
    }
    contact_form = ContactForm(initial=contact_initial)
    shipping_form = AddressForm(prefix='shipping')
    billing_form = AddressForm(prefix='billing')
    payment_form = PaymentMethodForm()
    # defaults for select inputs (used to preserve selection on errors)
    shipping_selected = 'new'
    billing_selected = 'same'
    payment_selected = 'new'

    if request.method == 'POST' and 'place_order' in request.POST:
        # Bind forms only as needed
        contact_form = ContactForm(request.POST)
        shipping_existing = request.POST.get('shipping_existing')
        billing_existing = request.POST.get('billing_existing')
        payment_existing = request.POST.get('payment_existing')

        # preserve what the user selected so we can re-render the selects on error
        shipping_selected = shipping_existing or 'new'
        billing_selected = billing_existing or 'same'
        payment_selected = payment_existing or 'new'

        # Validate contact
        valid = True
        if not contact_form.is_valid():
            valid = False

        # Create correct shipping address instance
        shipping_address_obj = None
        if shipping_existing and shipping_existing != 'new':
            try:
                shipping_address_obj = Address.objects.get(addr_id=shipping_existing, customer=customer)
            except Address.DoesNotExist:
                valid = False
                shipping_form.add_error(None, 'Selected shipping address not found.')
        else:
            shipping_form = AddressForm(request.POST, prefix='shipping')
            if shipping_form.is_valid():
                shipping_address_obj = shipping_form.save(commit=False)
                # Do not attach to customer for order-only address
                shipping_address_obj.customer = None
                shipping_address_obj.save()
            else:
                valid = False

        # Create correct billing address instance
        billing_address_obj = None
        if billing_existing == 'same':
            billing_address_obj = shipping_address_obj
        elif not billing_existing or billing_existing == 'new':
            billing_form = AddressForm(request.POST, prefix='billing')
            if billing_form.is_valid():
                billing_address_obj = billing_form.save(commit=False)
                # Do not attach to customer for order-only address
                billing_address_obj.customer = None
                billing_address_obj.save()
            else:
                billing_form.add_error(None, 'Invalid billing address.')
        else:
            try:
                billing_address_obj = Address.objects.get(addr_id=billing_existing, customer=customer)
            except Address.DoesNotExist:
                valid = False
                billing_form.add_error(None, 'Selected billing address not found.')

        # Validate payment: prefer 'new' payment, then COD, then existing-selection lookup
        payment_method_obj = None

        if payment_existing == 'new':
            payment_form = PaymentMethodForm(request.POST)
            if not payment_form.is_valid():
                valid = False
            else:
                payment_method_obj = payment_form.save(commit=False)
                payment_method_obj.customer = None
                payment_method_obj.save()
        elif payment_existing == 'cod':
            # Cash on delivery: explicitly no payment method object
            payment_method_obj = None
        elif payment_existing:
            try:
                payment_method_obj = PaymentMethod.objects.get(card_id=payment_existing, customer=customer)
            except PaymentMethod.DoesNotExist:
                valid = False
                payment_form.add_error(None, 'Selected payment method not found.')
        else:
            # No payment option picked
            valid = False
            payment_form.add_error(None, 'Please select a payment method.')

        if not valid:
            total = sum(item.total_price for item in cart_items)
            discount = 0
            final_total = total - discount
            return render(request, 'cart/checkout.html', {
                'cart_items': cart_items,
                'total': total,
                'discount': discount,
                'final_total': final_total,
                'customer': customer,
                'addresses': addresses,
                'payment_methods': payment_methods,
                # forms with errors
                'contact_form': contact_form,
                'shipping_form': shipping_form,
                'billing_form': billing_form,
                'payment_form': payment_form,
                'shipping_selected': shipping_selected,
                'billing_selected': billing_selected,
                'payment_selected': payment_selected,
            })

        # Create order using Address FKs
        total = sum(item.total_price for item in cart_items)
        discount = 0
        final_total = total - discount

        order = Order.objects.create(
            customer=customer,
            total_price=final_total,
            shipping_address=shipping_address_obj,
            billing_address=billing_address_obj,
            payment_method=payment_method_obj,
            status='Pending',
            discount_amount=0.00,
            subtotal=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                price=item.variant.shoe.price,
            )

        Notification.objects.create(
            customer=customer,
            message=f"Your order #{order.order_id} has been confirmed!",
            related_order=order,
        )

        # Clear cart
        cart_items.delete()

        return redirect('customer:customer_orders')

    # GET: render checkout
    total = sum(item.total_price for item in cart_items)
    discount = 0
    final_total = total - discount

    context = {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
        'customer': customer,
        'addresses': addresses,
        'payment_methods': payment_methods,
        'contact_form': contact_form,
        'shipping_form': shipping_form,
        'billing_form': billing_form,
        'payment_form': payment_form,
        'shipping_selected': shipping_selected,
        'billing_selected': billing_selected,
        'payment_selected': payment_selected,
    }
    return render(request, 'cart/checkout.html', context)
