from rest_framework import permissions, viewsets
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ShoeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shoe.objects.all()
    serializer_class = ShoeSerializer

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        category = self.request.GET.get('category', '').strip()
        brand = self.request.GET.get('brand', '').strip()
        gender = self.request.GET.get('gender', '').strip()
        min_price = self.request.GET.get('min_price', '').strip()
        max_price = self.request.GET.get('max_price', '').strip()

        qs = Shoe.objects.all().prefetch_related('images')

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        if category:
            qs = qs.filter(category__iexact=category)

        if brand:
            try:
                brand_id = int(brand)
                qs = qs.filter(brand_id=brand_id)
            except (ValueError, TypeError):
                pass

        if gender:
            qs = qs.filter(gender__iexact=gender)

        if min_price:
            try:
                qs = qs.filter(price__gte=float(min_price))
            except (ValueError, TypeError):
                pass

        if max_price:
            try:
                qs = qs.filter(price__lte=float(max_price))
            except (ValueError, TypeError):
                pass

        return qs.order_by('price', 'name')


class ShoeImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShoeImage.objects.all()
    serializer_class = ShoeImageSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ShoeVariantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShoeVariant.objects.all()
    serializer_class = ShoeVariantSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class WishlistItemViewSet(viewsets.ModelViewSet):
    queryset = WishlistItem.objects.all()
    serializer_class = WishlistItemSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
