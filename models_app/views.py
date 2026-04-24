from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .serializers import *
from django.contrib.auth.password_validation import validate_password
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'put']

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Customer.objects.none()
        return Customer.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return PaymentMethod.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
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


class PromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


"""class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
  # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
"""
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
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

    @action(detail=False, methods=['post'])  
    def checkout(self, request):            
        customer = getattr(request.user, "customer_profile", None)
        if not customer:
            return Response({"error": "No customer profile found"}, status=400)

        cart_items = CartItem.objects.filter(customer=customer)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        print("[OrderViewSet.checkout] user:", request.user.username)
        print("[OrderViewSet.checkout] customer_id:", customer.customer_id)
        print("[OrderViewSet.checkout] cart_count:", cart_items.count())

        shipping_address_id = request.data.get("shipping_address")
        billing_address_id = request.data.get("billing_address")
        payment_method_id = request.data.get("payment_method")

        print("[OrderViewSet.checkout] request.data:", dict(request.data))
        print("[OrderViewSet.checkout] shipping_address_id:", shipping_address_id)
        print("[OrderViewSet.checkout] billing_address_id:", billing_address_id)
        print("[OrderViewSet.checkout] payment_method_id:", payment_method_id)

        if not shipping_address_id:
            return Response({"error": "Shipping address is required"}, status=400)

        try:
            shipping_address = Address.objects.get(addr_id=shipping_address_id, customer=customer)
            print("[OrderViewSet.checkout] shipping_address:", shipping_address.addr_id, shipping_address.street, shipping_address.city)
        except Address.DoesNotExist:
            return Response({"error": "Shipping address not found"}, status=404)

        if billing_address_id in (None, "", "same"):
            billing_address = shipping_address
            print("[OrderViewSet.checkout] billing_address: same as shipping")
        else:
            try:
                billing_address = Address.objects.get(addr_id=billing_address_id, customer=customer)
                print("[OrderViewSet.checkout] billing_address:", billing_address.addr_id, billing_address.street, billing_address.city)
            except Address.DoesNotExist:
                return Response({"error": "Billing address not found"}, status=404)

        payment_method = None
        if payment_method_id not in (None, "", "cod"):
            try:
                payment_method = PaymentMethod.objects.get(card_id=payment_method_id, customer=customer)
                print("[OrderViewSet.checkout] payment_method:", payment_method.card_id, payment_method.masked, payment_method.holder_name)
            except PaymentMethod.DoesNotExist:
                return Response({"error": "Payment method not found"}, status=404)
        else:
            print("[OrderViewSet.checkout] payment_method: COD / none")

        total = sum(item.total_price for item in cart_items)
        print("[OrderViewSet.checkout] total:", total)

        order = Order.objects.create(
            customer=customer,
            total_price=total,
            status='Pending',
            shipping_address=shipping_address,
            billing_address=billing_address,
            payment_method=payment_method,
            subtotal=total,
            discount_amount=0,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                variant=item.variant,
                quantity=item.quantity,
                price=item.variant.shoe.price
            )

        cart_items.delete()

        # Create a notification for the customer
        Notification.objects.create(
            customer=customer,
            message=f"Your order #{order.order_id} has been placed successfully.",
            related_order=order
        )

        print("[OrderViewSet.checkout] order_id:", order.order_id)
        print("[OrderViewSet.checkout] items_created:", cart_items.count())

        return Response({
            "message": "Order placed",
            "order_id": order.order_id
        }, status=201)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__customer__user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(customer__user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = not notification.is_read
        notification.save()
        return Response({"status": "toggled", "is_read": notification.is_read})

    @action(detail=False, methods=['post'])
    def mark_all(self, request):
        notifications = self.get_queryset()
        notifications.update(is_read=True)
        return Response({"status": "all marked as read"})


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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer_profile)

    def perform_destroy(self, instance):
        if instance.customer.user != self.request.user:
            raise PermissionDenied("Cannot delete another user's wishlist item.")
        instance.delete()

class StoreLocationViewSet(viewsets.ModelViewSet):
    queryset = StoreLocation.objects.all()
    serializer_class = StoreLocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(customer__user=self.request.user)
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
        quantity = request.data.get('quantity', 1)

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            return Response({"error": "Quantity must be a number."}, status=400)

        if quantity < 1:
            return Response({"error": "Quantity must be at least 1."}, status=400)

        variant = get_object_or_404(ShoeVariant, variant_id=variant_id)
        if quantity > variant.stock:
            return Response({"error": f"Only {variant.stock} item(s) available for this variant."}, status=400)

        customer = request.user.customer_profile
        item, created = CartItem.objects.get_or_create(
            customer=customer,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            new_quantity = item.quantity + quantity
            if new_quantity > variant.stock:
                return Response({"error": f"Only {variant.stock} item(s) available for this variant."}, status=400)

            item.quantity = new_quantity
            item.save()
        return Response({"message": "Added to cart", "quantity": item.quantity if not created else quantity})

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
