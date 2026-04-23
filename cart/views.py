import json
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from models_app.models import *
from .forms import *


# ─────────────────────────────────────────────
# ADD TO CART (UNCHANGED - SAFE)
# ─────────────────────────────────────────────
def add_to_cart(request):
    variant_id = request.POST.get('variant')
    variant = get_object_or_404(ShoeVariant, variant_id=variant_id)

    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        customer = request.user.customer_profile

        cart_item, created = CartItem.objects.get_or_create(
            customer=customer,
            variant=variant,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    else:
        cart = request.session.get('cart', {})
        key = str(variant.variant_id)
        cart[key] = int(cart.get(key, 0)) + 1
        request.session['cart'] = cart

    return redirect('cart:summary')


# ─────────────────────────────────────────────
# CART SUMMARY (UNCHANGED - HTML RENDER)
# ─────────────────────────────────────────────
def cart_summary(request):

    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        customer = request.user.customer_profile
        cart_items = CartItem.objects.filter(customer=customer)

        total = sum(item.total_price for item in cart_items)
        discount = 0
        final_total = total - discount

        return render(request, 'cart/summary.html', {
           'cart_items': cart_items,
           'subtotal': total,
           'discount': discount,
           'total': final_total,
        })

    session_cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for variant_id, qty in session_cart.items():
        variant = ShoeVariant.objects.filter(variant_id=variant_id).first()
        if not variant:
            continue

        item_total = variant.shoe.price * int(qty)
        total += item_total

        cart_items.append({
            'id': variant.variant_id,
            'variant': variant,
            'quantity': int(qty),
            'total_price': item_total,
        })

    discount = 0
    final_total = total - discount

    return render(request, 'cart/summary.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        "total": final_total,
    })

def cart_summary_api(request):
    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        customer = request.user.customer_profile
        totals = _calculate_totals(customer)  # must be fresh query
    else:
        cart = request.session.get('cart', {})
        totals = _calculate_session_totals(cart)

    return JsonResponse(totals)

@login_required
@require_POST
def apply_promo(request):
    promo_code = (request.POST.get('promo_code') or '').strip()
    if not promo_code:
        return JsonResponse({
            'success': False,
            'error': 'Please enter a promo code.'
        }, status=400)

    promo = Promo.objects.filter(promo_code__iexact=promo_code).first()
    if not promo or not promo.is_valid():
        return JsonResponse({
            'success': False,
            'error': 'Promo code not found or expired.'
        }, status=404)

    request.session['promo_id'] = promo.id
    customer = request.user.customer_profile
    cart_items = customer.cart_items.all()
    subtotal = sum(item.total_price for item in cart_items)
    discount = (subtotal * promo.percent_off / Decimal('100')).quantize(Decimal('0.01'))
    final_total = subtotal - discount

    return JsonResponse({
        'success': True,
        'promo_code': promo.promo_code,
        'discount': str(discount),
        'subtotal': str(subtotal),
        'final_total': str(final_total),
        'message': f'Promo code "{promo.promo_code}" applied successfully.'
    })
# ─────────────────────────────────────────────
# UPDATE QUANTITY (AJAX + fallback support)
# ─────────────────────────────────────────────
def update_quantity(request, item_id):

    action = None

    # AJAX JSON support
    action = request.POST.get("action")

    # ── LOGGED IN USER ─────────────────────────
    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        item = get_object_or_404(
            CartItem,
            id=item_id,
            customer=request.user.customer_profile
        )

        if action not in ["increment", "decrement"]:
         return JsonResponse({"error": "Invalid action"}, status=400)

        if action == "increment":
            item.quantity += 1
        elif action == "decrement":
            item.quantity -= 1

        removed = False

        if item.quantity <= 0:
            item.delete()
            removed = True
            quantity = 0
            item_total = 0
        else:
            item.save()
            quantity = item.quantity
            item_total = item.total_price

        totals = _calculate_totals(request.user.customer_profile)

        # AJAX response
        if request.method == "POST":
            return JsonResponse({
                "removed": removed,
                "quantity": quantity,
                "item_total": item_total,
                "totals": totals
            })

        return redirect('cart:summary')


    # ── SESSION USER ───────────────────────────
    cart = request.session.get('cart', {})
    key = str(item_id)

    if key not in cart:
        return redirect('cart:summary')

    qty = int(cart[key])

    if action == "increment":
        qty += 1
    elif action == "decrement":
        qty -= 1

    removed = False

    if qty <= 0:
        cart.pop(key)
        removed = True
        qty = 0
        item_total = 0
    else:
        cart[key] = qty
        variant = ShoeVariant.objects.filter(variant_id=key).first()
        item_total = variant.shoe.price * int(qty) if variant else 0

    request.session['cart'] = cart

    totals = _calculate_session_totals(cart)

    if request.method == "POST":
        return JsonResponse({
            "removed": removed,
            "quantity": qty,
            "item_total": item_total,
            "totals": totals
        })

    return redirect('cart:summary')


