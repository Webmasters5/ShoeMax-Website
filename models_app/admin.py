from django.contrib import admin
from models_app import models

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(models.Shoe)
admin.site.register(models.ShoeImage)
admin.site.register(models.ShoeVariant)
admin.site.register(models.Brand)
admin.site.register(models.Customer)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem)
admin.site.register(models.Notification)
admin.site.register(models.Review)
admin.site.register(models.Admin) 
admin.site.register(models.WishlistItem)
admin.site.register(models.CartItem)
