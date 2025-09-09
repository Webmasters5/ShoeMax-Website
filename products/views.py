from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def product_details(request, product_id):
    return HttpResponse(f'Product {product_id} details')
