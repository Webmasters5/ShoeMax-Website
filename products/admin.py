from django.contrib import admin
from .models import Shoe, ShoeVariant, Brand, Customer, Order, OrderItem, Reviews

# Register your models here.
admin.site.register(Shoe)
admin.site.register(ShoeVariant)
admin.site.register(Brand)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Reviews)