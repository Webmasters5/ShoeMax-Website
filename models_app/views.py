from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .serializers import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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


"""class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
  # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
"""
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['post'])  
    def checkout(self, request):            
        customer = request.user.customer_profile
        cart_items = CartItem.objects.filter(customer=customer)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        total = sum(item.total_price for item in cart_items)

        order = Order.objects.create(
            customer=customer,
            total_price=total,
            status='pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                price=item.variant.shoe.price
            )

        cart_items.delete()

        return Response({
            "message": "Order placed",
            "order_id": order.order_id
        }, status=201)

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


"""class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]"""

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return CartItem.objects.filter(
            customer=self.request.user.customer_profile
        ).select_related('variant__shoe').prefetch_related('variant__shoe__images')

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        if not request.user.is_authenticated:
             return Response({"error": "Authentication required"}, status=401)
      
        items = self.get_queryset()
        data = []
        for item in items:
            image_obj = item.variant.shoe.images.first()

            data.append({
                "id": item.id,
                "shoe_name": item.variant.shoe.name,
                "color": item.variant.color,
                "size": str(item.variant.size),
                "price": float(item.variant.shoe.price),
                "quantity": item.quantity,
                "total_price": float(item.total_price),
                "image": image_obj.image.url if image_obj else None,
            })
        subtotal = sum(i["total_price"] for i in data)
        return Response({
            "items": data,
            "subtotal": subtotal,
            "discount": 0,
            "total": subtotal
        })
        
   
    @action(detail=False, methods=['post'])
    def add(self, request):
        if not request.user.is_authenticated:
         return Response({"error": "Authentication required"}, status=401)

        variant_id = request.data.get('variant')
        variant = ShoeVariant.objects.get(variant_id=variant_id)
        customer = request.user.customer_profile
        item, created = CartItem.objects.get_or_create(
            customer=customer,
            variant=variant,
            defaults={'quantity': 1}
        )
        if not created:
            item.quantity += 1
            item.save()
        return Response({"message": "Added to cart"})

    @action(detail=True, methods=['post']) 
    def increment(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        item = self.get_object()
        item.quantity += 1
        item.save()
        return Response({"quantity": item.quantity, "total_price": float(item.total_price)})

    @action(detail=True, methods=['post'])
    def decrement(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)
       
        item = self.get_object()
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return Response({"removed": True})
        item.save()
        return Response({"quantity": item.quantity, "total_price": float(item.total_price)})

    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)
        
        item = self.get_object()
        item.delete()
        return Response({"removed": True})