# ─────────────────────────────────────────────
# REMOVE ITEM (AJAX + fallback)
# ─────────────────────────────────────────────
def remove_from_cart(request, item_id):

    if request.method != "POST":
        return redirect('cart:summary')

    # LOGGED IN USER
    if request.user.is_authenticated and hasattr(request.user, 'customer_profile'):
        item = get_object_or_404(
            CartItem,
            id=item_id,
            customer=request.user.customer_profile
        )
        item.delete()

        totals = _calculate_totals(request.user.customer_profile)

        if request.method == "POST":
           return JsonResponse({
                "removed": True,
                "totals": totals
            })

        return redirect('cart:summary')

    # SESSION USER
    cart = request.session.get('cart', {})
    cart.pop(str(item_id), None)
    request.session['cart'] = cart

    totals = _calculate_session_totals(cart)

    if request.content_type == "application/json":
        return JsonResponse({
            "removed": True,
            "totals": totals
        })

    return redirect('cart:summary')


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def _calculate_totals(customer):
    items = CartItem.objects.filter(customer=customer)

    subtotal = sum(i.total_price for i in items)
    discount = 0
    final_total = subtotal - discount

    return {
        "subtotal": subtotal,
        "discount": discount,
        "total": final_total
    }


def _calculate_session_totals(cart):
    subtotal = 0
    for variant_id, qty in cart.items():
        variant = ShoeVariant.objects.filter(variant_id=variant_id).first()
        if variant:
            subtotal += variant.shoe.price * int(qty)

    discount = 0
    final_total = subtotal - discount

    return {
        "subtotal": subtotal,
        "discount": discount,
        "total": final_total
    }


@login_required
def checkout(request):
    from django.contrib import messages
    from decimal import Decimal
    from models_app.models import Address, PaymentMethod, Order, OrderItem, Notification, Promo

    customer = request.user.customer_profile
    cart_items = customer.cart_items.all()
    addresses = customer.addresses.all()
    payment_methods = customer.payment_methods.all()

    subtotal = sum(item.total_price for item in cart_items)

    # ─────────────────────────────
    # PROMO (UNIFIED SYSTEM)
    # ─────────────────────────────
    promo_id = request.session.get('promo_id')
    applied_promo = None
    discount = Decimal('0.00')

    if promo_id:
        try:
            applied_promo = Promo.objects.get(id=promo_id)
            if applied_promo.is_valid():
                discount = (subtotal * applied_promo.percent_off / Decimal('100')).quantize(Decimal('0.01'))
            else:
                del request.session['promo_id']
        except Promo.DoesNotExist:
            del request.session['promo_id']

    final_total = subtotal - discount

    # ─────────────────────────────
    # FORMS
    # ─────────────────────────────
    contact_form = ContactForm(initial={
        'full_name': customer.full_name,
        'email': request.user.email,
        'phone': customer.phone or '',
    })

    shipping_form = AddressForm(prefix='shipping')
    billing_form = AddressForm(prefix='billing')
    payment_form = PaymentMethodForm()

    shipping_selected = 'new'
    billing_selected = 'same'
    payment_selected = 'new'

    # ─────────────────────────────
    # PLACE ORDER
    # ─────────────────────────────
    if request.method == 'POST' and 'place_order' in request.POST:

        contact_form = ContactForm(request.POST)

        shipping_existing = request.POST.get('shipping_existing')
        billing_existing = request.POST.get('billing_existing')
        payment_existing = request.POST.get('payment_existing')

        shipping_selected = shipping_existing or 'new'
        billing_selected = billing_existing or 'same'
        payment_selected = payment_existing or 'new'

        valid = True

        if not contact_form.is_valid():
            valid = False

        # SHIPPING
        if shipping_existing != 'new':
            shipping_address = Address.objects.filter(addr_id=shipping_existing, customer=customer).first()
            if not shipping_address:
                valid = False
        else:
            shipping_form = AddressForm(request.POST, prefix='shipping')
            if shipping_form.is_valid():
                shipping_address = shipping_form.save(commit=False)
                shipping_address.customer = customer
                shipping_address.save()
            else:
                valid = False

        # BILLING
        if billing_existing == 'same':
            billing_address = shipping_address
        elif billing_existing != 'new':
            billing_address = Address.objects.filter(addr_id=billing_existing, customer=customer).first()
            if not billing_address:
                valid = False
        else:
            billing_form = AddressForm(request.POST, prefix='billing')
            if billing_form.is_valid():
                billing_address = billing_form.save(commit=False)
                billing_address.customer = customer
                billing_address.save()
            else:
                valid = False

        # PAYMENT
        if payment_existing == 'new':
            payment_form = PaymentMethodForm(request.POST)
            if payment_form.is_valid():
                payment_method = payment_form.save(commit=False)
                payment_method.customer = customer
                payment_method.save()
            else:
                valid = False
        elif payment_existing == 'cod':
            payment_method = None
        else:
            payment_method = PaymentMethod.objects.filter(card_id=payment_existing, customer=customer).first()
            if not payment_method:
                valid = False

        # FINAL CHECK
        if not valid:
            return render(request, 'cart/checkout.html', {
                'cart_items': cart_items,
                'subtotal': subtotal,
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
                'applied_promo': applied_promo,
            })

        # CREATE ORDER
        order = Order.objects.create(
            customer=customer,
            status='Pending',
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment_method=payment_method,
            subtotal=subtotal,
            discount_amount=discount,
            total_price=final_total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                price=item.variant.shoe.price
            )

            if item.variant.stock >= item.quantity:
                item.variant.stock -= item.quantity
                item.variant.save()

        cart_items.delete()

        # clear promo after use
        if 'promo_id' in request.session:
            del request.session['promo_id']

        Notification.objects.create(
            customer=customer,
            message=f"Your order #{order.order_id} has been placed successfully!",
            related_order=order
        )

        messages.success(request, "Order placed successfully!")
        return redirect('customer:customer_orders')

    # ─────────────────────────────
    # RENDER
    # ─────────────────────────────
    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
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
        'applied_promo': applied_promo,
    })
