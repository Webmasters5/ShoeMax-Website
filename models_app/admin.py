from django.contrib import admin
from models_app import models

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 1

class ShoeImageInline(admin.TabularInline):
    model = models.ShoeImage
    extra = 1
    readonly_fields = ()
    fields = ('image', 'alt_text')

class ShoeVariantInline(admin.TabularInline):
    model = models.ShoeVariant
    extra = 1
    fields = ('color', 'size', 'stock', 'sku')

# add/move inlines before CustomerAdmin
class CartItemInline(admin.TabularInline):
    model = models.CartItem
    extra = 0
    raw_id_fields = ('variant',)

class WishlistItemInline(admin.TabularInline):
    model = models.WishlistItem
    extra = 0
    raw_id_fields = ('shoe',)

class NotificationInline(admin.TabularInline):
    model = models.Notification
    extra = 0
    raw_id_fields = ('related_order',)
    fields = ('message', 'is_read', 'created_at', 'related_order')
    readonly_fields = ('created_at',)

class ShoeAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'gender', 'price')
    list_filter = ('brand', 'category', 'gender')
    search_fields = ('name', 'description', 'brand__name', 'variants__sku')
    inlines = [ShoeImageInline, ShoeVariantInline]
    autocomplete_fields = ('brand',)
    save_on_top = True

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)
    ordering = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'status', 'total_price')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__user__username', 'id')
    inlines = [OrderItemInline]
    raw_id_fields = ('customer',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price')
    search_fields = ('product_name', 'order__id')
    raw_id_fields = ('order',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'message', 'is_read', 'created_at', 'related_order')
    list_filter = ('is_read', 'created_at')
    search_fields = ('customer__user__username', 'message')
    raw_id_fields = ('customer', 'related_order')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'rating', 'date_added', 'order_item')
    search_fields = ('title', 'order_item__product_name')

class SiteAdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'user', 'role')
    raw_id_fields = ('user',)

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'shoe', 'date_added')
    search_fields = ('customer__user__username', 'shoe__name')
    raw_id_fields = ('customer', 'shoe')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('customer', 'variant', 'quantity')
    search_fields = ('customer__user__username', 'variant__sku')
    raw_id_fields = ('customer', 'variant')
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'mobile', 'theme_preference')
    search_fields = ('user__username', 'user__email', 'phone')
    raw_id_fields = ('user',)
    inlines = [CartItemInline, WishlistItemInline, NotificationInline]


admin.site.register(models.Shoe, ShoeAdmin)
admin.site.register(models.ShoeImage)
admin.site.register(models.ShoeVariant)
admin.site.register(models.Brand, BrandAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderItem, OrderItemAdmin)
admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Admin, SiteAdminAdmin)
admin.site.register(models.WishlistItem, WishlistItemAdmin)
admin.site.register(models.CartItem, CartItemAdmin)