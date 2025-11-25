from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from models_app.models import ShoeVariant, CartItem, Customer, Coupon,OrderItem,Order
from decimal import Decimal
from django.contrib import messages
# Create your views here.

#cart


@login_required
def cart_summary(request):
    # Get or create the Customer profile for the logged-in user
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name or '',
            'last_name': request.user.last_name or '',
            'email': request.user.email or '',
            'phone_number': '',
            'address': '',
        }
    )

    # ✅ Use CartItem instead of Cart
    cart_items = CartItem.objects.filter(customer=customer)

    subtotal = sum(item.variant.shoe.price * item.quantity for item in cart_items)
    shipping = 5.00  # example fixed shipping fee
    discount = 0.00  # could come from coupon later
    total = subtotal + shipping - discount

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'discount': discount,
        'total': total,
    }

    return render(request, 'cart/cart.html', context)


#adding to cart
@login_required
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ShoeVariant, id=variant_id)
    customer = request.user.customer_profile

    cart_item, created = CartItem.objects.get_or_create(
        customer=customer,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_summary')

#calcualating total
@login_required
def cart_summary(request):
    customer = request.user.customer_profile
    cart_items = CartItem.objects.filter(customer=customer)

    total = sum(item.total_price for item in cart_items)
    discount = 0  # future: apply coupon logic
    final_total = total - discount

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
    })

#delete button
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, customer=request.user.customer_profile)
    item.delete()
    return redirect('cart_summary')

#checkout
def checkout(request):
  return render(request,"cart/checkout.html",{})

#coupon
@login_required
def checkout_view(request):
    try:
        customer = request.user.customer_profile
    except Customer.DoesNotExist:
        return redirect('create_customer_profile')  # Optional fallback

    cart_items = CartItem.objects.filter(customer=customer)
    subtotal = sum(item.variant.shoe.price * item.quantity for item in cart_items)

    # Apply discount if any
    discount_amount = Decimal('0.00')
    applied_coupon = None

    if request.GET.get('coupon'):
        code = request.GET.get('coupon')
        try:
            applied_coupon = Coupon.objects.get(promo_code=code, is_active=True)
            if applied_coupon.is_valid():
                discount_amount = (applied_coupon.percent_off / 100) * subtotal
        except Coupon.DoesNotExist:
            applied_coupon = None

    total = subtotal - discount_amount

    context = {
        'customer': customer,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount_amount,
        'total': total,
        'coupon': applied_coupon,
    }
    return render(request, 'checkout.html', context)



#passing payment
@login_required
def checkout_view(request):
    # Get the current user's cart items
    cart_items = CartItem.objects.filter(customer=request.user.customer_profile)
    
    # Calculate order totals
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    discount = 0  # Apply logic if you have discount rules
    shipping = 5 if subtotal > 0 else 0  # Example flat shipping fee
    total = subtotal - discount + shipping

    # Handle form submission (payment selection)
    if request.method == 'POST':
        payment_method = request.POST.get('payment')
        if not payment_method:
            messages.error(request, "Please select a payment method.")
        else:
            # Create order from cart items
            order = Order.objects.create(
                customer=request.user.customer_profile,
                total_price=total,
                payment_method=payment_method,
                shipping_fee=shipping,
                discount=discount
            )

            # Move cart items to order (example logic)
            for item in cart_items:
                order.items.create(
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            
            # Clear the cart
            cart_items.delete()

            messages.success(request, "Order placed successfully!")
            return redirect('order_confirmation', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'cart/checkout.html', context)

#total
@login_required
def place_order(request):
    customer = request.user.customer_profile
    cart_items = CartItem.objects.filter(customer=customer)

    if not cart_items.exists():
        return redirect('cart_summary')

    order = Order.objects.create(
        customer=customer,
        shipping_cost=Decimal('0.00'),
        sub_total=sum(item.variant.shoe.price * item.quantity for item in cart_items),
        discount_amount=Decimal('0.00'),
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            variant=item.variant,
            quantity=item.quantity,
            price=item.variant.shoe.price * item.quantity
        )

    # Clear the cart after order placed
    cart_items.delete()

    return redirect('order_success')



#search
def search_view(request):
    query = request.GET.get("q")  # get ?q= value from URL
    results = []  # replace with real search logic (e.g. Product.objects.filter(...))

    if query:
        # Example if you had a Product model
        # results = Product.objects.filter(name__icontains=query)
        results = [f"Result for '{query}'"]  

    return render(request, "search_results.html", {"query": query, "results": results})
