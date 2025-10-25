from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from . import models
#from django.http import HttpResponse

# Create your views here.
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

