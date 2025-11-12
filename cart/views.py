from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import ShoeVariant
from .models import CartItem
from customer.models import Customer, Order, OrderItem, Notification

@login_required
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ShoeVariant, variant_id=variant_id)
    customer = request.user.customer

    cart_item, created = CartItem.objects.get_or_create(
        customer=customer,
        variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_summary')


@login_required
def cart_summary(request):
    customer = request.user.customer
    cart_items = CartItem.objects.filter(customer=customer)

    total = sum(item.total_price for item in cart_items)
    discount = 0
    final_total = total - discount

    return render(request, 'cart/cart_summary.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, customer=request.user.customer)
    item.delete()
    return redirect('cart:cart_summary')


@login_required
def checkout(request):
    customer = request.user.customer
    cart_items = CartItem.objects.filter(customer=customer)

    if request.method == 'POST':
        # calculate totals
        total = sum(item.total_price for item in cart_items)
        discount = 0
        final_total = total - discount

        # get form data
        shipping_address = request.POST.get('address') or customer.shipping_address
        billing_address = request.POST.get('billing_address') or customer.billing_address
        payment_method = request.POST.get('payment', 'N/A')  # optional if you want to track

        # create Order
        order = Order.objects.create(
            customer=customer,
            total_price=final_total,
            shipping_address=shipping_address,
            billing_address=billing_address,
            status='Pending',
        )

        # create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_name=f"{item.variant.shoe.name} — {item.variant.color} (Size {item.variant.size})",
                quantity=item.quantity,
                 price=item.variant.shoe.price
            )

        # create notification
        Notification.objects.create(
            customer=customer,
            message=f"Your order #{order.id} has been confirmed!",
            related_order=order
        )

        # clear cart
        cart_items.delete()

        return redirect('customer:customer_orders')  # or a confirmation page

    # GET request: show checkout page
    total = sum(item.total_price for item in cart_items)
    discount = 0
    final_total = total - discount

    context = {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
        'customer': customer
    }
    return render(request, 'cart/checkout.html', context)


def search_view(request):
    query = request.GET.get("q")
    results = []

    if query:
        results = [f"Result for '{query}'"]

    return render(request, "search_results.html", {"query": query, "results": results})
