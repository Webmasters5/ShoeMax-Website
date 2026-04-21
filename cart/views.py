import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from models_app.models import ShoeVariant, CartItem


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
    customer = request.user.customer_profile
    cart_items = customer.cart_items.all()

    total = sum(item.total_price for item in cart_items)
    discount = 0
    final_total = total - discount

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        "total": final_total,
        'customer': customer,
    })