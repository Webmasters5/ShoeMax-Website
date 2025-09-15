from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.
def product_details(request, product_id):
    # Create a dummy brand object
    class DummyBrand:
        def __init__(self):
            self.name = "Nike"
    
    # Create dummy variant objects
    class DummyVariant:
        def __init__(self, variant_id, color, size, stock):
            self.variant_id = variant_id
            self.color = color
            self.size = size
            self.stock = stock
    
    # Create dummy variants list
    variants = [
        DummyVariant(1, "Black", 8, 15),
        DummyVariant(2, "White", 8, 10),
        DummyVariant(3, "Black", 9, 8),
        DummyVariant(4, "White", 9, 12),
        DummyVariant(5, "Red", 10, 5),
    ]
    
    # Create dummy variants manager
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
    
    context = {
        'product': product,
        'product_id': product_id
    }
    
    return render(request, 'details.html', context)
