from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Shoe)
admin.site.register(models.ShoeVariant)
admin.site.register(models.Brand)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Review)