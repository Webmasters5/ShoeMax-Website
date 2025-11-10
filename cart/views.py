from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from models_app.models import ShoeVariant, CartItem, Customer
# Create your views here.

#cart
def cart_summary(request):
  return render(request,"cart_summary.html",{})
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


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, customer=request.user.customer_profile)
    item.delete()
    return redirect('cart_summary')

#checkout
def checkout(request):
  return render(request,"checkout.html",{})

#search
def search_view(request):
    query = request.GET.get("q")  # get ?q= value from URL
    results = []  # replace with real search logic (e.g. Product.objects.filter(...))

    if query:
        # Example if you had a Product model
        # results = Product.objects.filter(name__icontains=query)
        results = [f"Result for '{query}'"]  

    return render(request, "search_results.html", {"query": query, "results": results})
