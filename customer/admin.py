from django.contrib import admin

# Register your models here.
from .models import Customer

from .models import Order, OrderItem, Notification

admin.site.register(Customer)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(Notification)