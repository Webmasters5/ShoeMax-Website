from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from . import models
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
#from django.http import HttpResponse

# Create your views here.

@login_required
def add_wishlist_item(request, shoe_id):
    if request.method != "POST":
        return redirect('products:shoe_details', shoe_id=shoe_id)

    shoe = get_object_or_404(models.Shoe, pk=shoe_id)
    customer = request.user.customer_profile if request.user.is_authenticated else None    
    
    if not customer:
        return redirect('products:shoe_details', shoe_id=shoe_id)

    models.WishlistItem.objects.get_or_create(customer=customer, shoe=shoe)
    
    return redirect(shoe.get_absolute_url())

@login_required
def delete_wishlist_item(request, item_id):
    item = get_object_or_404(models.WishlistItem, pk=item_id)

    #customers can only delete their own wishlist items
    if not ((hasattr(item.customer, 'user') and item.customer.user == request.user)):
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        item.delete()

    return redirect(reverse('products:wishlist'))

class WishlistView(LoginRequiredMixin,generic.ListView):
    model = models.WishlistItem
    template_name = 'wishlist.html'
    context_object_name = 'wishlist_items'
    paginate_by = 5
    
    def get_queryset(self):
        qs = super().get_queryset().select_related('customer', 'shoe').prefetch_related('shoe__images')
        customer = self.request.user.customer_profile if self.request.user.is_authenticated else None
        if customer:
            return customer.wishlist_items.all()
        return qs.none()

def shoe_details(request, shoe_id):
    shoe = models.Shoe.objects.prefetch_related('images').get(pk=shoe_id)
       
    main_image = shoe.images.first() if shoe.images.exists() else None
    context = {'shoe': shoe, 'main_image': main_image}
    return render(request, 'details.html', context)

def search(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    shoes = models.Shoe.objects.all()

    if q:
        shoes = shoes.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    if category:
        shoes = shoes.filter(category__iexact=category)

    try:
        if min_price:
            shoes = shoes.filter(price__gte=float(min_price))
    except (TypeError, ValueError):
        pass

    try:
        if max_price:
            shoes = shoes.filter(price__lte=float(max_price))
    except (TypeError, ValueError):
        pass

    shoes = shoes.order_by('price', 'name')

    categories = (
        models.Shoe.objects.exclude(category__isnull=True)
        .exclude(category__exact='')
        .values_list('category', flat=True)
        .distinct()
        .order_by('category')
    )

    context = {
        'shoes': shoes,
        'categories': categories,
        'q': q,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
    }

    return render(request, 'search.html', context)