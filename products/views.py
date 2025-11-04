from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q,Avg
from .models import Shoe,ShoeVariant,Review,OrderItem
from .forms import Reviewform
#from django.http import HttpResponse

# Create your views here.
def product_details(request, product_id):

    class DummyBrand:
        def __init__(self):
            self.name = "Nike"
    
    class DummyVariant:
        def __init__(self, variant_id, color, size, stock):
            self.variant_id = variant_id
            self.color = color
            self.size = size
            self.stock = stock
    
    variants = [
        DummyVariant(1, "Black", 8, 15),
        DummyVariant(2, "White", 8, 10),
        DummyVariant(3, "Black", 9, 8),
        DummyVariant(4, "White", 9, 12),
        DummyVariant(5, "Red", 10, 5),
    ]
    
    class DummyVariantsManager:
        def all(self):
            return variants
    
    # Create dummy image field
    class DummyImageField:
        def __init__(self):
            self.url = "/static/images/nike-shoe-sample.jpg"
    
    # Create a dummy product object with all required attributes
    class DummyProduct:
        def __init__(self):
            self.shoe_id = product_id
            self.name = "Nike Air Max 270"
            self.price = 129.99
            self.brand = DummyBrand()
            self.color = "Black/White"
            self.size = 8
            self.gender = "Men"
            self.category = "Running Shoes"
            self.description = "The Nike Air Max 270 delivers visible Air cushioning from heel to toe. Inspired by the Air Max 93 and Air Max 180, the 270 features Nike's biggest heel Air unit yet for a super-soft ride that feels as impossible as it looks."
            self.image_url = DummyImageField()
            self.variants = DummyVariantsManager()
    
    product = DummyProduct()

    shoe=get_object_or_404(Shoe,shoe_id=product_id) #added this
    reviews=Review.objects.filter(order_item__variant__shoe=shoe)
    avg_rating = reviews.aggregate(average=Avg('rating'))['average']
    
    context = {
        'product': product,
        'product_id': product_id,
        'avg_rating': avg_rating
    }

    
    return render(request, 'details.html', context)


def search(request):
    """
    Basic search page for Shoe models with filters:
    - q: search text across name and description
    - category: exact match on Shoe.category
    - min_price, max_price: numeric filters on Shoe.price
    """
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    shoes = Shoe.objects.all()

    if q:
        shoes = shoes.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    if category:
        shoes = shoes.filter(category__iexact=category)

    # Defensive parsing of price inputs
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
        Shoe.objects.exclude(category__isnull=True)
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

def reviews(request,product_id):
    shoe=get_object_or_404(Shoe,shoe_id=product_id)
    reviews=Review.objects.filter(order_item__variant__shoe=shoe)
    avg_rating = reviews.aggregate(average=Avg('rating'))['average']
    context={
        'shoe':shoe,
        'reviews':reviews,
        'avg_rating':avg_rating,
    }
    return render(request,'reviews.html',context)
#@login_required
def review_product(request,product_id):
    shoe=get_object_or_404(Shoe,shoe_id=product_id)
    if request.method =='POST':
        form=Reviewform(request.POST)
        if form.is_valid():
            Review=form.save(commit=False)
            order_item=OrderItem.objects.filter(variant__shoe=shoe, order__customer__user=request.user)
            if order_item:
                Review.order_item = order_item
                Review.save()
                return redirect('products:reviews',product_id=shoe.shoe_id)
            else:
                form.add_error(None, 'You must purchase the product to review it.')
    else:
        form=Reviewform()
    context={
        'shoe':shoe,
        'form':form,
    }
    return render(request,'reviewform.html',context)

def dummy(request):
    shoe=Shoe.objects.all()
    return render(request,'dummy.html',{'shoes':shoe})