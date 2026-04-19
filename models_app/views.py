from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .serializers import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'patch', 'put']

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return User.objects.none()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        new_password = request.data.get("password")

        if not new_password:
            return Response({"error": "Password required"}, status=400)

        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"error": e.messages}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"status": "password updated"})


class ShoeViewSet(viewsets.ModelViewSet):
    queryset = Shoe.objects.all()
    serializer_class = ShoeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ShoeImageViewSet(viewsets.ModelViewSet):
    queryset = ShoeImage.objects.all()
    serializer_class = ShoeImageSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ShoeVariantViewSet(viewsets.ModelViewSet):
    queryset = ShoeVariant.objects.all()
    serializer_class = ShoeVariantSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Customer.objects.none()
        return Customer.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#class PaymentMethodViewSet(viewsets.ModelViewSet):
#    serializer_class = PaymentMethodSerializer
#    permission_classes = [permissions.IsAuthenticated]

#    def get_queryset(self):
#        return PaymentMethod.objects.filter(customer__user=self.request.user)

#    def perform_create(self, serializer):
#        serializer.save(customer=self.request.user.customer_profile)


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(customer__user=self.request.user)
    
    def get_customer(self):
        return getattr(self.request.user, "customer_profile", None)
    
    def perform_create(self, serializer):
        customer = self.get_customer()
        if not customer:
            raise PermissionDenied("No customer profile")
        serializer.save(customer=customer)


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)
    
    def get_customer(self):
        return getattr(self.request.user, "customer_profile", None)
    
    def perform_create(self, serializer):
        customer = self.get_customer()
        if not customer:
            raise PermissionDenied("No customer profile")
        serializer.save(customer=customer)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__customer__user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(customer__user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "read"})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class WishlistItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(customer__user=self.request.user)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(customer__user=self.request.user)
