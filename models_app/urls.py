from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    ShoeViewSet,
    ShoeImageViewSet,
    ShoeVariantViewSet,
    BrandViewSet,
    CustomerViewSet,
    PaymentMethodViewSet,
    AddressViewSet,
    PromoViewSet,
    OrderViewSet,
    OrderItemViewSet,
    NotificationViewSet,
    ReviewViewSet,
    AdminViewSet,
    WishlistItemViewSet,
    CartItemViewSet,
    StoreLocationViewSet,
)

router = DefaultRouter()
router.register(r'shoes', ShoeViewSet, basename='shoe')
router.register(r'shoe-images', ShoeImageViewSet, basename='shoeimage')
router.register(r'shoe-variants', ShoeVariantViewSet, basename='shoevariant')
router.register(r'brands', BrandViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'promos', PromoViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'users', UserViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'wishlist-items', WishlistItemViewSet)
router.register(r'cart-items', CartItemViewSet)
router.register(r'stores', StoreLocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
